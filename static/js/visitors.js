/* Visitors page — world bubble map + bar charts.
   Reads two static files: /static/data/world.json (base map) and
   /static/data/visitors.json (aggregated statistics, refreshed by the daily build).
   No external libraries. All labels are inserted with textContent. */
(function () {
  'use strict';

  var root = document.getElementById('visitors');
  if (!root) return;

  var SVG = 'http://www.w3.org/2000/svg';
  var TOP_COUNTRIES = 10;      // rows shown before "Show all"
  var R_MAX = 30, R_MIN = 3;   // bubble radius range (map units)

  var state = { range: null, country: null, showAll: false };
  var data, world, anchors = {};
  var fmt = new Intl.NumberFormat('en');
  var regionNames = null;
  try { regionNames = new Intl.DisplayNames(['en'], { type: 'region' }); } catch (e) { /* old browser */ }

  // ---------- helpers ----------
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text !== undefined && text !== null) n.textContent = text;
    return n;
  }
  function svg(tag, attrs) {
    var n = document.createElementNS(SVG, tag);
    for (var k in attrs) n.setAttribute(k, attrs[k]);
    return n;
  }
  function clear(n) { while (n.firstChild) n.removeChild(n.firstChild); }
  function $(id) { return document.getElementById(id); }
  function countryName(code) {
    try { if (regionNames) return regionNames.of(code) || code; } catch (e) { /* unknown code */ }
    return code;
  }
  function compact(n) {
    if (n >= 1e6) return (n / 1e6).toFixed(1).replace(/\.0$/, '') + 'M';
    if (n >= 1e4) return (n / 1e3).toFixed(1).replace(/\.0$/, '') + 'K';
    return fmt.format(n);
  }
  function title(s) { return s ? s.charAt(0).toUpperCase() + s.slice(1) : s; }

  // ---------- tooltip ----------
  var tip = el('div', 'vz-tip');
  tip.setAttribute('role', 'status');
  tip.hidden = true;
  document.body.appendChild(tip);

  function showTip(value, label, x, y) {
    clear(tip);
    tip.appendChild(el('strong', null, value));
    tip.appendChild(el('span', null, label));
    tip.hidden = false;
    var w = tip.offsetWidth, h = tip.offsetHeight;
    var left = Math.min(Math.max(8, x - w / 2), window.innerWidth - w - 8);
    var top = y - h - 12;
    if (top < 8) top = y + 16;
    tip.style.left = left + 'px';
    tip.style.top = top + 'px';
  }
  function hideTip() { tip.hidden = true; }
  function bindTip(node, value, label) {
    node.addEventListener('pointermove', function (e) { showTip(value, label, e.clientX, e.clientY); });
    node.addEventListener('pointerleave', hideTip);
    node.addEventListener('focus', function () {
      var r = node.getBoundingClientRect();
      showTip(value, label, r.left + r.width / 2, r.top);
    });
    node.addEventListener('blur', hideTip);
  }

  // ---------- range filter ----------
  function renderFilter() {
    var box = $('vz-filter');
    clear(box);
    Object.keys(data.ranges).forEach(function (key) {
      var b = el('button', 'vz-range' + (key === state.range ? ' active' : ''), data.ranges[key].label);
      b.type = 'button';
      b.setAttribute('aria-pressed', key === state.range ? 'true' : 'false');
      b.addEventListener('click', function () {
        state.range = key;
        state.showAll = false;
        render();
      });
      box.appendChild(b);
    });
  }

  // ---------- stat tiles ----------
  function renderTiles(r) {
    var box = $('vz-tiles');
    clear(box);
    var unit = r.unit === 'day' ? 'day' : 'month';
    var pts = r.series || [];
    var busiest = pts.reduce(function (m, p) { return Math.max(m, p.visitors); }, 0);
    var average = pts.length ? Math.round(r.totals.visitors / pts.length) : 0;
    [['Visitors', r.totals.visitors], ['Countries', r.countries.length],
     ['Average per ' + unit, average], ['Busiest ' + unit, busiest]].forEach(function (t) {
      var tile = el('div', 'vz-tile');
      tile.appendChild(el('div', 'vz-tile-value', compact(t[1] || 0)));
      tile.appendChild(el('div', 'vz-tile-label', t[0]));
      tile.title = fmt.format(t[1] || 0);
      box.appendChild(tile);
    });
  }

  // ---------- map ----------
  function renderMap(r) {
    var box = $('vz-map');
    clear(box);
    var s = svg('svg', {
      viewBox: '0 0 ' + world.width + ' ' + world.height,
      role: 'group', 'aria-label': 'World map of visitors by country'
    });
    var visited = {};
    r.countries.forEach(function (c) { visited[c.code] = c; });

    var land = svg('g', { 'class': 'vz-land' });
    world.countries.forEach(function (c) {
      if (!c.d) return;
      var cls = (visited[c.id] ? 'has-visitors' : '') + (c.id && c.id === state.country ? ' selected' : '');
      land.appendChild(svg('path', { d: c.d, 'class': cls.trim() }));
    });
    s.appendChild(land);

    var max = r.countries.reduce(function (m, c) { return Math.max(m, c.visitors); }, 1);
    function radius(v) { return Math.max(R_MIN, R_MAX * Math.sqrt(v / max)); }

    // big bubbles first, so small ones stay reachable on top
    var bubbles = svg('g', { 'class': 'vz-bubbles' });
    r.countries.slice().sort(function (a, b) { return b.visitors - a.visitors; }).forEach(function (c) {
      var p = anchors[c.code];
      if (!p) return;
      var name = countryName(c.code);
      var g = svg('g', {
        'class': 'vz-bubble' + (c.code === state.country ? ' selected' : ''),
        tabindex: '0', role: 'button',
        'aria-label': name + ': ' + fmt.format(c.visitors) + ' visitors'
      });
      var rad = radius(c.visitors);
      g.appendChild(svg('circle', { cx: p.x, cy: p.y, r: Math.max(rad, 9), 'class': 'vz-hit' }));
      g.appendChild(svg('circle', { cx: p.x, cy: p.y, r: rad, 'class': 'vz-dot' }));
      bindTip(g, fmt.format(c.visitors), name);
      function pick() { selectCountry(c.code, true); }
      g.addEventListener('click', pick);
      g.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pick(); }
      });
      bubbles.appendChild(g);
    });
    s.appendChild(bubbles);
    box.appendChild(s);

    // size legend
    var legend = $('vz-map-legend');
    clear(legend);
    var steps = [max];
    if (max >= 10) steps.push(Math.round(max / 4));
    if (max >= 100) steps.push(Math.round(max / 25));
    steps.forEach(function (v) {
      var item = el('span', 'vz-legend-item');
      var d = Math.round(2 * radius(v) * (box.clientWidth / world.width));
      var dot = el('span', 'vz-legend-dot');
      dot.style.width = dot.style.height = Math.max(d, 4) + 'px';
      item.appendChild(dot);
      item.appendChild(el('span', null, compact(v)));
      legend.appendChild(item);
    });
    legend.appendChild(el('span', 'vz-legend-note', 'visitors · bubble area is proportional'));
  }

  // ---------- bar rows ----------
  function barRow(label, value, max, opts) {
    opts = opts || {};
    var row = el(opts.button ? 'button' : 'div', 'vz-row' + (opts.cls ? ' ' + opts.cls : ''));
    if (opts.button) row.type = 'button';
    var name = el('span', 'vz-row-label', label);
    name.title = label;
    var track = el('span', 'vz-row-track');
    var bar = el('span', 'vz-row-bar');
    bar.style.width = Math.max(0.6, 100 * value / max) + '%';
    track.appendChild(bar);
    row.appendChild(name);
    row.appendChild(track);
    row.appendChild(el('span', 'vz-row-value', fmt.format(value)));
    return row;
  }

  function renderCountries(r) {
    var box = $('vz-countries');
    clear(box);
    var max = r.countries.reduce(function (m, c) { return Math.max(m, c.visitors); }, 1);
    var list = r.countries;
    var selectedIndex = list.findIndex(function (c) { return c.code === state.country; });
    var limit = state.showAll ? list.length : Math.max(TOP_COUNTRIES, selectedIndex + 1);

    list.slice(0, limit).forEach(function (c) {
      var open = c.code === state.country;
      var item = el('div', 'vz-country' + (open ? ' open' : ''));
      item.id = 'vz-country-' + c.code;
      var row = barRow(countryName(c.code), c.visitors, max, { button: true });
      row.setAttribute('aria-expanded', open ? 'true' : 'false');
      row.insertBefore(el('span', 'vz-caret', '›'), row.firstChild);
      row.addEventListener('click', function () { selectCountry(open ? null : c.code, false); });
      item.appendChild(row);

      if (open) {
        var regions = el('div', 'vz-regions');
        if (c.regions && c.regions.length) {
          var cmax = c.regions[0].visitors;
          c.regions.forEach(function (region) {
            regions.appendChild(barRow(region.name, region.visitors, Math.max(cmax, 1), { cls: 'vz-region' }));
          });
        } else {
          regions.appendChild(el('p', 'vz-empty-note', 'No regional data for this country.'));
        }
        item.appendChild(regions);
      }
      box.appendChild(item);
    });

    if (list.length > TOP_COUNTRIES) {
      var more = el('button', 'vz-more',
        state.showAll ? 'Show fewer' : 'Show all ' + list.length + ' countries');
      more.type = 'button';
      more.addEventListener('click', function () { state.showAll = !state.showAll; renderCountries(r); });
      box.appendChild(more);
    }
  }

  function selectCountry(code, scroll) {
    state.country = code;
    var r = data.ranges[state.range];
    renderMap(r);
    renderCountries(r);
    if (scroll && code) {
      var target = $('vz-country-' + code);
      if (target) target.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }

  // ---------- time series (columns) ----------
  function niceMax(v) {
    var p = Math.pow(10, Math.floor(Math.log10(Math.max(v, 1))));
    var n = v / p;
    return (n <= 1 ? 1 : n <= 2 ? 2 : n <= 5 ? 5 : 10) * p;
  }
  function periodLabel(t, unit, long) {
    var parts = t.split('-');
    var d = new Date(Date.UTC(+parts[0], +parts[1] - 1, +(parts[2] || 1)));
    var o = unit === 'day'
      ? (long ? { day: 'numeric', month: 'long', year: 'numeric' } : { day: 'numeric', month: 'short' })
      : (long ? { month: 'long', year: 'numeric' } : { month: 'short', year: '2-digit' });
    o.timeZone = 'UTC';
    return d.toLocaleDateString('en-GB', o);
  }

  function renderSeries(r) {
    var box = $('vz-series');
    clear(box);
    $('vz-series-title').textContent = 'Visitors per ' + (r.unit === 'day' ? 'day' : 'month');
    var pts = r.series || [];
    if (!pts.length) { box.appendChild(el('p', 'vz-empty-note', 'No data for this period yet.')); return; }

    var W = Math.max(box.clientWidth, 280), H = 210;
    var m = { l: 40, r: 8, t: 10, b: 24 };
    var iw = W - m.l - m.r, ih = H - m.t - m.b;
    var top = niceMax(pts.reduce(function (a, p) { return Math.max(a, p.visitors); }, 1));
    var band = iw / pts.length;
    var bw = Math.max(2, Math.min(24, band - 2));
    var s = svg('svg', { viewBox: '0 0 ' + W + ' ' + H, width: W, height: H, role: 'group',
                         'aria-label': $('vz-series-title').textContent });

    [0, 0.5, 1].forEach(function (f) {
      var y = m.t + ih - f * ih;
      s.appendChild(svg('line', { x1: m.l, x2: W - m.r, y1: y, y2: y, 'class': f ? 'vz-grid' : 'vz-axis' }));
      var t = svg('text', { x: m.l - 8, y: y + 4, 'text-anchor': 'end', 'class': 'vz-tick' });
      t.textContent = compact(Math.round(top * f));
      s.appendChild(t);
    });

    var every = Math.ceil(pts.length / Math.max(2, Math.floor(iw / 64)));
    pts.forEach(function (p, i) {
      var x = m.l + i * band + (band - bw) / 2;
      var h = Math.max(p.visitors ? 1.5 : 0, ih * p.visitors / top);
      var y = m.t + ih - h;
      var rr = Math.min(4, bw / 2, h);
      var g = svg('g', { 'class': 'vz-col', tabindex: '0', role: 'img',
        'aria-label': periodLabel(p.t, r.unit, true) + ': ' + fmt.format(p.visitors) + ' visitors' });
      g.appendChild(svg('rect', { x: m.l + i * band, y: m.t, width: band, height: ih, 'class': 'vz-hit' }));
      // rounded at the data end, square at the baseline
      g.appendChild(svg('path', { 'class': 'vz-col-bar', d:
        'M' + x + ',' + (y + h) + 'V' + (y + rr) + 'Q' + x + ',' + y + ' ' + (x + rr) + ',' + y +
        'H' + (x + bw - rr) + 'Q' + (x + bw) + ',' + y + ' ' + (x + bw) + ',' + (y + rr) +
        'V' + (y + h) + 'Z' }));
      bindTip(g, fmt.format(p.visitors) + ' visitors', periodLabel(p.t, r.unit, true));
      s.appendChild(g);
      if (i % every === 0) {
        var t = svg('text', { x: m.l + i * band + band / 2, y: H - 6, 'text-anchor': 'middle', 'class': 'vz-tick' });
        t.textContent = periodLabel(p.t, r.unit, false);
        s.appendChild(t);
      }
    });
    box.appendChild(s);
  }

  // ---------- small bar lists ----------
  function renderList(id, rows, transform) {
    var box = $(id);
    clear(box);
    if (!rows || !rows.length) { box.appendChild(el('p', 'vz-empty-note', 'No data yet.')); return; }
    var max = rows.reduce(function (m, x) { return Math.max(m, x.value); }, 1);
    rows.forEach(function (x) {
      box.appendChild(barRow(transform ? transform(x.name) : x.name, x.value, max));
    });
  }

  // ---------- page ----------
  function render() {
    var r = data.ranges[state.range];
    if (state.country && !r.countries.some(function (c) { return c.code === state.country; })) {
      state.country = null;
    }
    renderFilter();
    renderTiles(r);
    renderMap(r);
    renderCountries(r);
    renderSeries(r);
    renderList('vz-pages', r.pages);
    renderList('vz-referrers', r.referrers);
    renderList('vz-browsers', r.browsers, title);
    renderList('vz-systems', r.systems);
    renderList('vz-devices', r.devices, title);
  }

  function empty(message) {
    $('vz-status').textContent = message;
    $('vz-status').hidden = false;
    $('vz-body').hidden = true;
  }

  function getJSON(url) {
    return fetch(url, { cache: 'no-cache' }).then(function (res) {
      if (!res.ok) throw new Error(url + ': ' + res.status);
      return res.json();
    });
  }

  Promise.all([getJSON(root.getAttribute('data-world')), getJSON(root.getAttribute('data-stats'))])
    .then(function (res) {
      world = res[0];
      data = res[1];
      world.countries.forEach(function (c) {
        if (c.id && c.x !== null && c.x !== undefined) anchors[c.id] = c;
      });
      var keys = Object.keys(data.ranges || {});
      if (!keys.length) {
        empty('We have only just started counting — the map will appear here once the first statistics are in.');
        return;
      }
      state.range = data.ranges.all ? 'all' : keys[keys.length - 1];
      $('vz-status').hidden = true;
      $('vz-body').hidden = false;
      $('vz-demo').hidden = !data.demo;
      if (data.generated) {
        var d = new Date(data.generated);
        var since = data.since ? new Date(data.since + 'T00:00:00Z') : null;
        var o = { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC' };
        $('vz-updated').textContent =
          (since ? 'Counting since ' + since.toLocaleDateString('en-GB', o) + ' · ' : '') +
          'updated ' + d.toLocaleDateString('en-GB', o);
      }
      render();
      var t;
      window.addEventListener('resize', function () {
        clearTimeout(t);
        t = setTimeout(function () {
          renderSeries(data.ranges[state.range]);
          renderMap(data.ranges[state.range]);
        }, 150);
      });
    })
    .catch(function (err) {
      console.error(err);
      empty('The statistics could not be loaded. Please try again later.');
    });
})();

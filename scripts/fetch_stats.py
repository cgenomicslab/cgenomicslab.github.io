#!/usr/bin/env python3
"""Fetch aggregated visitor statistics from GoatCounter -> static/data/visitors.json

Runs in the GitHub Actions build (see .github/workflows/jekyll.yml), so the API
key never reaches the browser: the public page only reads the aggregated JSON.

Environment:
    GOATCOUNTER_API_KEY   API token with "Read statistics" (repository secret)
    GOATCOUNTER_CODE      site code; default: goatcounter.code in _config.yml
    GOATCOUNTER_URL       default https://<code>.goatcounter.com;
                          set it for a self-hosted GoatCounter

Usage:
    python3 scripts/fetch_stats.py            # fetch real data
    python3 scripts/fetch_stats.py --archive  # store finished months in the archive
    python3 scripts/fetch_stats.py --demo     # synthetic data, for local preview only

Archive: every finished calendar month is saved once to
_data/visitors_archive.json (committed by .github/workflows/stats-archive.yml),
so the history lives in this repository and does not depend on the counter
keeping it. "Last 12 months" and "All time" are built from the archived months
plus the running month. Monthly visitor counts are added up, so someone who
visits in two different months counts twice.

All dates are UTC days, which is how GoatCounter stores its statistics.
Only the Python standard library is used.
"""
import datetime as dt
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "static", "data", "visitors.json")
ARCHIVE = os.path.join(ROOT, "_data", "visitors_archive.json")
LIVE_COPY = "https://cgenomicslab.org/static/data/visitors.json"

EARLIEST = dt.date(2026, 1, 1)   # counting cannot have started before this
MAX_COUNTRIES = 60        # countries listed per range
MAX_REGION_COUNTRIES = 30  # countries that get a region breakdown
MAX_REGIONS = 15          # regions per country
MAX_ROWS = 10             # pages / referrers / browsers / ...
MIN_REGION_VISITORS = 1   # raise to hide regions with very few visitors
PAUSE = 0.3               # seconds between calls (limit: 4 calls / second)

# The archive keeps longer lists than the page shows, so that rankings stay
# right when many months are added together.
ARCHIVE_LIMITS = {"countries": 250, "region_countries": 40, "regions": 30, "rows": 50}
PAGE_LIMITS = {"countries": MAX_COUNTRIES, "region_countries": MAX_REGION_COUNTRIES,
               "regions": MAX_REGIONS, "rows": MAX_ROWS}
LISTS = ("pages", "referrers", "browsers", "systems", "devices")
SCREENS = {"phone": "Phones", "largephone": "Large phones, small tablets",
           "tablet": "Tablets and small laptops", "desktop": "Computer monitors",
           "desktophd": "Large monitors", "unknown": "Unknown"}


def config_code():
    try:
        with open(os.path.join(ROOT, "_config.yml"), encoding="utf-8") as fh:
            m = re.search(r'^goatcounter:\s*\n(?:[ \t]+.*\n)*?[ \t]+code:\s*"?([A-Za-z0-9_-]*)"?',
                          fh.read(), re.M)
        return m.group(1) if m else ""
    except OSError:
        return ""


class GoatCounter:
    def __init__(self, base, key):
        self.base = base.rstrip("/") + "/api/v0"
        self.key = key

    def get(self, path, start, end, **params):
        params.update(start=start.strftime("%Y-%m-%dT00:00:00Z"),
                      end=end.strftime("%Y-%m-%dT23:00:00Z"))
        url = "%s/%s?%s" % (self.base, path, urllib.parse.urlencode(params))
        req = urllib.request.Request(url, headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.key,
            "User-Agent": "cglab-site-stats/1.0",
        })
        for attempt in range(4):
            time.sleep(PAUSE)
            try:
                with urllib.request.urlopen(req, timeout=30) as r:
                    return json.load(r)
            except urllib.error.HTTPError as err:
                if err.code != 429 or attempt == 3:
                    raise
                time.sleep(float(err.headers.get("X-Rate-Limit-Reset") or 2) + 0.5)

    def rows(self, path, start, end, limit):
        """A ranked list; follows pagination (at most 100 rows per call)."""
        out = []
        while len(out) < limit:
            page = self.get(path, start, end, limit=min(100, limit - len(out)), offset=len(out))
            stats = page.get("stats") or []
            out.extend({"id": str(r.get("id") or ""), "name": str(r.get("name") or ""),
                        "value": int(r.get("count") or 0)} for r in stats)
            if not page.get("more") or not stats:
                break
        return [r for r in out if r["value"] > 0]

    def days(self, start, end):
        """Visitors per day, and their sum."""
        data = self.get("stats/total", start, end)
        return ({str(s["day"])[:10]: int(s.get("daily") or 0) for s in data.get("stats") or []},
                int(data.get("total") or 0))


def named(rows):
    return [{"name": r["name"] or r["id"], "value": r["value"]} for r in rows
            if r["name"] or r["id"]]


def snapshot(api, start, end, limits):
    """Everything the page shows for one period (whole days, both included)."""
    _, total = api.days(start, end)

    countries = []
    for i, row in enumerate(api.rows("stats/locations", start, end, limits["countries"])):
        code = row["id"].upper()
        if not re.fullmatch(r"[A-Z]{2}", code):
            continue
        entry = {"code": code, "visitors": row["value"], "regions": []}
        if i < limits["region_countries"]:
            regions = api.rows("stats/locations/" + code, start, end, limits["regions"])
            entry["regions"] = [{"name": r["name"], "visitors": r["value"]} for r in regions
                                if r["name"] and r["name"] != "(unknown)"]
        countries.append(entry)

    hits = api.get("stats/hits", start, end, limit=min(100, limits["rows"]))
    pages = [{"name": str(h["path"]), "value": int(h.get("count") or 0)}
             for h in hits.get("hits") or [] if not h.get("event") and h.get("count")]

    sizes = api.rows("stats/sizes", start, end, 10)
    devices = [{"name": SCREENS.get(r["id"], r["name"] or r["id"]), "value": r["value"]}
               for r in sizes if r["id"] != "unknown"]

    return {
        "totals": {"visitors": total},
        "countries": countries,
        "pages": pages,
        "referrers": named(api.rows("stats/toprefs", start, end, limits["rows"] + 5)),
        "browsers": named(api.rows("stats/browsers", start, end, limits["rows"])),
        "systems": named(api.rows("stats/systems", start, end, limits["rows"])),
        "devices": devices,
    }


def ranked(counts, key, value):
    return [{key: k, value: v} for k, v in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))]


def combine(records):
    """Add several periods (months) together."""
    total = 0
    countries, regions, lists = {}, {}, {k: {} for k in LISTS}
    for rec in records:
        total += int(rec.get("totals", {}).get("visitors", 0))
        for c in rec.get("countries", []):
            countries[c["code"]] = countries.get(c["code"], 0) + c["visitors"]
            into = regions.setdefault(c["code"], {})
            for r in c.get("regions", []):
                into[r["name"]] = into.get(r["name"], 0) + r["visitors"]
        for k in LISTS:
            for row in rec.get(k, []):
                lists[k][row["name"]] = lists[k].get(row["name"], 0) + row["value"]
    out = {"totals": {"visitors": total},
           "countries": [dict(c, regions=ranked(regions.get(c["code"], {}), "name", "visitors"))
                         for c in ranked(countries, "code", "visitors")]}
    for k in LISTS:
        out[k] = ranked(lists[k], "name", "value")
    return out


def for_page(rec):
    """Cut a record down to what the page shows."""
    out = {"totals": rec["totals"]}
    out["countries"] = [
        dict(c, regions=[x for x in c.get("regions", [])
                         if x["visitors"] >= MIN_REGION_VISITORS][:MAX_REGIONS]
             if i < MAX_REGION_COUNTRIES else [])
        for i, c in enumerate(rec["countries"][:MAX_COUNTRIES])]
    for k in LISTS:
        out[k] = rec.get(k, [])[:MAX_ROWS]
    out["referrers"] = [r for r in rec.get("referrers", [])
                        if "cgenomicslab.org" not in r["name"]][:MAX_ROWS]
    return out


# ---------- months ----------
def month_start(d):
    return d.replace(day=1)


def next_month(d):
    return (d.replace(day=28) + dt.timedelta(days=5)).replace(day=1)


def month_end(d):
    return next_month(d) - dt.timedelta(days=1)


def month_key(d):
    return d.strftime("%Y-%m")


def months_between(first, last):
    """Month starts from the month of `first` up to and including that of `last`."""
    m, out = month_start(first), []
    while m <= month_start(last):
        out.append(m)
        m = next_month(m)
    return out


def load_archive():
    try:
        with open(ARCHIVE, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        data = {}
    data.setdefault("since", None)
    data.setdefault("months", {})
    return data


def first_day(api, archive, today):
    """First day with a visitor: from the archive, else from the counter."""
    if archive["since"]:
        return dt.date.fromisoformat(archive["since"])
    days, _ = api.days(EARLIEST, today)
    seen = sorted(d for d, n in days.items() if n > 0)
    return dt.date.fromisoformat(seen[0]) if seen else None


def archive_months(api):
    """Save every finished month that is not in the archive yet."""
    today = dt.datetime.now(dt.timezone.utc).date()
    archive = load_archive()
    before = json.dumps(archive, sort_keys=True)
    first = first_day(api, archive, today)
    if first is None:
        print("no visitors counted yet — nothing to archive")
        return
    archive["since"] = first.isoformat()

    added = []
    for m in months_between(first, today)[:-1]:          # [-1] is the running month
        key = month_key(m)
        if key in archive["months"]:
            continue
        rec = snapshot(api, max(m, first), month_end(m), ARCHIVE_LIMITS)
        rec["archived"] = today.isoformat()
        archive["months"][key] = rec
        added.append(key)

    if json.dumps(archive, sort_keys=True) != before:
        os.makedirs(os.path.dirname(ARCHIVE), exist_ok=True)
        with open(ARCHIVE, "w", encoding="utf-8") as fh:
            json.dump(archive, fh, ensure_ascii=False, indent=1, sort_keys=True)
            fh.write("\n")
    print("archived: %s" % (", ".join(added) or "nothing new"))


def fetch(api):
    now = dt.datetime.now(dt.timezone.utc)
    today = now.date()
    archive = load_archive()
    first = first_day(api, archive, today)
    out = {"generated": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "ranges": {}}
    if first is None:
        return out                       # page shows "just started counting"
    out["since"] = first.isoformat()

    # last 30 days: straight from the counter, with a daily series
    start = max(first, today - dt.timedelta(days=29))
    recent = for_page(snapshot(api, start, today, PAGE_LIMITS))
    days, _ = api.days(start, today)
    span = (today - start).days + 1
    recent.update(label="Last 30 days", unit="day", series=[
        {"t": d.isoformat(), "visitors": days.get(d.isoformat(), 0)}
        for d in (start + dt.timedelta(days=i) for i in range(span))])
    out["ranges"]["30d"] = recent

    # longer periods: archived months + months not archived yet + the running month
    months = months_between(first, today)
    records = {}
    for m in months:
        key = month_key(m)
        records[key] = archive["months"].get(key) or snapshot(
            api, max(m, first), min(month_end(m), today), ARCHIVE_LIMITS)

    for key, label, keys in (("12m", "Last 12 months", [month_key(m) for m in months[-12:]]),
                             ("all", "All time", [month_key(m) for m in months])):
        data = for_page(combine([records[k] for k in keys]))
        data.update(label=label, unit="month", series=[
            {"t": k, "visitors": records[k]["totals"]["visitors"]} for k in keys])
        out["ranges"][key] = data
    return out


def demo():
    """Synthetic numbers so the page can be previewed before real data exists."""
    rnd = random.Random(7)
    places = {
        "GR": ["Crete", "Attica", "Central Macedonia", "Western Greece", "Thessaly", "Epirus"],
        "US": ["New York", "Massachusetts", "California", "Washington", "Illinois"],
        "DE": ["Baden-Württemberg", "Berlin", "Bavaria", "North Rhine-Westphalia"],
        "ES": ["Catalonia", "Madrid", "Valencia"],
        "GB": ["England", "Scotland", "Wales"],
        "FR": ["Île-de-France", "Auvergne-Rhône-Alpes", "Nouvelle-Aquitaine"],
        "CA": ["British Columbia", "Ontario", "Quebec"],
        "IT": ["Lazio", "Lombardy", "Campania"],
        "NL": ["North Holland", "Utrecht"], "CH": ["Zurich", "Basel-City", "Vaud"],
        "CN": ["Beijing", "Shanghai"], "JP": ["Tokyo", "Kyoto"], "IN": ["Karnataka", "Delhi"],
        "TR": ["Istanbul", "Ankara"], "AU": ["New South Wales", "Victoria"],
        "BR": ["São Paulo"], "SE": ["Stockholm"], "CY": ["Nicosia"], "IL": ["Tel Aviv"],
        "SG": [], "ZA": ["Western Cape"], "AR": ["Buenos Aires"], "MX": ["Mexico City"],
        "AT": ["Vienna"],
    }
    weights = [400, 160, 120, 90, 80, 60, 55, 40, 35, 30, 28, 24, 22, 20, 18, 12, 10, 9,
               8, 7, 5, 4, 4, 3]
    now = dt.datetime.now(dt.timezone.utc)
    out = {"generated": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "demo": True,
           "since": (now - dt.timedelta(days=540)).strftime("%Y-%m-%d"), "ranges": {}}
    for key, label, unit, steps, scale in (("30d", "Last 30 days", "day", 30, 1),
                                           ("12m", "Last 12 months", "month", 12, 9),
                                           ("all", "All time", "month", 18, 13)):
        countries = []
        for (code, regions), w in zip(places.items(), weights):
            n = max(1, int(w * scale * rnd.uniform(0.8, 1.2)))
            share = sorted((rnd.random() ** 2 for _ in regions), reverse=True)
            rows = [{"name": c, "visitors": max(1, int(n * 0.8 * f / sum(share)))}
                    for c, f in zip(regions, share)]
            countries.append({"code": code, "visitors": n, "regions": rows})
        countries.sort(key=lambda c: -c["visitors"])
        visitors = sum(c["visitors"] for c in countries)
        series = []
        for i in range(steps):
            d = now - (dt.timedelta(days=steps - 1 - i) if unit == "day"
                       else dt.timedelta(days=30.4 * (steps - 1 - i)))
            series.append({"t": d.strftime("%Y-%m-%d" if unit == "day" else "%Y-%m"),
                           "visitors": max(1, int(visitors / steps * rnd.uniform(0.6, 1.4)))})

        def rows(names, top):
            vals = sorted((int(top * rnd.uniform(0.2, 1) / (i + 1)) + 1
                           for i in range(len(names))), reverse=True)
            return [{"name": n, "value": v} for n, v in zip(names, vals)]

        out["ranges"][key] = {
            "label": label, "unit": unit, "series": series, "countries": countries,
            "totals": {"visitors": visitors},
            "pages": rows(["/", "/research/", "/members/", "/join/", "/teaching/",
                           "/members/pittis/", "/publications/", "/contact/"], visitors),
            "referrers": rows(["Google", "imbb.forth.gr", "scholar.google.com",
                               "github.com", "bsky.app", "linkedin.com"], visitors // 3),
            "browsers": rows(["Chrome", "Firefox", "Safari", "Edge"], visitors),
            "systems": rows(["Windows", "macOS", "Linux", "iOS", "Android"], visitors),
            "devices": rows(["Computer monitors", "Phones", "Large monitors",
                             "Tablets and small laptops"], visitors),
        }
    return out


def write(data):
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, separators=(",", ":"))
        fh.write("\n")
    print("wrote", os.path.normpath(OUT))


def keep_published_copy():
    """If the API is unreachable, re-publish the numbers that are already live."""
    try:
        with urllib.request.urlopen(LIVE_COPY, timeout=20) as r:
            data = json.load(r)
        if data.get("ranges") and not data.get("demo"):
            write(data)
            print("kept the currently published statistics")
    except (urllib.error.URLError, ValueError) as err:
        print("could not reuse the published statistics:", err)


def main():
    if "--demo" in sys.argv:
        write(demo())
        print("NOTE: synthetic demo data — do not commit static/data/visitors.json")
        return 0

    key = os.environ.get("GOATCOUNTER_API_KEY", "").strip()
    code = os.environ.get("GOATCOUNTER_CODE", "").strip() or config_code()
    base = os.environ.get("GOATCOUNTER_URL", "").strip() or (
        "https://%s.goatcounter.com" % code if code else "")
    if not key or not base:
        print("GoatCounter API key / site code not set — leaving statistics untouched")
        return 0
    try:
        api = GoatCounter(base, key)
        if "--archive" in sys.argv:
            archive_months(api)
        else:
            write(fetch(api))
    except (urllib.error.URLError, ValueError, KeyError, TypeError) as err:
        # never print the request (it carries the key) — only the error class/message
        print("fetching statistics failed: %s: %s" % (type(err).__name__, err))
        if "--archive" in sys.argv:
            return 1                      # let the archive job show as failed
        keep_published_copy()
    return 0


if __name__ == "__main__":
    sys.exit(main())

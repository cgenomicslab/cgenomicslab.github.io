#!/usr/bin/env python3
"""Fetch aggregated visitor statistics from Umami -> static/data/visitors.json

Runs in the GitHub Actions build (see .github/workflows/jekyll.yml), so the API
key never reaches the browser: the public page only reads the aggregated JSON.

Environment:
    UMAMI_API_KEY      API key (repository secret)                 [required]
    UMAMI_WEBSITE_ID   website id; default: umami.website_id in _config.yml
    UMAMI_API_URL      default https://api.umami.is/v1 (Umami Cloud);
                       for a self-hosted instance use https://<host>/api

Usage:
    python3 scripts/fetch_stats.py            # fetch real data
    python3 scripts/fetch_stats.py --demo     # synthetic data, for local preview only

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
LIVE_COPY = "https://cgenomicslab.org/static/data/visitors.json"

TIMEZONE = "Europe/Athens"
MAX_COUNTRIES = 60        # countries listed per range
MAX_CITY_COUNTRIES = 30   # countries that get a city breakdown
MAX_CITIES = 15           # cities per country
MAX_ROWS = 10             # pages / referrers / browsers / ...
MIN_CITY_VISITORS = 1     # raise to hide cities with very few visitors
PAUSE = 0.35              # seconds between calls (limit: 50 calls / 15 s)

RANGES = [                # key, label, days back (None = since tracking began), unit
    ("30d", "Last 30 days", 30, "day"),
    ("12m", "Last 12 months", 365, "month"),
    ("all", "All time", None, "month"),
]


def config_website_id():
    try:
        with open(os.path.join(ROOT, "_config.yml"), encoding="utf-8") as fh:
            m = re.search(r'^umami:\s*\n(?:[ \t]+.*\n)*?[ \t]+website_id:\s*"?([0-9a-fA-F-]*)"?',
                          fh.read(), re.M)
        return m.group(1) if m else ""
    except OSError:
        return ""


class Umami:
    def __init__(self, base, key, website):
        self.base = base.rstrip("/")
        self.key = key
        self.website = website

    def get(self, path, **params):
        url = "%s/websites/%s/%s?%s" % (
            self.base, self.website, path,
            urllib.parse.urlencode({k: v for k, v in params.items() if v is not None}))
        req = urllib.request.Request(url, headers={
            "Accept": "application/json",
            "Authorization": "Bearer " + self.key,
            "x-umami-api-key": self.key,
            "User-Agent": "cglab-site-stats/1.0",
        })
        time.sleep(PAUSE)
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)

    def metrics(self, kind, start, end, limit, **filters):
        rows = self.get("metrics", type=kind, startAt=start, endAt=end, limit=limit, **filters)
        rows = [{"name": str(r.get("x") or ""), "value": int(r.get("y") or 0)}
                for r in rows if isinstance(r, dict)]
        return [r for r in rows if r["value"] > 0][:limit]


def ms(d):
    return int(d.timestamp() * 1000)


def number(v):
    """Umami v2 returns {"value": n, "prev": m}; v3 returns n."""
    if isinstance(v, dict):
        v = v.get("value")
    return int(v or 0)


def fetch_range(api, start, end, unit):
    s, e = ms(start), ms(end)
    stats = api.get("stats", startAt=s, endAt=e)
    totals = {k: number(stats.get(k)) for k in ("visitors", "visits", "pageviews")}

    pv = api.get("pageviews", startAt=s, endAt=e, unit=unit, timezone=TIMEZONE)
    size = 10 if unit == "day" else 7
    views = {str(p["x"])[:size]: int(p["y"]) for p in pv.get("pageviews", [])}
    sessions = {str(p["x"])[:size]: int(p["y"]) for p in pv.get("sessions", [])}
    series = [{"t": t, "visitors": sessions.get(t, 0), "pageviews": views.get(t, 0)}
              for t in sorted(set(views) | set(sessions))]

    countries = []
    for i, row in enumerate(api.metrics("country", s, e, MAX_COUNTRIES)):
        code = row["name"].upper()
        if not re.fullmatch(r"[A-Z]{2}", code):
            continue
        entry = {"code": code, "visitors": row["value"], "cities": []}
        if i < MAX_CITY_COUNTRIES:
            cities = api.metrics("city", s, e, MAX_CITIES, country=code)
            entry["cities"] = [{"name": c["name"], "visitors": c["value"]} for c in cities
                               if c["name"] and c["value"] >= MIN_CITY_VISITORS]
        countries.append(entry)

    try:
        pages = api.metrics("path", s, e, MAX_ROWS)
    except urllib.error.HTTPError:          # Umami v2 calls this type "url"
        pages = api.metrics("url", s, e, MAX_ROWS)

    referrers = [r for r in api.metrics("referrer", s, e, MAX_ROWS + 5)
                 if r["name"] and "cgenomicslab.org" not in r["name"]][:MAX_ROWS]

    return {
        "totals": totals,
        "unit": unit,
        "series": series,
        "countries": countries,
        "pages": pages,
        "referrers": referrers,
        "browsers": api.metrics("browser", s, e, MAX_ROWS),
        "systems": api.metrics("os", s, e, MAX_ROWS),
        "devices": api.metrics("device", s, e, MAX_ROWS),
    }


def fetch(api):
    now = dt.datetime.now(dt.timezone.utc)
    first = None
    try:
        r = api.get("daterange")
        raw = r.get("startDate") or r.get("mindate")
        if raw:
            first = dt.datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
            if first.tzinfo is None:
                first = first.replace(tzinfo=dt.timezone.utc)
    except (urllib.error.URLError, ValueError, KeyError):
        pass
    first = first or now - dt.timedelta(days=365)

    out = {"generated": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
           "since": first.strftime("%Y-%m-%d"), "ranges": {}}
    for key, label, days, unit in RANGES:
        start = first if days is None else max(first, now - dt.timedelta(days=days))
        data = fetch_range(api, start, now, unit)
        data["label"] = label
        out["ranges"][key] = data
    return out


def demo():
    """Synthetic numbers so the page can be previewed before real data exists."""
    rnd = random.Random(7)
    places = {
        "GR": ["Heraklion", "Athens", "Thessaloniki", "Patras", "Chania", "Rethymno"],
        "US": ["New York", "Boston", "San Francisco", "Seattle", "Chicago"],
        "DE": ["Heidelberg", "Berlin", "Munich", "Cologne"],
        "ES": ["Barcelona", "Madrid", "Valencia"],
        "GB": ["London", "Cambridge", "Oxford", "Edinburgh"],
        "FR": ["Paris", "Lyon", "Bordeaux"],
        "CA": ["Vancouver", "Toronto", "Montreal"],
        "IT": ["Rome", "Milan", "Naples"],
        "NL": ["Amsterdam", "Utrecht"], "CH": ["Zurich", "Basel", "Lausanne"],
        "CN": ["Beijing", "Shanghai"], "JP": ["Tokyo", "Kyoto"], "IN": ["Bengaluru", "Delhi"],
        "TR": ["Istanbul", "Ankara"], "AU": ["Sydney", "Melbourne"], "BR": ["São Paulo"],
        "SE": ["Stockholm"], "CY": ["Nicosia"], "IL": ["Tel Aviv"], "SG": ["Singapore"],
        "ZA": ["Cape Town"], "AR": ["Buenos Aires"], "MX": ["Mexico City"], "AT": ["Vienna"],
    }
    weights = [400, 160, 120, 90, 80, 60, 55, 40, 35, 30, 28, 24, 22, 20, 18, 12, 10, 9,
               8, 7, 5, 4, 4, 3]
    now = dt.datetime.now(dt.timezone.utc)
    out = {"generated": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "demo": True,
           "since": (now - dt.timedelta(days=540)).strftime("%Y-%m-%d"), "ranges": {}}
    for (key, label, days, unit), scale in zip(RANGES, (1, 9, 13)):
        countries = []
        for (code, cities), w in zip(places.items(), weights):
            n = max(1, int(w * scale * rnd.uniform(0.8, 1.2)))
            share = sorted((rnd.random() ** 2 for _ in cities), reverse=True)
            rows = [{"name": c, "visitors": max(1, int(n * 0.8 * f / sum(share)))}
                    for c, f in zip(cities, share)]
            countries.append({"code": code, "visitors": n, "cities": rows})
        countries.sort(key=lambda c: -c["visitors"])
        visitors = sum(c["visitors"] for c in countries)
        steps = 30 if unit == "day" else (12 if key == "12m" else 18)
        series = []
        for i in range(steps):
            d = now - (dt.timedelta(days=steps - 1 - i) if unit == "day"
                       else dt.timedelta(days=30.4 * (steps - 1 - i)))
            v = max(1, int(visitors / steps * rnd.uniform(0.6, 1.4)))
            series.append({"t": d.strftime("%Y-%m-%d" if unit == "day" else "%Y-%m"),
                           "visitors": v, "pageviews": int(v * rnd.uniform(1.8, 2.6))})

        def rows(names, top):
            vals = sorted((int(top * rnd.uniform(0.2, 1) / (i + 1)) + 1
                           for i in range(len(names))), reverse=True)
            return [{"name": n, "value": v} for n, v in zip(names, vals)]

        out["ranges"][key] = {
            "label": label, "unit": unit, "series": series, "countries": countries,
            "totals": {"visitors": visitors, "visits": int(visitors * 1.3),
                       "pageviews": sum(p["pageviews"] for p in series)},
            "pages": rows(["/", "/research/", "/members/", "/join/", "/teaching/",
                           "/members/pittis/", "/publications/", "/contact/"], visitors),
            "referrers": rows(["google.com", "imbb.forth.gr", "scholar.google.com",
                               "github.com", "bsky.app", "linkedin.com"], visitors // 3),
            "browsers": rows(["chrome", "firefox", "safari", "edge"], visitors),
            "systems": rows(["Windows", "Mac OS", "Linux", "iOS", "Android"], visitors),
            "devices": rows(["desktop", "mobile", "laptop", "tablet"], visitors),
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

    key = os.environ.get("UMAMI_API_KEY", "").strip()
    website = os.environ.get("UMAMI_WEBSITE_ID", "").strip() or config_website_id()
    base = os.environ.get("UMAMI_API_URL", "").strip() or "https://api.umami.is/v1"
    if not key or not website:
        print("UMAMI_API_KEY / website id not set — leaving statistics untouched")
        return 0
    try:
        write(fetch(Umami(base, key, website)))
    except (urllib.error.URLError, ValueError, KeyError, TypeError) as err:
        # never print the request (it carries the key) — only the error class/message
        print("fetching statistics failed: %s: %s" % (type(err).__name__, err))
        keep_published_copy()
    return 0


if __name__ == "__main__":
    sys.exit(main())

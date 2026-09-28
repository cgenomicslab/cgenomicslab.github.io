#!/usr/bin/env python3
"""Build static/data/world.json — the base map for the Visitors page.

Run once (or when the map style changes); the output is committed.

    python3 scripts/build_worldmap.py

Downloads Natural Earth country shapes (public domain, via the world-atlas
package) and ISO 3166 codes, projects them with the Equal Earth projection and
writes, per country: ISO alpha-2 code, an SVG path and a bubble anchor point.
Shapes come from the 1:110m set (small file); anchor points from the 1:50m set
so that small countries (Malta, Singapore, ...) still get a bubble.
"""
import json
import math
import os
import sys
import urllib.request

ATLAS = "https://cdn.jsdelivr.net/npm/world-atlas@2.0.2/countries-%s.json"
ISO = ("https://raw.githubusercontent.com/lukes/"
       "ISO-3166-Countries-with-Regional-Codes/master/all/all.json")
OUT = os.path.join(os.path.dirname(__file__), "..", "static", "data", "world.json")

WIDTH = 1000.0
LAT_MIN, LAT_MAX = -58.0, 84.0      # crop Antarctica / empty Arctic
NO_ISO = {"Kosovo": "XK"}           # shapes without a numeric ISO id

A1, A2, A3, A4 = 1.340264, -0.081106, 0.000893, 0.003796
M = math.sqrt(3) / 2


def equal_earth(lon, lat):
    lam, phi = math.radians(lon), math.radians(lat)
    t = math.asin(M * math.sin(phi))
    t2 = t * t
    t6 = t2 * t2 * t2
    x = lam * math.cos(t) / (M * (A1 + 3 * A2 * t2 + t6 * (7 * A3 + 9 * A4 * t2)))
    y = t * (A1 + A2 * t2 + t6 * (A3 + A4 * t2))
    return x, y


X_MAX = equal_earth(180, 0)[0]
SCALE = WIDTH / (2 * X_MAX)
Y_TOP = equal_earth(0, LAT_MAX)[1]
HEIGHT = (Y_TOP - equal_earth(0, LAT_MIN)[1]) * SCALE


def project(lon, lat):
    lat = max(LAT_MIN, min(LAT_MAX, lat))
    x, y = equal_earth(lon, lat)
    return (x + X_MAX) * SCALE, (Y_TOP - y) * SCALE


def load(url, cache):
    if cache and os.path.exists(cache):
        with open(cache, encoding="utf-8") as fh:
            return json.load(fh)
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)


def decode(topo):
    """TopoJSON -> list of (id, name, [polygon, ...]); polygon = [ring, ...]."""
    sx, sy = topo["transform"]["scale"]
    tx, ty = topo["transform"]["translate"]
    arcs = []
    for arc in topo["arcs"]:
        x = y = 0
        pts = []
        for dx, dy in arc:
            x += dx
            y += dy
            pts.append((x * sx + tx, y * sy + ty))
        arcs.append(pts)

    def ring(idx):
        out = []
        for i in idx:
            pts = arcs[i] if i >= 0 else arcs[~i][::-1]
            out.extend(pts[1:] if out else pts)
        return out

    res = []
    for g in topo["objects"]["countries"]["geometries"]:
        if g["type"] == "Polygon":
            polys = [g["arcs"]]
        elif g["type"] == "MultiPolygon":
            polys = g["arcs"]
        else:
            continue
        res.append((g.get("id"), g["properties"]["name"],
                    [[ring(r) for r in p] for p in polys]))
    return res


def area_centroid(ring):
    a = cx = cy = 0.0
    for (x0, y0), (x1, y1) in zip(ring, ring[1:] + ring[:1]):
        f = x0 * y1 - x1 * y0
        a += f
        cx += (x0 + x1) * f
        cy += (y0 + y1) * f
    if abs(a) < 1e-12:
        return 0.0, ring[0]
    return abs(a) / 2, (cx / (3 * a), cy / (3 * a))


def main():
    cache = sys.argv[1] if len(sys.argv) > 1 else None   # optional dir with downloads
    c = lambda n: os.path.join(cache, n) if cache else None
    iso = {e["country-code"]: e["alpha-2"] for e in load(ISO, c("iso.json"))}
    code = lambda cid, name: iso.get(str(cid).zfill(3)) if cid else NO_ISO.get(name)

    countries = {}
    # anchor points: centroid of the largest polygon (so France sits in Europe)
    for cid, name, polys in decode(load(ATLAS % "50m", c("c50.json"))):
        a2 = code(cid, name)
        if not a2 or a2 == "AQ":
            continue
        best = max((area_centroid([project(*p) for p in poly[0]]) for poly in polys),
                   key=lambda t: t[0])
        countries[a2] = {"id": a2, "x": round(best[1][0], 1), "y": round(best[1][1], 1)}

    for cid, name, polys in decode(load(ATLAS % "110m", c("c110.json"))):
        a2 = code(cid, name)
        if a2 == "AQ" or name == "Antarctica":
            continue
        d = []
        for poly in polys:
            for r in poly:
                lons = [p[0] for p in r]
                if max(lons) - min(lons) > 300:     # ring wraps the antimeridian (Fiji)
                    continue
                pts = [project(*p) for p in r]
                d.append("M" + "L".join("%.1f,%.1f" % p for p in pts) + "Z")
        key = a2 or name
        countries.setdefault(key, {"id": a2 or "", "x": None, "y": None})["d"] = "".join(d)

    out = {
        "source": "Natural Earth (public domain) via world-atlas 2.0.2; Equal Earth projection",
        "width": int(WIDTH),
        "height": int(round(HEIGHT)),
        "countries": sorted(countries.values(), key=lambda e: e["id"]),
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, separators=(",", ":"), ensure_ascii=False)
    print("wrote %s: %d countries, %d with shapes, %.0f kB" % (
        os.path.normpath(OUT), len(countries),
        sum(1 for e in countries.values() if "d" in e), os.path.getsize(OUT) / 1000))


if __name__ == "__main__":
    main()

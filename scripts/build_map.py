#!/usr/bin/env python3
"""Rebuild the 69-wilaya map of Algeria from OpenStreetMap boundaries.

Pipeline
  1. fetch     download every wilaya (the `subarea` members of the Algeria relation)
               from the OSM API (cached in build/osm/, delete it to refresh)
  2. assemble  turn every relation into a polygon keyed by its `ref` (wilaya code)
  3. correct   make the 69 polygons a clean partition of the country:
                 - subtract every wilaya from the parent it was carved out of
                   (OSM sometimes adds the new relation without shrinking the parent)
                 - move the communes listed in MEMBERSHIP_FIXES to their legal wilaya
                 - give leftover overlaps to one side and fill interior gaps
  4. simplify  topology-preserving simplification with mapshaper, so neighbours
               keep sharing exactly the same border
  5. write     data/algeria-69-wilayas.geojson and map-algeria-69-wilayas.svg

Names and parent codes come from data/wilayas.csv; OSM only provides geometry.

Requirements: Python 3.10+, shapely>=2, pyproj, and Node.js (for `npx mapshaper`).
Usage:  python scripts/build_map.py
"""

import csv
import json
import math
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from pyproj import Transformer
from shapely import make_valid, set_precision
from shapely.geometry import LineString, MultiPolygon, Polygon, mapping, shape
from shapely.ops import polygonize, transform, unary_union

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
WILAYAS_CSV = ROOT / "data" / "wilayas.csv"
OUT_GEOJSON = ROOT / "data" / "algeria-69-wilayas.geojson"
OUT_SVG = ROOT / "map-algeria-69-wilayas.svg"

OSM_API = "https://api.openstreetmap.org/api/0.6"
COUNTRY_RELATION = 192756  # Algeria (admin_level=2); its `subarea` members are the wilayas
USER_AGENT = "algeria-69-wilayas-map-builder (https://github.com/chemsallioua/Algeria69WilayaMap)"

# Communes whose territory OSM draws inside the wrong wilaya. Membership is fixed
# by law (law 19-12 for the 2019 wilayas, law 26-06 of 4 April 2026 for all 69),
# so the commune outline decides the line: {OSM relation id of the commune: code}.
MEMBERSHIP_FIXES = {
    # Mansoura stayed in Ghardaïa when El Meniaa was created (law 19-12 gives El Meniaa
    # only El Meniaa, Hassi Gara and Hassi Fehal); OSM draws its whole daïra in El Meniaa.
    5117521: "47",
}

SIMPLIFY = "visvalingam weighted 8%"  # share of vertices kept by mapshaper
MIN_ISLAND = "0.5km2"                  # islets smaller than this are dropped
SVG_WIDTH = 10000                      # viewBox width; coordinates are rounded to integers
EQUAL_AREA = "ESRI:102022"             # Africa Albers Equal Area, used for reporting areas only


def osm_get(path, cache):
    """GET an OSM API resource as JSON, cached on disk."""
    if cache.exists():
        return json.loads(cache.read_text(encoding="utf-8"))
    for attempt in range(5):
        try:
            req = urllib.request.Request(f"{OSM_API}/{path}", headers={"User-Agent": USER_AGENT})
            body = urllib.request.urlopen(req, timeout=300).read().decode("utf-8")
            cache.write_text(body, encoding="utf-8")
            time.sleep(0.5)  # stay well within the OSM API usage policy
            return json.loads(body)
        except OSError as e:
            print(f"  {path}: {e}", file=sys.stderr)
            time.sleep(10 * (attempt + 1))
    sys.exit(f"Could not download {path} from the OSM API.")


def fetch():
    cache = BUILD / "osm"
    cache.mkdir(parents=True, exist_ok=True)
    country = osm_get(f"relation/{COUNTRY_RELATION}.json", cache / "country.json")
    ids = [m["ref"] for m in country["elements"][0]["members"] if m["role"] == "subarea"]
    wilayas = [osm_get(f"relation/{i}/full.json", cache / f"{i}.json") for i in ids]
    communes = [osm_get(f"relation/{i}/full.json", cache / f"commune-{i}.json")
                for i in MEMBERSHIP_FIXES]
    return wilayas, communes


def relation(data):
    """The relation a `relation/<id>/full` response was requested for: the one that is
    not itself a member (the response also lists sub-relations such as daïras)."""
    rels = [e for e in data["elements"] if e["type"] == "relation"]
    members = {m["ref"] for r in rels for m in r["members"] if m["type"] == "relation"}
    return next(r for r in rels if r["id"] not in members)


def relation_polygon(data):
    """Assemble a (multi)polygon from the outer/inner member ways of a relation."""
    nodes = {e["id"]: (e["lon"], e["lat"]) for e in data["elements"] if e["type"] == "node"}
    ways = {e["id"]: e["nodes"] for e in data["elements"] if e["type"] == "way"}
    rel = relation(data)

    def faces(*roles):
        lines = [LineString([nodes[n] for n in ways[m["ref"]]])
                 for m in rel["members"] if m["type"] == "way" and m["role"] in roles]
        return list(polygonize(unary_union(lines)))

    outer = unary_union(faces("outer", ""))
    inner = faces("inner")
    return make_valid(outer.difference(unary_union(inner)) if inner else outer)


def polygonal(geom):
    """Keep only the polygon parts of a geometry (set operations can leave lines/points)."""
    if isinstance(geom, (Polygon, MultiPolygon)):
        return geom
    return unary_union([g for g in getattr(geom, "geoms", []) if isinstance(g, (Polygon, MultiPolygon))])


def assemble(wilayas, meta):
    polys = {}
    for data in wilayas:
        ref = relation(data).get("tags", {}).get("ref", "")
        code = f"{int(ref):02d}" if ref.isdigit() else ref
        if code in meta:
            polys[code] = relation_polygon(data)
    missing = sorted(set(meta) - set(polys))
    if missing:
        sys.exit(f"OSM has no admin_level=4 relation for wilaya(s) {', '.join(missing)}")
    return polys


def km2(geom, to_ea=Transformer.from_crs(4326, EQUAL_AREA, always_xy=True).transform):
    return transform(to_ea, geom).area / 1e6


def correct(polys, meta, communes):
    # 1. A wilaya carved out of a parent must not stay inside that parent.
    for code, row in meta.items():
        parent = row["parent_code"]
        if parent and polys[parent].intersects(polys[code]):
            overlap = km2(polys[parent].intersection(polys[code]))
            if overlap > 1:
                print(f"  {code} {row['name_latin']}: removed {overlap:,.0f} km2 from parent {parent}")
            polys[parent] = polygonal(polys[parent].difference(polys[code]))

    # 2. Communes that OSM draws in the wrong wilaya.
    for data in communes:
        rel = relation(data)
        target = MEMBERSHIP_FIXES[rel["id"]]
        commune = relation_polygon(data)
        for code in polys:
            if code != target and polys[code].intersects(commune):
                moved = polys[code].intersection(commune)
                if km2(moved) > 1:
                    print(f"  commune {rel['tags'].get('name:fr', rel['tags'].get('name'))}: "
                          f"{km2(moved):,.0f} km2 moved from {code} to {target}")
                polys[code] = polygonal(polys[code].difference(commune))
                polys[target] = polygonal(polys[target].union(moved))

    # 3. Any other overlap goes to the wilaya with the lower code.
    codes = sorted(polys)
    for i, a in enumerate(codes):
        for b in codes[i + 1:]:
            if polys[a].intersects(polys[b]):
                overlap = polys[a].intersection(polys[b])
                if overlap.area > 0:
                    if km2(overlap) > 1:
                        print(f"  overlap {a}/{b}: {km2(overlap):,.1f} km2 kept in {a}")
                    polys[b] = polygonal(polys[b].difference(polys[a]))

    # 4. Interior gaps (slivers between relations) go to the neighbour sharing the longest edge.
    country = unary_union(list(polys.values()))
    gaps = [Polygon(r) for p in getattr(country, "geoms", [country]) for r in p.interiors]
    for gap in gaps:
        best = max(polys, key=lambda c: polys[c].boundary.intersection(gap.buffer(1e-7)).length)
        polys[best] = polygonal(polys[best].union(gap))
    if gaps:
        print(f"  filled {len(gaps)} interior gap(s), {sum(km2(g) for g in gaps):.2f} km2 in total")

    return {c: set_precision(make_valid(p), 1e-7) for c, p in polys.items()}


def simplify(polys, meta):
    """Topology-preserving simplification; returns GeoJSON features in lon/lat."""
    full = BUILD / "wilayas-full.geojson"
    simple = BUILD / "wilayas-simplified.geojson"
    features = [{"type": "Feature", "properties": {"code": c}, "geometry": mapping(polys[c])}
                for c in sorted(polys)]
    full.write_text(json.dumps({"type": "FeatureCollection", "features": features}), encoding="utf-8")
    if shutil.which("mapshaper"):
        mapshaper = [shutil.which("mapshaper")]
    elif shutil.which("npx"):
        mapshaper = [shutil.which("npx"), "--yes", "mapshaper"]
    else:
        sys.exit("Node.js is required for the simplification step (npx mapshaper).")
    subprocess.run([*mapshaper, "-i", str(full), "snap",
                    "-filter-islands", f"min-area={MIN_ISLAND}", "remove-empty",
                    "-simplify", *SIMPLIFY.split(), "keep-shapes",
                    "-clean", "-o", "format=geojson", "precision=0.0001", str(simple)], check=True)
    out = json.loads(simple.read_text(encoding="utf-8"))["features"]
    for f in out:
        f["properties"] = {"code": f["properties"]["code"], **{k: meta[f["properties"]["code"]][k]
                           for k in ("slug", "name_latin", "name_ar", "parent_code")}}
    return sorted(out, key=lambda f: f["properties"]["code"])


def write_geojson(features):
    fc = {"type": "FeatureCollection",
          "attribution": "© OpenStreetMap contributors, ODbL 1.0",
          "features": features}
    text = json.dumps(fc, ensure_ascii=False, separators=(",", ":"))
    OUT_GEOJSON.write_text(text.replace('{"type":"Feature",', '\n{"type":"Feature",') + "\n",
                           encoding="utf-8")


def mercator(lon, lat):
    return math.radians(lon), math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))


def write_svg(features):
    shapes = [shape(f["geometry"]) for f in features]
    west, south, east, north = unary_union(shapes).bounds
    left, bottom = mercator(west, south)
    right, top = mercator(east, north)
    scale = SVG_WIDTH / (right - left)
    height = round((top - bottom) * scale)

    def project(lon, lat):
        x, y = mercator(lon, lat)
        return round((x - left) * scale), round((top - y) * scale)

    def ring_path(coords):
        pts = [project(*c) for c in coords[:-1]]
        pts = [p for i, p in enumerate(pts) if i == 0 or p != pts[i - 1]]
        d = [f"M{pts[0][0]} {pts[0][1]}"]
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            d.append(f"{bx - ax} {by - ay}")
        return d[0] + "l" + " ".join(d[1:]).replace(" -", "-") + "z"

    def geom_path(g):
        parts = getattr(g, "geoms", [g])
        return "".join(ring_path(r.coords) for p in parts for r in (p.exterior, *p.interiors))

    lines = [
        f'<svg id="algeria-map-69-wilaya" data-name="algeria-map-69-wilaya" '
        f'xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SVG_WIDTH} {height}" '
        f'data-bbox="{west:.4f},{south:.4f},{east:.4f},{north:.4f}">',
        "<!-- Wilaya boundaries: © OpenStreetMap contributors, ODbL 1.0 "
        "(https://www.openstreetmap.org/copyright). Projection: Web Mercator. -->",
        "<defs><style>.cls-1{fill:#bcbec0;stroke:#fff;stroke-width:1px;"
        "stroke-linejoin:round;vector-effect:non-scaling-stroke;}</style></defs>",
        '<g id="wilayas">',
    ]
    for f, g in zip(features, shapes):
        p = f["properties"]
        lines.append(f'<path id="{p["code"]}" data-name="{p["slug"]}" '
                     f'data-name-latin="{p["name_latin"]}" data-name-ar="{p["name_ar"]}" '
                     f'class="cls-1" d="{geom_path(g)}"/>')
    lines += ["</g>", "</svg>"]
    OUT_SVG.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return west, south, east, north


def main():
    with WILAYAS_CSV.open(encoding="utf-8") as f:
        meta = {row["code"]: row for row in csv.DictReader(f)}
    print("fetching OSM boundaries")
    osm, communes = fetch()
    print("assembling polygons")
    polys = assemble(osm, meta)
    print("correcting")
    polys = correct(polys, meta, communes)
    print("simplifying")
    features = simplify(polys, meta)
    write_geojson(features)
    bbox = write_svg(features)
    print(f"wrote {OUT_GEOJSON.relative_to(ROOT)} and {OUT_SVG.relative_to(ROOT)}; "
          f"bbox W,S,E,N = {', '.join(f'{v:.4f}' for v in bbox)}")


if __name__ == "__main__":
    main()

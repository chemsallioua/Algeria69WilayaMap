# Technical Specifications

## Files

| File | Content | Size |
| --- | --- | --- |
| `map-algeria-69-wilayas.svg` | 69 wilaya paths, Web Mercator, ready to inline in a page | ~130 KB |
| `data/algeria-69-wilayas.geojson` | The same 69 polygons in longitude/latitude (WGS 84) | ~500 KB |
| `data/wilayas.csv` | Codes, slugs, Latin and Arabic names, parent wilaya | 3 KB |
| `scripts/build_map.py` | Rebuilds the SVG and GeoJSON from OpenStreetMap | |

## SVG

- **Format**: SVG 1.1, UTF-8 (Arabic names are stored as-is)
- **ViewBox**: `0 0 10000 9999`, integer coordinates (1 unit ≈ 200 m on the ground)
- **Projection**: Web Mercator (EPSG:3857), the projection of OpenStreetMap, Google Maps and Leaflet tiles
- **Extent**: longitude −8.6689 to 11.9973, latitude 18.9681 to 37.0883 (also stored in the root `data-bbox` attribute as `west,south,east,north`)
- **Elements**: 69 `<path>` elements, one per wilaya, in code order (01 to 69). Islets smaller than 0.5 km² are left out.

### Root Element

```xml
<svg id="algeria-map-69-wilaya"
     data-name="algeria-map-69-wilaya"
     xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 10000 9999"
     data-bbox="-8.6689,18.9681,11.9973,37.0883">
  <g id="wilayas">
    <path id="01" data-name="adrar-01" data-name-latin="Adrar" data-name-ar="أدرار" class="cls-1" d="…"/>
    …
  </g>
</svg>
```

### Path Attributes

- `id`: two-digit wilaya code (`"01"` to `"69"`)
- `data-name`: kebab-case name followed by the code (`"adrar-01"`, `"bou-saada-68"`)
- `data-name-latin`: Latin-script name (`"Adrar"`, `"Bou Saâda"`)
- `data-name-ar`: Arabic name (`"أدرار"`, `"بوسعادة"`)
- `class`: `"cls-1"`, styled by the embedded stylesheet (grey fill, 1px white border)
- `d`: the outline, drawn with absolute `M` and relative `l` commands; a wilaya with several parts (islands) has several subpaths

The ids start with a digit, so `#16` is not a valid CSS selector. Use `[id="16"]`, `CSS.escape('16')` or `document.getElementById('16')`.

Neighbouring wilayas share exactly the same border vertices, so the map has no gaps or overlaps.

## GeoJSON

- **Coordinates**: longitude/latitude (WGS 84), 4 decimal places (about 10 m)
- **Winding**: outer rings counter-clockwise, as in RFC 7946
- **Properties** of each feature:

```json
{ "code": "68", "slug": "bou-saada-68", "name_latin": "Bou Saâda", "name_ar": "بوسعادة", "parent_code": "28" }
```

`parent_code` is the wilaya a newer wilaya was carved from (empty for 01–48).

## Data Source and Corrections

The boundaries come from the OpenStreetMap `admin_level=4` relations of Algeria (the `subarea` members of relation [192756](https://www.openstreetmap.org/relation/192756)), retrieved on 2026-10-27. Two corrections make the 69 polygons follow the law:

1. **El Aricha (63)** was added to OSM without shrinking Tlemcen (13), so the two overlapped by 3,012 km². Every wilaya is now subtracted from the wilaya it was carved from.
2. **Mansoura** is a commune of Ghardaïa (47), but OSM draws its whole daïra inside El Meniaa (58). Its 4,786 km² were moved back to Ghardaïa, following the commune outline.

After correction, 1,538 of the 1,541 commune seats fall inside their own wilaya; the other three are coastal or border seats within 200 m of the line. The outlines are then simplified with [mapshaper](https://github.com/mbloch/mapshaper) (Visvalingam, 8% of the vertices kept) in a way that keeps shared borders identical.

## Rebuilding

```bash
pip install -r scripts/requirements.txt   # shapely, pyproj
npm install -g mapshaper                  # or let the script use npx
python scripts/build_map.py
```

The script downloads the relations from the OSM API into `build/` (delete that folder to refresh), applies the corrections, and rewrites the SVG and the GeoJSON. Names and numbers always come from `data/wilayas.csv`; OSM only provides the geometry.

## Browser Compatibility

The SVG works in all modern browsers (Chrome, Firefox, Safari, Edge, and mobile browsers). The border width uses `vector-effect: non-scaling-stroke`, so borders stay 1px thick at any zoom level.

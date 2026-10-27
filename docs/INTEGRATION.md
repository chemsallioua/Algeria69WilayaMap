# Integration with Mapping Libraries

The repository ships the same boundaries in two forms:

- `data/algeria-69-wilayas.geojson` for mapping libraries (longitude/latitude)
- `map-algeria-69-wilayas.svg` for plain web pages (Web Mercator, so it also lines up with web map tiles)

## Leaflet.js with GeoJSON

```javascript
const map = L.map('map').setView([28.0, 3.0], 5);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

fetch('data/algeria-69-wilayas.geojson')
    .then(response => response.json())
    .then(data => {
        L.geoJSON(data, {
            style: { color: '#fff', weight: 1, fillColor: '#2ecc71', fillOpacity: 0.5 },
            onEachFeature: (feature, layer) => {
                const p = feature.properties;
                layer.bindTooltip(`${p.name_latin} (${p.code}) – ${p.name_ar}`);
            }
        }).addTo(map);
    });
```

## Leaflet.js with the SVG

The SVG is drawn in Web Mercator and its root element stores its extent in `data-bbox` (`west,south,east,north`), so it can be laid over the tiles exactly:

```javascript
fetch('map-algeria-69-wilayas.svg')
    .then(response => response.text())
    .then(text => {
        const svg = new DOMParser().parseFromString(text, 'image/svg+xml').documentElement;
        const [west, south, east, north] = svg.dataset.bbox.split(',').map(Number);
        L.svgOverlay(svg, [[south, west], [north, east]], { interactive: true }).addTo(map);

        svg.addEventListener('click', event => {
            const path = event.target.closest('path');
            if (path) console.log(path.dataset.nameLatin, path.id);
        });
    });
```

## D3.js with the SVG

```javascript
d3.xml('map-algeria-69-wilayas.svg').then(data => {
    d3.select('#map-container')
        .node()
        .append(data.documentElement);

    d3.selectAll('#algeria-map-69-wilaya path')
        .on('click', function () {
            console.log(d3.select(this).attr('data-name-latin'));
        });
});
```

## D3.js with GeoJSON

The GeoJSON follows RFC 7946 (outer rings counter-clockwise). d3-geo expects the opposite winding, so reverse the rings once after loading:

```javascript
d3.json('data/algeria-69-wilayas.geojson').then(data => {
    for (const feature of data.features) {
        const polygons = feature.geometry.type === 'Polygon'
            ? [feature.geometry.coordinates]
            : feature.geometry.coordinates;
        polygons.forEach(rings => rings.forEach(ring => ring.reverse()));
    }

    const projection = d3.geoMercator().fitSize([800, 800], data);
    d3.select('#map-container')
        .append('svg')
        .attr('viewBox', '0 0 800 800')
        .selectAll('path')
        .data(data.features)
        .join('path')
        .attr('d', d3.geoPath(projection))
        .attr('fill', '#bcbec0')
        .attr('stroke', '#fff')
        .append('title')
        .text(d => `${d.properties.name_latin} (${d.properties.code})`);
});
```

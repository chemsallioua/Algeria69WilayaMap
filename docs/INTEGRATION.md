# Integration with Mapping Libraries

## Leaflet.js Integration

```javascript
// While this is an SVG, you can overlay it on Leaflet maps
const map = L.map('map').setView([28.0, 3.0], 5);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

// Add SVG overlay
const svgOverlay = L.svgOverlay(
    'map-algeria-69.svg',
    [[19, -8.67], [37, 12]]
).addTo(map);
```

## D3.js Integration

```javascript
d3.xml("map-algeria-69.svg").then(data => {
    d3.select("#map-container")
        .node()
        .append(data.documentElement);
    
    d3.selectAll("#algeria-map-69-wilaya path")
        .on("click", function() {
            const wilaya = d3.select(this);
            console.log(wilaya.attr("data-name-latin"));
        });
});
```

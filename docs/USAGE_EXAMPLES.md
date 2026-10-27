# Usage Examples

## Basic HTML Integration

To style and script the wilayas, the SVG has to be inline in the page. An `<img>` tag shows the map, but its paths can't be styled or clicked. You can paste the file's content into the page, or load it:

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        #algeria-map-69-wilaya {
            width: 100%;
            height: auto;
        }
        #algeria-map-69-wilaya path {
            fill: #bcbec0;
            stroke: #333;
            cursor: pointer;
            transition: fill 0.3s;
        }
        #algeria-map-69-wilaya path:hover {
            fill: #2ecc71;
        }
    </style>
</head>
<body>
    <div id="map-container"></div>
    <script>
        fetch('map-algeria-69-wilayas.svg')
            .then(response => response.text())
            .then(svg => {
                document.getElementById('map-container').innerHTML = svg;
            });
    </script>
</body>
</html>
```

`fetch` needs the page to be served over HTTP (for example `npx serve` or `python -m http.server`); it does not work from a `file://` URL.

## JavaScript Interaction

```javascript
// Get all wilaya paths
const wilayas = document.querySelectorAll('#algeria-map-69-wilaya path');

// Add click event to each wilaya
wilayas.forEach(wilaya => {
    wilaya.addEventListener('click', function() {
        const id = this.id;
        const name = this.getAttribute('data-name');
        const nameLatin = this.getAttribute('data-name-latin');
        const nameArabic = this.getAttribute('data-name-ar');

        console.log(`Clicked: ${nameLatin} (${nameArabic}) - ID: ${id}`);
    });
});

// Highlight specific wilaya by ID
function highlightWilaya(wilayaId) {
    const wilaya = document.getElementById(wilayaId);
    if (wilaya) {
        wilaya.style.fill = '#e74c3c';
    }
}

// Example: Highlight Algiers (16)
highlightWilaya('16');
```

The ids start with a digit, so in CSS and `querySelector` write `[id="16"]` instead of `#16`.

## React Component Example

```jsx
import React, { useEffect, useState } from 'react';

function InteractiveMap() {
    const [svg, setSvg] = useState('');
    const [selectedWilaya, setSelectedWilaya] = useState(null);

    useEffect(() => {
        fetch('/map-algeria-69-wilayas.svg')
            .then(response => response.text())
            .then(setSvg);
    }, []);

    const handleWilayaClick = (event) => {
        const path = event.target.closest('path');
        if (path) {
            setSelectedWilaya({
                id: path.id,
                name: path.dataset.name,
                nameLatin: path.dataset.nameLatin,
                nameArabic: path.dataset.nameAr
            });
        }
    };

    return (
        <div>
            <div onClick={handleWilayaClick} dangerouslySetInnerHTML={{ __html: svg }} />
            {selectedWilaya && (
                <div className="info-panel">
                    <h3>{selectedWilaya.nameLatin}</h3>
                    <p>{selectedWilaya.nameArabic}</p>
                    <p>Wilaya #{selectedWilaya.id}</p>
                </div>
            )}
        </div>
    );
}

export default InteractiveMap;
```

Put the SVG in your `public/` folder. If you import it as a component with SVGR instead, turn off SVGO's id cleanup (`cleanupIds`), or the `id` attributes will be renamed.

## Data Visualization Example

```javascript
// Color wilayas based on data (sample values)
const populationData = {
    '16': 3000000, // Alger
    '05': 1200000, // Batna
    // ... more data
};

function colorByPopulation(data) {
    Object.keys(data).forEach(wilayaId => {
        const wilaya = document.getElementById(wilayaId);
        const population = data[wilayaId];

        // Color gradient based on population
        const intensity = Math.min(population / 3000000, 1);
        const color = `rgba(231, 76, 60, ${intensity})`;

        wilaya.style.fill = color;
    });
}

colorByPopulation(populationData);
```

## Styling Recommendations

The SVG embeds a default style (grey fill, 1px white borders). Any rule in your page that targets `#algeria-map-69-wilaya path` overrides it.

### CSS Variables

```css
:root {
    --wilaya-default: #bcbec0;
    --wilaya-hover: #2ecc71;
    --wilaya-active: #e74c3c;
    --wilaya-border: #333333;
    --border-width: 1px;
}

#algeria-map-69-wilaya path {
    fill: var(--wilaya-default);
    stroke: var(--wilaya-border);
    stroke-width: var(--border-width);
    transition: fill 0.3s ease, stroke-width 0.3s ease;
}

#algeria-map-69-wilaya path:hover {
    fill: var(--wilaya-hover);
    stroke-width: 2px;
}

#algeria-map-69-wilaya path.selected {
    fill: var(--wilaya-active);
    stroke-width: 3px;
}
```

Borders use `vector-effect: non-scaling-stroke`, so `stroke-width` is in screen pixels whatever the size of the map.

### Responsive Design

```css
.map-container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
}

#algeria-map-69-wilaya {
    width: 100%;
    height: auto;
    display: block;
}

@media (max-width: 768px) {
    .map-container {
        padding: 10px;
    }
}
```

## Use Cases

- **Educational Platforms**: Interactive geography lessons about Algeria
- **Data Visualization**: Display statistics by wilaya (population, economy, etc.)
- **Travel Websites**: Regional information and navigation
- **Government Portals**: Administrative division information
- **News Media**: Regional news mapping and coverage
- **Business Analytics**: Regional market analysis and visualization
- **Research Projects**: Geographic and demographic studies

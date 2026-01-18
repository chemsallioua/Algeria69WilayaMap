# Usage Examples

## Basic HTML Integration

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        #algeria-map-69-wilaya {
            width: 100%;
            height: auto;
        }
        .cls-1 {
            fill: #bcbec0;
            stroke: #333;
            stroke-width: 2;
            cursor: pointer;
            transition: fill 0.3s;
        }
        .cls-1:hover {
            fill: #2ecc71;
        }
    </style>
</head>
<body>
    <div id="map-container">
        <!-- Include the SVG file here -->
    </div>
</body>
</html>
```

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

## React Component Example

```jsx
import React, { useState } from 'react';
import AlgeriaMap from './map-algeria-69.svg';

function InteractiveMap() {
    const [selectedWilaya, setSelectedWilaya] = useState(null);

    const handleWilayaClick = (event) => {
        const target = event.target;
        if (target.tagName === 'path') {
            setSelectedWilaya({
                id: target.id,
                name: target.getAttribute('data-name'),
                nameLatin: target.getAttribute('data-name-latin'),
                nameArabic: target.getAttribute('data-name-ar')
            });
        }
    };

    return (
        <div>
            <div onClick={handleWilayaClick}>
                <img src={AlgeriaMap} alt="Algeria Map" />
            </div>
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

## Data Visualization Example

```javascript
// Color wilayas based on data
const populationData = {
    '16': 3000000, // Algiers
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

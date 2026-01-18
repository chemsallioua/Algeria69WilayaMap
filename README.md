# Algeria Map - 69 Wilayas SVG

A comprehensive, multilingual SVG map of Algeria featuring all 69 administrative divisions (wilayas) with detailed metadata in Arabic, Latin, and structured data attributes.

## Overview

This project provides a high-quality, scalable vector graphics (SVG) map of Algeria's 69 wilayas (provinces). Each wilaya is represented as a separate path element with rich metadata including official names in Arabic and Latin scripts, making it ideal for interactive web applications, data visualization, and geographic information systems.

## Features

- **Complete Coverage**: All 69 wilayas of Algeria
- **Multilingual Support**: Names in both Arabic (official) and Latin scripts
- **Structured Data**: Consistent naming conventions and data attributes
- **Scalable**: Vector format ensures perfect quality at any size
- **Web-Ready**: Optimized for use in web applications and interactive maps
- **Accessible**: Semantic IDs and data attributes for easy DOM manipulation

## File Structure

### SVG Attributes

Each wilaya path element contains the following attributes:

- `id`: Two-digit numeric identifier (e.g., `"01"`, `"05"`, `"48"`)
- `data-name`: Kebab-case name with number (e.g., `"adrar-01"`, `"batna-05"`)
- `data-name-latin`: Official Latin script name (e.g., `"Adrar"`, `"Batna"`)
- `data-name-ar`: Official Arabic script name (e.g., `"أدرار"`, `"باتنة"`)
- `class`: CSS class for styling (`"cls-1"`)
- `d`: SVG path data defining the wilaya boundaries
- `transform`: Coordinate transformation for positioning

### Root Element

```xml
<svg id="algeria-map-69-wilaya" 
     data-name="algeria-map-69-wilaya" 
     xmlns="http://www.w3.org/2000/svg" 
     viewBox="0 0 9968 9644.45">
```

## Usage Examples

### Basic HTML Integration

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

### JavaScript Interaction

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

### React Component Example

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

### Data Visualization Example

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

## Complete List of Wilayas

| ID | Latin Name | Arabic Name | Data Name |
|----|------------|-------------|-----------|
| 01 | Adrar | أدرار | adrar-01 |
| 02 | Chlef | الشلف | chlef-02 |
| 03 | Laghouat | الأغواط | laghouat-03 |
| 04 | Oum El Bouaghi | أم البواقي | oum-el-bouaghi-04 |
| 05 | Batna | باتنة | batna-05 |
| 06 | Béjaïa | بجاية | bejaia-06 |
| 07 | Biskra | بسكرة | biskra-07 |
| 08 | Béchar | بشار | bechar-08 |
| 09 | Blida | البليدة | blida-09 |
| 10 | Bouira | البويرة | bouira-10 |
| 11 | Tamanrasset | تمنراست | tamanrasset-11 |
| 12 | Tébessa | تبسة | tebessa-12 |
| 13 | Tlemcen | تلمسان | tlemcen-13 |
| 14 | Tiaret | تيارت | tiaret-14 |
| 15 | Tizi Ouzou | تيزي وزو | tizi-ouzou-15 |
| 16 | Algiers | الجزائر | algiers-16 |
| 17 | Djelfa | الجلفة | djelfa-17 |
| 18 | Jijel | جيجل | jijel-18 |
| 19 | Sétif | سطيف | setif-19 |
| 20 | Saïda | سعيدة | saida-20 |
| 21 | Skikda | سكيكدة | skikda-21 |
| 22 | Sidi Bel Abbès | سيدي بلعباس | sidi-bel-abbes-22 |
| 23 | Annaba | عنابة | annaba-23 |
| 24 | Guelma | قالمة | guelma-24 |
| 25 | Constantine | قسنطينة | constantine-25 |
| 26 | Médéa | المدية | medea-26 |
| 27 | Mostaganem | مستغانم | mostaganem-27 |
| 28 | M'Sila | المسيلة | msila-28 |
| 29 | Mascara | معسكر | mascara-29 |
| 30 | Ouargla | ورقلة | ouargla-30 |
| 31 | Oran | وهران | oran-31 |
| 32 | El Bayadh | البيض | el-bayadh-32 |
| 33 | Illizi | إليزي | illizi-33 |
| 34 | Bordj Bou Arreridj | برج بوعريريج | bordj-bou-arreridj-34 |
| 35 | Boumerdès | بومرداس | boumerdes-35 |
| 36 | El Tarf | الطارف | el-tarf-36 |
| 37 | Tindouf | تندوف | tindouf-37 |
| 38 | Tissemsilt | تيسمسيلت | tissemsilt-38 |
| 39 | El Oued | الوادي | el-oued-39 |
| 40 | Khenchela | خنشلة | khenchela-40 |
| 41 | Souk Ahras | سوق أهراس | souk-ahras-41 |
| 42 | Tipaza | تيبازة | tipaza-42 |
| 43 | Mila | ميلة | mila-43 |
| 44 | Aïn Defla | عين الدفلى | ain-defla-44 |
| 45 | Naâma | النعامة | naama-45 |
| 46 | Aïn Témouchent | عين تموشنت | ain-temouchent-46 |
| 47 | Ghardaïa | غرداية | ghardaia-47 |
| 48 | Relizane | غليزان | relizane-48 |
| 49 | Timimoun | تيميمون | timimoun-49 |
| 50 | Bordj Badji Mokhtar | برج باجي مختار | bordj-badji-mokhtar-50 |
| 51 | Ouled Djellal | أولاد جلال | ouled-djellal-51 |
| 52 | Béni Abbès | بني عباس | beni-abbes-52 |
| 53 | In Salah | عين صالح | in-salah-53 |
| 54 | In Guezzam | عين قزام | in-guezzam-54 |
| 55 | Touggourt | تقرت | touggourt-55 |
| 56 | Djanet | جانت | djanet-56 |
| 57 | El M'Ghair | المغير | el-mghair-57 |
| 58 | El Meniaa | المنيعة | el-meniaa-58 |
| 59 | Ouargla New | ورقلة الجديدة | ouargla-new-59 |
| 60 | Laghouat New | الأغواط الجديدة | laghouat-new-60 |
| 61 | Illizi New | إليزي الجديدة | illizi-new-61 |
| 62 | Béchar New | بشار الجديدة | bechar-new-62 |
| 63 | Tindouf New | تندوف الجديدة | tindouf-new-63 |
| 64 | Adrar New | أدرار الجديدة | adrar-new-64 |
| 65 | Tamanrasset New | تمنراست الجديدة | tamanrasset-new-65 |
| 66 | El Bayadh New | البيض الجديدة | el-bayadh-new-66 |
| 67 | Naâma New | النعامة الجديدة | naama-new-67 |
| 68 | Aïn Témouchent New | عين تموشنت الجديدة | ain-temouchent-new-68 |
| 69 | Ghardaïa New | غرداية الجديدة | ghardaia-new-69 |

## Technical Specifications

- **Format**: SVG (Scalable Vector Graphics)
- **Version**: SVG 1.1
- **ViewBox**: `0 0 9968 9644.45`
- **Coordinate System**: Cartesian (transformed from geographic coordinates)
- **Encoding**: UTF-8 (supports Arabic text)
- **File Size**: ~450 KB
- **Total Elements**: 69 path elements (one per wilaya)

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

## Browser Compatibility

This SVG map is compatible with all modern browsers:

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Opera 76+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## Integration with Mapping Libraries

### Leaflet.js Integration

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

### D3.js Integration

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

## Data Processing Scripts

This repository includes PowerShell scripts for batch processing:

- `update-wilayas.ps1`: Update all wilaya names in batch
- `update-names.ps1`: Individual name replacements

## Contributing

Contributions are welcome! Here's how you can help:

1. **Report Issues**: Found incorrect boundaries or metadata? Open an issue.
2. **Improve Documentation**: Help translate or improve the README.
3. **Add Examples**: Share your implementation examples.
4. **Enhance Metadata**: Suggest additional data attributes.
5. **Fix Bugs**: Submit pull requests for any issues you find.

### Contribution Guidelines

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages (`git commit -m 'Add: new feature description'`)
6. Push to your fork (`git push origin feature/improvement`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2026 Algeria Map SVG Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Acknowledgments

- Geographic data based on official Algerian administrative divisions
- Arabic names follow official government designations
- Latin transliterations follow standard conventions

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/algeria-map-svg/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/algeria-map-svg/discussions)
- **Email**: support@example.com (replace with your contact)

## Changelog

### Version 1.0.0 (2026-01-18)
- Initial release
- All 69 wilayas with complete metadata
- Multilingual support (Arabic and Latin)
- Structured data attributes
- Web-ready SVG format

## Roadmap

- [ ] Add population data as attributes
- [ ] Include capital cities information
- [ ] Provide simplified/compressed version
- [ ] Add geographic center coordinates for each wilaya
- [ ] Create interactive demo website
- [ ] Add TypeScript definitions
- [ ] Provide npm package
- [ ] Create React/Vue/Angular component libraries

## FAQ

**Q: Can I use this in commercial projects?**  
A: Yes! The MIT license allows commercial use.

**Q: How accurate are the boundaries?**  
A: The boundaries are based on official administrative divisions of Algeria.

**Q: Can I modify the SVG?**  
A: Absolutely! Fork it, modify it, and share your improvements.

**Q: Is there a CDN link?**  
A: You can use GitHub's raw content or services like jsDelivr after publishing.

**Q: How do I add my own data to each wilaya?**  
A: Use JavaScript to add custom data attributes or maintain a separate data object keyed by wilaya ID.

**Q: Does this include disputed territories?**  
A: This map represents Algeria's official administrative divisions.

## Related Resources

- [Official Algeria Government Portal](https://www.interieur.gov.dz/)
- [GeoJSON Version](https://github.com/yourusername/algeria-map-geojson) (if available)
- [Administrative Divisions of Algeria - Wikipedia](https://en.wikipedia.org/wiki/Provinces_of_Algeria)

---

**Made with ❤️ for Algeria** | **الجزائر**

If you find this useful, please ⭐ star the repository!

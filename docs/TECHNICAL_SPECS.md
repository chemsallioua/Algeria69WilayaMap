# Technical Specifications

## Format Details

- **Format**: SVG (Scalable Vector Graphics)
- **Version**: SVG 1.1
- **ViewBox**: `0 0 9968 9644.45`
- **Coordinate System**: Cartesian (transformed from geographic coordinates)
- **Encoding**: UTF-8 (supports Arabic text)
- **File Size**: ~450 KB
- **Total Elements**: 69 path elements (one per wilaya)

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

## Browser Compatibility

This SVG map is compatible with all modern browsers:

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Opera 76+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## Data Processing Scripts

This repository includes PowerShell scripts for batch processing:

- `update-wilayas.ps1`: Update all wilaya names in batch
- `update-names.ps1`: Individual name replacements

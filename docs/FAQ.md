# FAQ

**Q: Can I use this in commercial projects?**  
A: Yes. The code and documentation are MIT. The boundary geometry comes from OpenStreetMap and is under the ODbL 1.0, which also allows commercial use: credit "© OpenStreetMap contributors", and share any modified boundary data under the same licence. See [DATA_LICENSE.md](../DATA_LICENSE.md).

**Q: How accurate are the boundaries?**  
A: They come from OpenStreetMap's wilaya boundaries, corrected so that every commune lies in the wilaya the law assigns it to (see [Technical Specifications](TECHNICAL_SPECS.md#data-source-and-corrections)). They are simplified for display, with a typical error of a few hundred metres. They are fine for maps and data visualisation, but not for legal or survey use.

**Q: Which numbering do the new wilayas use?**  
A: The official one: Law 26-06 of 4 April 2026 created wilayas 59 to 69, and Presidential Decree 26-206 numbered them in the order of the wilaya each was carved from (59 Aflou from Laghouat … 69 El Abiodh Sidi Cheikh from El Bayadh). Some maps published before the decree use a different order.

**Q: Can I modify the SVG?**  
A: Absolutely. For lasting changes, edit `data/wilayas.csv` or `scripts/build_map.py` and rebuild, so the SVG and the GeoJSON stay in sync.

**Q: Is there a CDN link?**  
A: Files on GitHub can be served through jsDelivr, for example `https://cdn.jsdelivr.net/gh/chemsallioua/Algeria69WilayaMap@main/map-algeria-69-wilayas.svg`.

**Q: How do I add my own data to each wilaya?**  
A: Keep a separate object keyed by wilaya code (the path `id`, or the `code` property in the GeoJSON), or add your own data attributes from JavaScript.

**Q: Does this include disputed territories?**  
A: This map represents Algeria's official administrative divisions.

## Related Resources

- [Official Algeria Government Portal](https://www.interieur.gov.dz/)
- [OpenStreetMap relation of Algeria](https://www.openstreetmap.org/relation/192756)
- [Administrative Divisions of Algeria - Wikipedia](https://en.wikipedia.org/wiki/Provinces_of_Algeria)

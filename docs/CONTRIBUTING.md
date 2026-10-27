# Contributing

Contributions are welcome! Here's how you can help:

1. **Report Issues**: Found incorrect boundaries or metadata? Open an issue.
2. **Improve Documentation**: Help translate or improve the README.
3. **Add Examples**: Share your implementation examples.
4. **Enhance Metadata**: Suggest additional data attributes.
5. **Fix Bugs**: Submit pull requests for any issues you find.

The SVG and the GeoJSON are generated, so don't edit them by hand. Names and codes live in `data/wilayas.csv`, boundary corrections in `scripts/build_map.py`; run `python scripts/build_map.py` after changing either (see [Technical Specifications](TECHNICAL_SPECS.md#rebuilding)). A wrong boundary is best fixed in OpenStreetMap itself, so the next rebuild picks it up.

## Contribution Guidelines

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages (`git commit -m 'Add: new feature description'`)
6. Push to your fork (`git push origin feature/improvement`)
7. Open a Pull Request

## Roadmap

- [x] Provide a GeoJSON version with real coordinates
- [ ] Add population data as attributes
- [ ] Include capital cities information
- [ ] Add geographic center coordinates for each wilaya
- [ ] Create interactive demo website
- [ ] Add TypeScript definitions
- [ ] Provide npm package
- [ ] Create React/Vue/Angular component libraries

## Changelog

### Version 2.0.0 (2026-10-27)

- Wilayas 59–69 now carry their real names and the official numbering of Decree 26-206 (they previously repeated the names of wilayas 49–58)
- Boundaries rebuilt from OpenStreetMap: accurate outlines, borders shared exactly between neighbours, no gaps or overlaps
- Corrected Tlemcen / El Aricha and Ghardaïa / El Meniaa (Mansoura) to match the law
- New `data/algeria-69-wilayas.geojson` (longitude/latitude) and `data/wilayas.csv`
- SVG is now in Web Mercator and records its extent in `data-bbox`, so it overlays web maps exactly
- SVG paths are in code order, have no `transform`, and the duplicate root id was removed
- Touggourt's Arabic name corrected to توقرت; El M'Ghair's slug is now `el-mghair-57`
- Build script (`scripts/build_map.py`) to regenerate everything

### Version 1.0.0 (2026-01-18)

- Initial release
- All 69 wilayas with complete metadata
- Multilingual support (Arabic and Latin)
- Structured data attributes
- Web-ready SVG format

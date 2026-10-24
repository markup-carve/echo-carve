# Changelog

## [0.1.0] - 2026-10-24

The first echo-carve release renders Carve sources to HTML from Echo through a Rust bridge.

### Improvements

- Render Carve source as HTML through `carve::to_html`, with invalid UTF-8 reported as status 2 (#4).
- Use command-line, module, and benchmark examples with the bridge (#4).
- Rendering follows the published carve-rs 0.1.11 engine (#11).

**Full Changelog**: https://github.com/markup-carve/echo-carve/compare/6155ff05152f52ebafc645255e34990f6c70fcd6...0.1.0

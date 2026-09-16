# Changelog

All notable changes to Carve for Echo are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and the project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Carve HTML rendering for Echo through a C ABI over `carve-rs`
- `carve::to_html` for Echo sources, with invalid UTF-8 reported as status 2
- Command-line, module and benchmark examples
- A corpus runner that renders every shared Carve fixture through the binding

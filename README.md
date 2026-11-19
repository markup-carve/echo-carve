# Carve for Echo

Carve 0.2 HTML rendering for the [Echo programming language](https://echoc.dev/),
backed by the unreleased `carve-lang` engine on the `carve-rs` `next2` branch through
a small C ABI. The dependency is pinned to a commit, not a registry release.

The Echo API is `carve::try_to_html` or `carve::to_html`. It uses Carve 0.2
defaults: raw HTML is escaped and unsafe URL schemes are denied. The binding
does not expose render options. Malformed UTF-8 source bytes become replacement
characters, as required by the 0.2 source contract.

Build the native bridge first:

```sh
CARGO_TARGET_DIR=native/target \
  cargo build --release --locked --manifest-path native/Cargo.toml
```

Then build and run the Echo example. Echo requires `clang` for its final link:

```sh
cd examples
echoc build --release --target render -o render
LD_LIBRARY_PATH=../native/target/release ./render # Linux
# DYLD_LIBRARY_PATH=../native/target/release ./render # macOS
```

Use it from Echo:

```echo
string $html = carve::to_html($source);
```

For the backend choice, API contract, validation, and measurements, see
[Design](docs/design.md), [Testing](docs/testing.md), and
[Performance](docs/performance.md).

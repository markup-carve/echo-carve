# Carve for Echo

Carve HTML rendering for the [Echo programming language](https://echoc.dev/),
backed by the conforming `carve-rs` engine through a small C ABI.

Build the native bridge first:

```sh
CARGO_TARGET_DIR=native/target \
  cargo build --release --manifest-path native/Cargo.toml
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

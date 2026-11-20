# Testing

The 0.2 bridge pins the `carve-lang` crate (library `carve`) from a commit on the `carve-rs` `next2`
branch. Cargo resolves that Git dependency and records it in `native/Cargo.lock`.
Build and test the native boundary with four workers:

```sh
export CARGO_BUILD_JOBS=4
CARGO_TARGET_DIR=native/target cargo test --locked --manifest-path native/Cargo.toml
CARGO_TARGET_DIR=native/target cargo build --release --locked --manifest-path native/Cargo.toml
```

Build the Echo command-line example with Echo 0.16 or newer:

```sh
cd examples
echoc build --release --target echo-carve -o echo-carve
cd ..
```

The integration check reads verified default-option HTML examples from the
pinned Rust engine's `spec-conformance/examples.json`. Check out that exact
commit and run the examples through the Echo executable:

```sh
git clone --branch next2 https://github.com/markup-carve/carve-rs.git engine
git -C engine checkout 8388a5a4f77452174ad04d9ee99f03a35244a960
CARGO_TARGET_DIR=native/target python3 test_corpus.py engine/spec-conformance/examples.json
```

The runner also checks that malformed UTF-8 bytes render with a replacement
character. Native unit tests check buffer ownership, the empty input, null
pointers, and the secure raw HTML default. CI runs these checks for pull
requests to `next2`.

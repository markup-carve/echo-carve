# Testing

Build and test the native boundary:

```sh
CARGO_TARGET_DIR=native/target \
  cargo test --locked --manifest-path native/Cargo.toml
```

Build the Echo command-line example:

```sh
cd examples
echoc build --release --target carve-echo -o carve-echo
```

Compare it with the shared Carve HTML corpus from the repository root:

```sh
python3 test_corpus.py /path/to/carve/tests/corpus
```

The runner checks every `.crv`/`.html` pair and verifies that invalid UTF-8 is
reported as status 2. At the pinned Carve revision, all 1,695 fixtures pass.

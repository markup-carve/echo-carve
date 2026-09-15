# Testing

Build and test the native boundary:

```sh
CARGO_TARGET_DIR=native/target \
  cargo test --locked --manifest-path native/Cargo.toml
CARGO_TARGET_DIR=native/target \
  cargo build --release --locked --manifest-path native/Cargo.toml
```

Build the Echo command-line example:

```sh
cd examples
echoc build --release --target carve-echo -o carve-echo
cd ..
```

Compare it with the shared Carve HTML corpus from the repository root:

```sh
git -C /path/to/carve-rs checkout d512479
git -C /path/to/carve-rs submodule update --init tests/spec
python3 test_corpus.py /path/to/carve-rs/tests/spec/tests/corpus
```

The runner checks every `.crv`/`.html` pair and verifies that invalid UTF-8 is
reported as status 2. The reported 1,695 passing fixtures are from `carve-rs`
commit `d512479`, the revision pinned in `native/Cargo.toml`. Its `tests/spec`
submodule pins the Carve specification at commit `56d76d7`; another revision
may contain a different number of fixtures.

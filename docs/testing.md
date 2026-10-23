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
echoc build --release --target echo-carve -o echo-carve
cd ..
```

Compare it with the shared Carve HTML corpus from the repository root:

```sh
git -C /path/to/carve-rs checkout 0.1.11
git -C /path/to/carve-rs submodule update --init tests/spec
python3 test_corpus.py /path/to/carve-rs/tests/spec/tests/corpus
```

The runner checks every `.crv`/`.html` pair and verifies that invalid UTF-8 is
reported as status 2. The reported 2,508 passing fixtures are from `carve-rs`
0.1.11 (commit `da5518c`), the revision pinned in `native/Cargo.toml`. Its
`tests/spec` submodule pins the Carve specification at commit `7f080ef`; another
revision may contain a different number of fixtures.

CI runs exactly this, so the count above is the one the workflow prints rather
than a figure from one machine.

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
git -C /path/to/carve-rs checkout 68e75bda67e0f89d719243e2731cbb9d30b396bb
git -C /path/to/carve-rs submodule update --init tests/spec
python3 test_corpus.py /path/to/carve-rs/tests/spec/tests/corpus
```

The runner checks every `.crv`/`.html` pair and verifies that invalid UTF-8 is
reported as status 2. The reported 4,600 passing fixtures are from `carve-rs`
commit `68e75bda`, the revision pinned in `native/Cargo.toml`. Its `tests/spec`
submodule pins the Carve specification at commit `df07d99`; another
revision may contain a different number of fixtures.

Three more fixtures at that pin are ones `carve-rs` itself declares behind its
spec pin (markup-carve/carve-rs#4259). `KNOWN_BEHIND` in `test_corpus.py`
lists them; the runner fails if one of them starts passing, so the list
shrinks with the pin.

CI runs exactly this, so the count above is the one the workflow prints rather
than a figure from one machine.

# Performance

The fast-track binding delegates parsing and rendering to the same Rust engine
as `carve-rs`. Its additional work is one C call and one copy from the returned
Rust buffer into an owned Echo string.

## Measurement

The included Echo and Rust benchmarks each load
`182-openers-past-the-nesting-cap-are-one-paragraph.crv` from the Carve spec
corpus at commit `56d76d7` (the `tests/spec` submodule of `carve-rs` commit
`d512479`). That 2,032-byte nesting-stress fixture is loaded once and rendered
1,000 times. See [Testing](testing.md) for the submodule checkout commands.

Build both entry points:

```sh
CARGO_TARGET_DIR=native/target \
  cargo build --release --locked --manifest-path native/Cargo.toml \
  --bin benchmark
cd examples
echoc build --release --target benchmark-echo -o benchmark-echo
cd ..
```

Measure them from the repository root, replacing `$FIXTURE` with the fixture
path. `/usr/bin/time` is the GNU time binary used for the table:

```sh
LD_LIBRARY_PATH=native/target/release \
  /usr/bin/time -f '%e s, %M KiB' examples/benchmark-echo "$FIXTURE"
/usr/bin/time -f '%e s, %M KiB' native/target/release/benchmark "$FIXTURE"
```

The table reports medians from twelve alternating runs of each command to
reduce ordering and temperature effects.

Test machine:

- AMD Ryzen 9 PRO 7940HS
- Linux x86-64
- Echo 0.3.14, release build
- Rust 1.97.1, release build with thin LTO and one codegen unit

| Entry point | Median | Peak RSS |
| --- | ---: | ---: |
| Echo binding | 1.21 s | 4.5 MiB |
| Direct Rust | 1.25 s | 4.2 MiB |

The medians do not show a meaningful slowdown at the Echo boundary. They are
not evidence that Echo is faster than Rust; no uncertainty estimate was
recorded for this exploratory measurement.

These numbers measure repeated in-process rendering. They do not measure cold
compilation, dynamic-library deployment, or a native parser written in Echo.

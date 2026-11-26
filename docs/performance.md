# Performance

The Echo binding calls `carve::api::render` from the pinned Carve 0.2 Rust
engine. Each call validates pointer and length arguments, passes source bytes to
the engine, catches Rust panics, and returns an owned HTML buffer. The Echo
wrapper copies that buffer into its own string and releases the Rust allocation.
The renderer uses `Options::default()`, including the secure raw HTML and URL
policy defaults.

The repository includes two benchmark entry points. The Echo program calls the
C ABI and copies the result. The Rust program calls the public 0.2 render API
directly. Both render the same input 1,000 times. This isolates the binding
cost; it is not a comparison of two parsers.

Build them with the pinned dependency:

```sh
export CARGO_BUILD_JOBS=4
CARGO_TARGET_DIR=native/target cargo build --release --locked --manifest-path native/Cargo.toml --bin benchmark
cd examples
echoc build --release --target echo-carve-benchmark -o echo-carve-benchmark
cd ..
```

Measure both programs on each input. `FIXTURE` is a Carve 0.2 source file:

```sh
LD_LIBRARY_PATH=native/target/release /usr/bin/time -f '%e s, %M KiB' examples/echo-carve-benchmark "$FIXTURE"
/usr/bin/time -f '%e s, %M KiB' native/target/release/benchmark "$FIXTURE"
```

The 0.1 measurements are not comparable to 0.2 because the engine and the
benchmark call changed together. The latest local 0.2 measurements are recorded
below after the three input sizes have been run.

## Local Carve 0.2 measurement

On 2026-11-19, with the pinned engine commit, Rust 1.99.1, Echo 0.16.0, and an
Intel Core i7-10750H, each program rendered generated paragraph source 1,000
times. The input sizes were 2,042, 8,180, and 32,754 bytes. The table shows
one wall-clock run per size. Other builds were active on the shared machine, so
these numbers are a functional scale check, not a stable binding-overhead
estimate. Both paths produced the same total HTML byte counts.

| Input size | Direct Rust | Echo binding | Total HTML bytes |
| --- | ---: | ---: | ---: |
| 2,042 bytes | 0.716 s | 0.418 s | 4,854,000 |
| 8,180 bytes | 2.211 s | 2.430 s | 19,362,000 |
| 32,754 bytes | 10.598 s | 11.427 s | 77,446,000 |

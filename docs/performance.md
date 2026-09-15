# Performance

The fast-track binding delegates parsing and rendering to the same Rust engine
as `carve-rs`. Its additional work is one C call and one copy from the returned
Rust buffer into an owned Echo string.

## Measurement

The included Echo and Rust benchmarks each load the same 2,032-byte Carve
nesting-stress fixture once and render it 1,000 times. Twelve runs were
interleaved to reduce ordering and temperature effects.

Test machine:

- AMD Ryzen 9 PRO 7940HS
- Linux x86-64
- Echo 0.3.14, release build
- Rust 1.97.1, release build with thin LTO and one codegen unit

| Entry point | Median | Peak RSS |
| --- | ---: | ---: |
| Echo binding | 1.21 s | 4.5 MiB |
| Direct Rust | 1.25 s | 4.2 MiB |

The timing difference is within normal run-to-run noise. The useful conclusion
is that the C boundary and output copy added no measurable overhead for this
workload, not that Echo is faster than Rust.

These numbers measure repeated in-process rendering. They do not measure cold
compilation, dynamic-library deployment, or a native parser written in Echo.

# Design

## Why the binding uses Rust

The implementation is a compatibility layer over `carve-rs`, not a
second Carve parser written directly in Echo. This was the shortest route to a
useful Echo API while retaining the behavior of a parser that already passes
the shared Carve corpus.

A native Echo parser would require rebuilding Carve's block parser, inline
parser, document-wide resolution, Unicode behavior, HTML renderer, and safety
limits. Echo can express that work, but its parser-oriented library ecosystem
is still young. Starting with the existing Rust engine separates two questions:

1. Can Echo call and safely consume a conforming Carve implementation?
2. Is replacing that engine with a native Echo implementation worthwhile?

The project answers the first question without preventing the second.
The public Echo namespace can remain stable if the backend changes later.

## Boundary

The native library exposes two C functions. One renders Carve source bytes to an
allocated UTF-8 HTML buffer; the other releases that buffer. Rust catches
unwinding panics before they cross the C boundary.

The bridge calls `carve::api::render` with `Options::default()`. The defaults
escape raw HTML and deny unsafe URL schemes. The 0.2 API replaces malformed
UTF-8 source bytes with replacement characters. It can refuse an input that
exceeds its profile limit. The Echo wrapper copies successful output into an
owned `string` and releases the Rust allocation immediately.

`carve::try_to_html` reports invalid pointers, invalid source input, engine
errors, and native panics as `result<string, carve::Error>`.
The C status codes are 1 for invalid pointers, 2 for rejected source input,
3 for a Rust panic, and 4 for another engine error. Status 2 no longer means
malformed UTF-8.
`carve::to_html` is the convenience form and terminates when that result is an
error.

The bridge exposes the HTML result of `render`. It does not expose the separate
`renderWithDiagnostics` call or configurable render options.

The Rust dependency is pinned to an exact `carve-rs` revision in
`native/Cargo.toml`. Updating the backend is therefore deliberate and
reviewable.

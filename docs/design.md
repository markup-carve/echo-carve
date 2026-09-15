# Design

## Why the first version uses Rust

The initial implementation is a compatibility layer over `carve-rs`, not a
second Carve parser written directly in Echo. This was the shortest route to a
useful Echo API while retaining the behavior of a parser that already passes
the shared Carve corpus.

A native Echo parser would require rebuilding Carve's block parser, inline
parser, document-wide resolution, Unicode behavior, HTML renderer, and safety
limits. Echo can express that work, but its parser-oriented library ecosystem
is still young. Starting with the existing Rust engine separates two questions:

1. Can Echo call and safely consume a conforming Carve implementation?
2. Is replacing that engine with a native Echo implementation worthwhile?

The current project answers the first question without preventing the second.
The public Echo namespace can remain stable if the backend changes later.

## Boundary

The native library exposes two C functions. One renders UTF-8 Carve bytes to an
allocated UTF-8 HTML buffer; the other releases that buffer. Rust catches
unwinding panics before they cross the C boundary.

The Echo wrapper copies successful output into an owned `string` and releases
the Rust allocation immediately. `carve::try_to_html` reports invalid pointers,
invalid UTF-8, and native panics as `result<string, carve::Error>`.
`carve::to_html` is the convenience form and terminates when that result is an
error.

The Rust dependency is pinned to an exact `carve-rs` revision in
`native/Cargo.toml`. Updating the backend is therefore deliberate and
reviewable.

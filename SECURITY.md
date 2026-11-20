# Security policy

## Supported versions

The released 0.1 line is maintained on `main`. The unreleased 0.2 port is on
`next2`.

## Reporting a vulnerability

Please use
[GitHub's private vulnerability reporting](https://github.com/markup-carve/echo-carve/security/advisories/new)
instead of opening a public issue. Include the affected version, a minimal
reproduction, the expected security boundary, and the observed behavior.

## Scope

This repository is a binding. Rendering, escaping, and the profile limits are
`carve-rs`'s, so a defect in rendered output usually belongs
[there](https://github.com/markup-carve/carve-rs/security/policy). Report it
here when the binding itself is at fault: the C ABI boundary in `native/src`,
its handling of lengths, ownership and malformed UTF-8 replacement, or the Echo
wrapper.

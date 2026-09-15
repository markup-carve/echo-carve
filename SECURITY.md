# Security policy

## Supported versions

Until the first tagged release, security fixes are applied to `main`.

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
its handling of lengths, ownership and invalid UTF-8, or the Echo wrapper.

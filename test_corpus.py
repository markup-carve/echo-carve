#!/usr/bin/env python3
"""Run the Echo binding against every shared Carve HTML fixture."""

from pathlib import Path
import os
import subprocess
import sys
import tempfile


# Fixtures the pinned carve-rs revision declares behind its own spec pin
# (`BEHIND_ON_PAIR` in its tests/corpus.rs). Each must still fail, so a pin
# that fixes one forces its entry out.
KNOWN_BEHIND = {
    "1063-a-block-shaped-line-inside-a-comment-run-keeps-the-item-tight": "markup-carve/carve-rs#4259",
    "1063-a-block-shaped-line-inside-a-comment-run-keeps-the-item-tight-2": "markup-carve/carve-rs#4259",
    "1063-a-block-shaped-line-inside-a-comment-run-keeps-the-item-tight-3": "markup-carve/carve-rs#4259",
}


binding = Path(__file__).resolve().parent
if len(sys.argv) != 2:
    sys.exit("usage: test_corpus.py /path/to/carve/tests/corpus")
corpus = Path(sys.argv[1]).resolve()
executable = binding / "examples" / "echo-carve"
library = binding / "native" / "target" / "release"

environment = os.environ.copy()
library_path_variable = (
    "DYLD_LIBRARY_PATH" if sys.platform == "darwin" else "LD_LIBRARY_PATH"
)
environment[library_path_variable] = os.pathsep.join(
    filter(None, [str(library), environment.get(library_path_variable)])
)

files = sorted(corpus.glob("*.crv"))
if not files:
    sys.exit(f"no Carve fixtures found under {corpus}")

failures = []
known_behind_seen = set()
for source in files:
    rendered = subprocess.run(
        [executable, source],
        capture_output=True,
        env=environment,
        check=False,
    )
    expected_path = source.with_suffix(".html")
    if not expected_path.exists():
        failures.append(f"{source.name}: expected HTML is missing")
        continue
    expected = expected_path.read_bytes()
    failed = rendered.returncode or rendered.stdout.rstrip() != expected.rstrip()
    if source.stem in KNOWN_BEHIND:
        known_behind_seen.add(source.stem)
        if not failed:
            failures.append(
                f"{source.name}: passes now; drop it from KNOWN_BEHIND"
                f" ({KNOWN_BEHIND[source.stem]})"
            )
        continue
    if failed:
        failures.append(
            f"{source.name}: Echo stderr={rendered.stderr.decode(errors='replace')!r}"
        )

failures += [
    f"{name}: KNOWN_BEHIND names a fixture the corpus does not hold"
    for name in sorted(set(KNOWN_BEHIND) - known_behind_seen)
]

if failures:
    print(f"{len(failures)} of {len(files)} fixtures failed", file=sys.stderr)
    print("\n".join(failures[:20]), file=sys.stderr)
    sys.exit(1)

with tempfile.NamedTemporaryFile() as invalid:
    invalid.write(b"\xff")
    invalid.flush()
    rejected = subprocess.run(
        [executable, invalid.name],
        capture_output=True,
        env=environment,
        check=False,
    )
    if rejected.returncode == 0 or b"status 2" not in rejected.stderr:
        sys.exit("Echo binding did not reject invalid UTF-8 with status 2")

print(
    f"Carve for Echo passed {len(files) - len(KNOWN_BEHIND)} HTML fixtures"
    f" ({len(KNOWN_BEHIND)} declared behind)"
)

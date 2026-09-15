#!/usr/bin/env python3
"""Run the Echo binding against every shared Carve HTML fixture."""

from pathlib import Path
import os
import subprocess
import sys
import tempfile


binding = Path(__file__).resolve().parent
if len(sys.argv) != 2:
    sys.exit("usage: test_corpus.py /path/to/carve/tests/corpus")
corpus = Path(sys.argv[1]).resolve()
executable = binding / "examples" / "carve-echo"
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
    if rendered.returncode or rendered.stdout.rstrip() != expected.rstrip():
        failures.append(
            f"{source.name}: Echo stderr={rendered.stderr.decode(errors='replace')!r}"
        )

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

print(f"Carve for Echo passed {len(files)} HTML fixtures")

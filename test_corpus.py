#!/usr/bin/env python3
"""Run the Echo binding against verified default-option Carve 0.2 examples."""

from pathlib import Path
import json
import os
import subprocess
import sys
import tempfile


binding = Path(__file__).resolve().parent
if len(sys.argv) != 2:
    sys.exit("usage: test_corpus.py /path/to/carve-rs/v2/spec-conformance/examples.json")
examples_path = Path(sys.argv[1]).resolve()
executable = binding / "examples" / "echo-carve"
library = Path(os.environ.get("CARGO_TARGET_DIR", binding / "native" / "target")) / "release"

environment = os.environ.copy()
library_path_variable = (
    "DYLD_LIBRARY_PATH" if sys.platform == "darwin" else "LD_LIBRARY_PATH"
)
environment[library_path_variable] = os.pathsep.join(
    filter(None, [str(library), environment.get(library_path_variable)])
)

examples = [
    example
    for example in json.loads(examples_path.read_text())["examples"]
    if example["kind"] == "render"
    and example["status"] == "verified"
    and example["options"] == {}
    and "html" in example["expected"]
]
if not examples:
    sys.exit(f"no verified default-option examples found in {examples_path}")

failures = []
with tempfile.NamedTemporaryFile() as source:
    for example in examples:
        source.seek(0)
        source.truncate()
        source.write(example["input"].encode())
        source.flush()
        rendered = subprocess.run(
            [executable, source.name],
            capture_output=True,
            env=environment,
            check=False,
        )
        expected = example["expected"]["html"].encode()
        if rendered.returncode or rendered.stdout != expected:
            failures.append(
                f"{example['id']}: Echo stderr={rendered.stderr.decode(errors='replace')!r}, "
                f"expected={expected[:120]!r}, got={rendered.stdout[:120]!r}"
            )

if failures:
    print(f"{len(failures)} of {len(examples)} examples failed", file=sys.stderr)
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
    if rejected.returncode or rejected.stdout != "<p>�</p>".encode():
        sys.exit("Echo binding did not replace malformed UTF-8 source bytes")

print(f"Carve for Echo passed {len(examples)} verified 0.2 HTML examples")

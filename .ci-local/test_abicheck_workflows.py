#!/usr/bin/env python3
"""Focused contracts for the PVXS ABICheck GitHub workflow."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
shadow = (ROOT / ".github/workflows/abicheck-shadow.yml").read_text()
baseline = (ROOT / ".github/workflows/abicheck-baseline.yml").read_text()
stager = (ROOT / ".github/workflows/abicheck-stage-installed.sh").read_text()

for name, text in {"shadow": shadow, "baseline": baseline}.items():
    assert "pull_request_target" not in text, name
    assert "permissions:\n  contents: read" in text, name
    assert "fb423dfd62c267b0db61739941f2d35ee2dacb16" in text, name

assert "git clean -ffdx" in shadow
assert "git checkout --detach" in shadow
assert "make -j\"$BUILD_JOBS\" install INSTALL_LOCATION=" in shadow
assert shadow.count("depth: headers") == 2
for library in ("libpvxs", "libpvxsIoc"):
    assert f"Compare {library}" in shadow
    assert f"lib/{library}.so" in shadow
assert "include/os/Linux" in shadow
assert "include/compiler/gcc" in shadow
assert shadow.count("pr-comment: false") == 2

assert "workflow_call:" in baseline
assert "workflow_dispatch:" in baseline
assert "Capture reusable baseline-set" in baseline
assert "depth: headers" in baseline
assert '"name":"libpvxs"' in baseline
assert '"name":"libpvxsIoc"' in baseline
assert "stage_binary\":true" in baseline
assert '"$install_root/lib"' in stager
assert "linux-*" in stager
assert "install_root/include" in stager

print("PVXS ABICheck workflow contracts: OK")

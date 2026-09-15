#!/usr/bin/env bash
# Normalize normal EPICS install output for ABICheck's stable Action inputs.
set -euo pipefail

install_root=$1
stage_root=$2
EPICS_BASE=${EPICS_BASE:-}
if [ -z "$EPICS_BASE" ] && [ -f configure/RELEASE.local ]; then
    EPICS_BASE=$(sed -n -E 's/^[[:space:]]*EPICS_BASE[[:space:]]*=[[:space:]]*//p' configure/RELEASE.local | tail -n 1)
fi
: "${EPICS_BASE:?cue.py prepare must provide EPICS_BASE}"

libdir=$(find "$install_root/lib" -mindepth 1 -maxdepth 1 -type d -name 'linux-*' -print -quit)
test -n "$libdir"
mkdir -p "$stage_root/lib" "$stage_root/epics"
cp -a "$install_root/include" "$stage_root/include"
ln -s "$(find "$libdir" -type f -name 'libpvxs.so.*' -print -quit)" "$stage_root/lib/libpvxs.so"
ln -s "$(find "$libdir" -type f -name 'libpvxsIoc.so.*' -print -quit)" "$stage_root/lib/libpvxsIoc.so"
cp -a "$EPICS_BASE/include" "$stage_root/epics/include"

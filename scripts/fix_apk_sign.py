#!/usr/bin/env python3
"""Manual fix for KernelSU-Next/kernel/apk_sign.c on this LOS kernel tree.

The only hunk of the upstream SUSFS patch for this file fails to apply (its
context expects EXPECTED_SIZE/EXPECTED_HASH, the pinned KernelSU-Next commit
has EXPECTED_NEXT_SIZE/EXPECTED_NEXT_HASH). apk_sign.h and throne_tracker.c DO
get renamed to ksu_is_manager_apk(), so the definition is left behind:
  ld.lld: error: undefined symbol: ksu_is_manager_apk

Fix: rename the definition only. The same hunk also accepts a second, third
party manager signature under CONFIG_KSU_SUSFS; that part is left out on
purpose, so only the official KernelSU-Next manager is trusted.
"""
p = "KernelSU-Next/kernel/apk_sign.c"
s = open(p).read()

old = "bool is_manager_apk(char *path)\n"
new = "bool ksu_is_manager_apk(char *path)\n"
assert s.count(old) == 1, "apk_sign.c: expected is_manager_apk definition not found, needs manual review"
open(p, "w").write(s.replace(old, new, 1))
print("apk_sign.c: OK (renamed is_manager_apk -> ksu_is_manager_apk)")

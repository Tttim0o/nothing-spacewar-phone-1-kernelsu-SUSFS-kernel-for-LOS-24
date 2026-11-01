#!/usr/bin/env python3
"""Manual fix for KernelSU-Next/kernel/core_hook.c on this LOS kernel tree.

The upstream SUSFS patch (10_enable_susfs_for_ksu.patch) adds a new
'bool is_zygote_child' declaration inside a CONFIG_KSU_SUSFS_SUS_MOUNT block
earlier in the same function, intending to also rename the ORIGINAL
'bool is_zygote_child = is_zygote(old->security);' declaration further down
to something else (via a separate hunk). On this tree that rename hunk fails
to apply (context drift), so both declarations survive in the same function
scope, causing:
  error: redefinition of 'is_zygote_child'

Fix: rename only the NEW (SUSFS-added) declaration + its one use to
'is_sus_zygote_child', leaving the original/unmodified code untouched.
"""
p = "KernelSU-Next/kernel/core_hook.c"
s = open(p).read()

old_decl = "bool is_zygote_child = susfs_is_sid_equal(old->security, susfs_zygote_sid);"
new_decl = "bool is_sus_zygote_child = susfs_is_sid_equal(old->security, susfs_zygote_sid);"
assert old_decl in s, "core_hook.c: expected SUSFS is_zygote_child declaration not found, needs manual review"
assert s.count(old_decl) == 1, "core_hook.c: SUSFS is_zygote_child declaration not unique"
s = s.replace(old_decl, new_decl, 1)

old_use = "if (likely(is_zygote_child)) {"
new_use = "if (likely(is_sus_zygote_child)) {"
assert old_use in s, "core_hook.c: expected SUSFS is_zygote_child usage not found, needs manual review"
assert s.count(old_use) == 1, "core_hook.c: SUSFS is_zygote_child usage not unique"
s = s.replace(old_use, new_use, 1)

open(p, "w").write(s)
print("core_hook.c: OK (renamed SUSFS-added is_zygote_child -> is_sus_zygote_child)")

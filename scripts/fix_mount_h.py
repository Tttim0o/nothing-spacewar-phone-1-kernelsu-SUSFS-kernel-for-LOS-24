#!/usr/bin/env python3
"""Manual fix for include/linux/mount.h on this LOS kernel tree.
The upstream SUSFS patch's hunk expects ANDROID_KABI_RESERVE(4) to be
immediately followed by '} __randomize_layout;', but this tree has an
extra 'void *data;' line in between, so the hunk's context doesn't match.
"""
p = "include/linux/mount.h"
s = open(p).read()
old = "\tANDROID_KABI_RESERVE(4);\n\tvoid *data;\n} __randomize_layout;"
new = (
    "#ifdef CONFIG_KSU_SUSFS\n"
    "\tANDROID_KABI_USE(4, u64 susfs_mnt_id_backup);\n"
    "#else\n"
    "\tANDROID_KABI_RESERVE(4);\n"
    "#endif\n"
    "\tvoid *data;\n} __randomize_layout;"
)
assert old in s, "mount.h: expected context not found, needs manual review"
open(p, "w").write(s.replace(old, new, 1))
print("mount.h: OK")

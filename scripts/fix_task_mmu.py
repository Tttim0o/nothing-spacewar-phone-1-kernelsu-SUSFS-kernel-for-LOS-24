#!/usr/bin/env python3
"""Manual fix for fs/proc/task_mmu.c on this LOS kernel tree.
The upstream SUSFS patch's hunk #1 expects '#include <linux/pkeys.h>' to be
immediately followed (within a few lines) by '#include <asm/elf.h>', but
this tree has two extra includes (mm_inline.h, ctype.h) in between, so the
hunk's context doesn't match. Hunks #2 and #3 of the same patch apply fine.
"""
p = "fs/proc/task_mmu.c"
s = open(p).read()
old = "#include <linux/pkeys.h>\n"
new = (
    old
    + "#ifdef CONFIG_KSU_SUSFS_SUS_KSTAT\n"
    + "#include <linux/susfs_def.h>\n"
    + "#endif\n"
)
assert old in s, "task_mmu.c: expected context not found, needs manual review"
open(p, "w").write(s.replace(old, new, 1))
print("task_mmu.c: OK")

#!/usr/bin/env python3
"""Manual fix for KernelSU-Next/kernel/core_hook.c on this LOS kernel tree.

Hunk #16 of the upstream SUSFS patch (10_enable_susfs_for_ksu.patch) fails to
apply here, because the pinned KernelSU-Next commit has extra try_umount()
calls ("/system_ext", "/system/etc/hosts") in the same block. Earlier hunks DO
apply, so the file ends up half converted:
  - the SUSFS-added 'bool is_zygote_child' survives next to the original one:
      error: redefinition of 'is_zygote_child'
  - is_zygote() / try_umount() were renamed to ksu_is_zygote() /
    ksu_try_umount(), but these callers were not, which -Wno-implicit-function-
    declaration hides until the final link (undefined symbol)
  - susfs_try_umount_all() is never called, so CONFIG_KSU_SUSFS_TRY_UMOUNT
    would silently do nothing

Fix: apply what hunk #16 intended, by hand. "/sbin" and "/system/etc/hosts" are
not in susfs_try_umount_all(), so they stay as explicit calls here to keep the
coverage the pinned commit has.
"""
p = "KernelSU-Next/kernel/core_hook.c"
s = open(p).read()

old_decl = "\tbool is_zygote_child = is_zygote(old->security);\n"
new_decl = (
    "#ifndef CONFIG_KSU_SUSFS_SUS_MOUNT\n"
    "\tbool is_zygote_child = ksu_is_zygote(old->security);\n"
    "#endif\n"
)
assert s.count(old_decl) == 1, "core_hook.c: expected is_zygote() declaration not found, needs manual review"
s = s.replace(old_decl, new_decl, 1)

old_block = (
    "\t// fixme: use `collect_mounts` and `iterate_mount` to iterate all mountpoint and\n"
    "\t// filter the mountpoint whose target is `/data/adb`\n"
    "\ttry_umount(\"/system\", true, 0);\n"
    "\ttry_umount(\"/system_ext\", true, 0);\n"
    "\ttry_umount(\"/vendor\", true, 0);\n"
    "\ttry_umount(\"/product\", true, 0);\n"
    "\ttry_umount(\"/data/adb/modules\", false, MNT_DETACH);\n"
    "\n"
    "\t// try umount ksu temp path\n"
    "\ttry_umount(\"/debug_ramdisk\", false, MNT_DETACH);\n"
    "\ttry_umount(\"/sbin\", false, MNT_DETACH);\n"
    "\t\n"
    "\t// try umount hosts file\n"
    "\ttry_umount(\"/system/etc/hosts\", false, MNT_DETACH);\n"
)
new_block = (
    "#ifdef CONFIG_KSU_SUSFS_TRY_UMOUNT\n"
    "\t// susfs come first, and lastly umount by ksu, make sure umount in reversed order\n"
    "\tsusfs_try_umount_all(new_uid.val);\n"
    "\tksu_try_umount(\"/sbin\", false, MNT_DETACH, new_uid.val);\n"
    "\tksu_try_umount(\"/system/etc/hosts\", false, MNT_DETACH, new_uid.val);\n"
    "#else\n"
    "\t// fixme: use `collect_mounts` and `iterate_mount` to iterate all mountpoint and\n"
    "\t// filter the mountpoint whose target is `/data/adb`\n"
    "\tksu_try_umount(\"/system\", true, 0);\n"
    "\tksu_try_umount(\"/system_ext\", true, 0);\n"
    "\tksu_try_umount(\"/vendor\", true, 0);\n"
    "\tksu_try_umount(\"/product\", true, 0);\n"
    "\tksu_try_umount(\"/data/adb/modules\", false, MNT_DETACH);\n"
    "\n"
    "\t// try umount ksu temp path\n"
    "\tksu_try_umount(\"/debug_ramdisk\", false, MNT_DETACH);\n"
    "\tksu_try_umount(\"/sbin\", false, MNT_DETACH);\n"
    "\t\n"
    "\t// try umount hosts file\n"
    "\tksu_try_umount(\"/system/etc/hosts\", false, MNT_DETACH);\n"
    "#endif\n"
)
assert s.count(old_block) == 1, "core_hook.c: expected try_umount() block not found, needs manual review"
s = s.replace(old_block, new_block, 1)

open(p, "w").write(s)
print("core_hook.c: OK (hunk #16 applied by hand: ksu_is_zygote, ksu_try_umount, susfs_try_umount_all)")

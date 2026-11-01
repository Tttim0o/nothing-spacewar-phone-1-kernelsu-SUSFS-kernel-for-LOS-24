#!/usr/bin/env python3
"""Fix LINUX_VERSION_CODE drift in KernelSU-Next/kernel/selinux/selinux.h.

Same root cause as the pkg_observer.c fixup: this vendor 5.4 kernel tree's
Makefile reports VERSION=5 PATCHLEVEL=4 (LINUX_VERSION_CODE < 5.10.0), but
its actual backported SELinux API already matches the >=5.10 shape:
- security/selinux/include/objsec.h already defines current_sid() itself
- the kernel already uses the selinux_state struct, not the raw
  selinux_enforcing / selinux_disabled globals

KernelSU-Next's selinux.h gates on LINUX_VERSION_CODE to decide which API
shape to use:
    #if (LINUX_VERSION_CODE >= KERNEL_VERSION(5, 10, 0)) || defined(KSU_COMPAT_HAS_SELINUX_STATE)
    #define KSU_COMPAT_USE_SELINUX_STATE
    #endif
On this tree that evaluates false, so selinux.c falls back to the old API
(raw selinux_enforcing, and its own current_sid() definition), causing:
    error: use of undeclared identifier 'selinux_enforcing'
    error: redefinition of 'current_sid'
      note: previous definition is here ../security/selinux/include/objsec.h:...

Fix: force both compat macros on, regardless of the (unreliable)
LINUX_VERSION_CODE check, since this tree already has the newer API.
"""
p = "KernelSU-Next/kernel/selinux/selinux.h"
s = open(p).read()

old = (
    "#if (LINUX_VERSION_CODE >= KERNEL_VERSION(5, 10, 0)) || defined(KSU_COMPAT_HAS_SELINUX_STATE)\n"
    "#define KSU_COMPAT_USE_SELINUX_STATE\n"
    "#endif\n"
)
new = (
    "/* Vynutene: tento vendor 5.4 strom ma uz novu selinux_state API a\n"
    " * vlastnu current_sid() v objsec.h, bez ohladu na (nespolahlivy)\n"
    " * LINUX_VERSION_CODE check (rovnaky root cause ako pkg_observer.c). */\n"
    "#define KSU_COMPAT_USE_SELINUX_STATE\n"
    "#define KSU_COMPAT_HAS_CURRENT_SID\n"
)
assert old in s, "selinux.h: expected LINUX_VERSION_CODE guard not found, needs manual review"
assert s.count(old) == 1, "selinux.h: guard not unique"
open(p, "w").write(s.replace(old, new, 1))
print("selinux.h: OK (forced KSU_COMPAT_USE_SELINUX_STATE + KSU_COMPAT_HAS_CURRENT_SID)")

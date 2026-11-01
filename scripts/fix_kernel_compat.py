#!/usr/bin/env python3
"""Fix LINUX_VERSION_CODE drift in KernelSU-Next/kernel/kernel_compat.c.

Same root cause as the pkg_observer.c and selinux.h fixups: this vendor tree
reports 5.4 but has mm/maccess.c backported from >=5.8, so
strncpy_from_unsafe_user() is gone and strncpy_from_user_nofault() replaced it.
The 5.3-5.7 branch of kernel_compat.c still calls the old name, which
-Wno-implicit-function-declaration hides until the final link:
    ld.lld: error: undefined symbol: strncpy_from_unsafe_user

Fix: call the function this tree really has.
"""
p = "KernelSU-Next/kernel/kernel_compat.c"
s = open(p).read()

old = "return strncpy_from_unsafe_user(dst, unsafe_addr, count);"
new = "return strncpy_from_user_nofault(dst, unsafe_addr, count);"
assert s.count(old) == 1, "kernel_compat.c: expected strncpy_from_unsafe_user call not found, needs manual review"
open(p, "w").write(s.replace(old, new, 1))
print("kernel_compat.c: OK (strncpy_from_unsafe_user -> strncpy_from_user_nofault)")

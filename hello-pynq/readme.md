# hello_pynq — Out-of-tree Kernel Module on PYNQ (Xilinx Linux)

This repo contains a minimal out-of-tree kernel module (`hello_pynq.ko`) and notes on how to compile and load it on a PYNQ board running:

- Kernel: `6.6.10-xilinx-v2024.1-g1594cb1cd9ce`
- Arch: `arm64` / `aarch64`
- Xilinx Vitis / PetaLinux style kernel tree packaged at:
  `/lib/modules/$(uname -r)/build`

Goal: Ensure kernel headers + generated headers exist and module `vermagic` matches kernel exactly.

---

## 0) Prerequisites

```bash
sudo apt-get update
sudo apt-get install -y build-essential bc bison flex libssl-dev libelf-dev
```

---

## 1) Kernel build tree (KDIR)

Verify kernel build tree exists:

```bash
ls -ld /lib/modules/$(uname -r)/build
```

---

## 2) Generate required headers

Run:

```bash
cd /lib/modules/$(uname -r)/build
sudo make modules_prepare
```

Verify generated headers exist:

```bash
ls arch/arm64/include/generated/asm/cpucaps.h
ls arch/arm64/include/generated/asm/sysreg-defs.h
ls include/generated/utsrelease.h
ls scripts/mod/modpost
```

If they exist, you can stop the make with Ctrl+C if warning spam appears.

---

## 3) Fix vermagic mismatch (“Invalid module format”)

If insmod prints:

```bash
version magic '6.6.10-xilinx-v2024.1' should be '6.6.10-xilinx-v2024.1-g1594cb1cd9ce'
```

Then `UTS_RELEASE` is wrong.

Fix it:

```bash
cd /lib/modules/$(uname -r)/build
echo "#define UTS_RELEASE \"$(uname -r)\"" | sudo tee include/generated/utsrelease.h
```

Verify:

```bash
cat include/generated/utsrelease.h
```

---

## 4) Build the module

```bash
make clean
make
```

Verify vermagic:

```bash
modinfo hello_pynq.ko | grep vermagic
uname -r
```

They must match.

---

## 5) Fix missing `<asm/types.h>` (optional)

If your module build fails with:

```bash
fatal error: asm/types.h: No such file or directory
```

Fix it:

```bash
cd /lib/modules/$(uname -r)/build

sudo mkdir -p include/uapi
sudo ln -snf ../../arch/arm64/include/generated/uapi/asm include/uapi/asm

sudo tee arch/arm64/include/generated/uapi/asm/types.h >/dev/null <<'EOF'
/* SPDX-License-Identifier: GPL-2.0 WITH Linux-syscall-note */
#ifndef _ASM_ARM64_TYPES_H
#define _ASM_ARM64_TYPES_H
#include <asm-generic/types.h>
#endif
EOF

ls include/uapi/asm/types.h
```

---


## 6) Load and unload the module

```bash
sudo insmod hello_pynq.ko
dmesg | tail -n 20

sudo rmmod hello_pynq
```

---

## 7) Optional: install for modprobe

```bash
sudo mkdir -p /lib/modules/$(uname -r)/extra
sudo cp hello_pynq.ko /lib/modules/$(uname -r)/extra/
sudo depmod -a

sudo modprobe hello_pynq
```

---

## Troubleshooting

### A) Missing cpucaps.h

```bash
sudo make modules_prepare
ls arch/arm64/include/generated/asm/cpucaps.h
```

### B) Missing asm/types.h

See section 5.

### C) UTS_RELEASE undeclared

Add in your module:

```c
#include <linux/utsrelease.h>
```

Or use:

```c
#include <linux/utsname.h>
pr_info("%s\n", utsname()->release);
```

---

## Notes

- Compiler mismatch warnings are harmless for simple modules.
- Xilinx kernel trees sometimes miss UAPI links or generated headers; this README includes known fixes.


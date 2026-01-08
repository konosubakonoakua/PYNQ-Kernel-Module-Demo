ifneq ($(KERNELRELEASE),)
# -------------------------------------------------------------------------
# Kbuild Phase: When the kernel build system parses this file, it ONLY 
# cares about what objects to build.
# -------------------------------------------------------------------------
obj-m += hello-pynq.o

else
# -------------------------------------------------------------------------
# Local Phase: When you type 'make' in the terminal, it runs this section.
# -------------------------------------------------------------------------
# Include common environment variables and checks
include ../Makefile.common

.PHONY: all clean install

# Ensure check_env runs before building
all: check_env
	$(MAKE) -C $(KDIR) M=$(PWD) ARCH=$(ARCH) CROSS_COMPILE=$(CROSS_COMPILE) modules

clean:
	$(MAKE) -C $(KDIR) M=$(PWD) ARCH=$(ARCH) clean

install: all
	@echo "[install] Installing to /lib/modules/$(UNAME_R)/extra/"
	@sudo mkdir -p /lib/modules/$(UNAME_R)/extra
	@sudo cp -f hello_pynq.ko /lib/modules/$(UNAME_R)/extra/
	@sudo depmod -a
	@echo "[install] Done. You can now: sudo modprobe hello_pynq"

endif

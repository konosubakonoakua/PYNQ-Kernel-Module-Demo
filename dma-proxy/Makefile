ifneq ($(KERNELRELEASE),)
# -------------------------------------------------------------------------
# Kbuild Phase
# -------------------------------------------------------------------------
obj-m := dma-proxy.o

else
# -------------------------------------------------------------------------
# Local Phase
# -------------------------------------------------------------------------
APP_NAME := dma-proxy-test

# Include common environment variables and checks
include ../Makefile.common

CC := $(CROSS_COMPILE)gcc
CFLAGS := -O3 -Wall

.PHONY: all module app clean install

# Ensure check_env is the first step for 'all'
all: check_env module app

module:
	$(MAKE) -C $(KDIR) M=$(PWD) ARCH=$(ARCH) CROSS_COMPILE=$(CROSS_COMPILE) modules

app: dma-proxy-test.c dma-proxy.h
	$(CC) $(CFLAGS) -o $(APP_NAME) dma-proxy-test.c -lpthread

clean:
	$(MAKE) -C $(KDIR) M=$(PWD) ARCH=$(ARCH) clean
	rm -f $(APP_NAME)

install: all
	@echo "[install] Installing module and app..."
	sudo mkdir -p /lib/modules/$(UNAME_R)/extra
	sudo cp -f dma-proxy.ko /lib/modules/$(UNAME_R)/extra/
	sudo cp -f $(APP_NAME) /usr/local/bin/
	sudo depmod -a
	@echo "[install] Done. Module: dma-proxy, App: $(APP_NAME)"

endif

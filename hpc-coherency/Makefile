# --- Configuration ---
# The name of your source file (without extension)
DTS_NAME = axi_dma_0_coherent
DTS_SRC = $(DTS_NAME).dts
DTBO_OUT = $(DTS_NAME).dtbo

# Paths
OVERLAY_BASE = /sys/kernel/config/device-tree/overlays
OVERLAY_NAME = dma_fix
TARGET_DIR = $(OVERLAY_BASE)/$(OVERLAY_NAME)
FIRMWARE_DIR = /lib/firmware

# --- Rules ---

.PHONY: all compile load unload status clean check_ident

all: compile

# 1. Compile the DTS to DTBO
compile: $(DTS_SRC)
	@echo "[MKL] Compiling $(DTS_SRC)..."
	dtc -@ -I dts -O dtb -o $(DTBO_OUT) $(DTS_SRC)

# 2. Load the Overlay into the kernel
load: compile
	@if [ -d $(TARGET_DIR) ]; then \
		echo "[MKL] Overlay $(OVERLAY_NAME) already exists. Unloading first..."; \
		sudo rmdir $(TARGET_DIR); \
	fi
	@echo "[MKL] Loading $(DTBO_OUT)..."
	sudo cp -f $(DTBO_OUT) $(FIRMWARE_DIR)/
	sudo mkdir -p $(TARGET_DIR)
	@echo "$(DTBO_OUT)" | sudo tee $(TARGET_DIR)/path > /dev/null
	@echo "[MKL] Load complete."
	@$(MAKE) status

# 3. Unload the Overlay
unload:
	@if [ -d $(TARGET_DIR) ]; then \
		echo "[MKL] Unloading $(OVERLAY_NAME)..."; \
		sudo rmdir $(TARGET_DIR); \
		echo "[MKL] Unload complete."; \
	else \
		echo "[MKL] Error: Overlay $(OVERLAY_NAME) is not loaded."; \
	fi

# 4. Check the status of the node in the live device tree
status:
	@echo "--- Device Tree Status ---"
	@find /proc/device-tree/axi -name "*a002*" -exec echo "Found Node: {}" \; || echo "Node not found."
	@if [ -f /proc/device-tree/axi/coherency_stub@a0020000/dma-coherent ]; then \
		echo "[SUCCESS] dma-coherent property is LIVE."; \
	else \
		echo "[WARNING] dma-coherent NOT found in live tree."; \
	fi
	@echo "--- udmabuf Status ---"
	@if [ -f /sys/class/u-dma-buf/udmabuf0/dma_coherent ]; then \
		printf "udmabuf0 dma_coherent: "; cat /sys/class/u-dma-buf/udmabuf0/dma_coherent; \
	fi

# 5. Clean generated files
clean:
	rm -f $(DTBO_OUT)

# 6. Quick check of APU Broadcast register
check_apu:
	@printf "APU_CONTROL (0xFF410040): "; sudo busybox devmem 0xff410040 32

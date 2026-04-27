# DMA Proxy Driver and Test Application

This repository contains a Linux character device driver (`dma-proxy.c`) and an associated user-space test application (`dma-proxy-test.c`) that act as a proxy for the Linux DMA Engine. It enables user-space applications to initiate and control DMA transfers (e.g., via Xilinx AXI DMA or AXI MCDMA) utilizing a zero-copy memory mapped interface.

## Repository Contents

* `dma-proxy.c`: The kernel space character device driver. It maps kernel-allocated DMA coherent memory to user space and provides `ioctl` commands to start and synchronize transfers.
* `dma-proxy-test.c`: A multi-threaded user-space application demonstrating how to interact with the driver. It spawns separate threads for RX and TX channels to operate simultaneously.
* `dma-proxy.h`: The shared header file defining the `channel_buffer` data structures, memory alignments, and `ioctl` definitions (`START_XFER`, `FINISH_XFER`, `XFER`).

## Hardware & System Requirements

* **Linux DMA Engine Support:** The underlying hardware must be supported by the standard Linux DMA Engine (e.g., Xilinx AXI DMA/MCDMA).
* **Hardware Coherency (Optional but Recommended):** For maximum performance, especially on MPSoC platforms, a hardware-coherent system is recommended. This requires:
    * AXI signals tied correctly for coherent transactions.
    * Connection to an HPC slave port (for Zynq MPSoC).
    * CCI initialized prior to Linux boot.
    * The `dma-coherent` property added to the device tree node.

## Device Tree Configuration

To use this driver, you must declare a proxy node in your device tree that maps to your physical DMA channels. The strings in `dma-names` dictate the `/dev/` node names created by the driver.

**Example 1: AXI DMA with TX and RX loopback**
```dts
dma_proxy {
    compatible ="xlnx,dma_proxy";
    dmas = <&axi_dma_1_loopback 0  &axi_dma_1_loopback 1>;
    dma-names = "dma_proxy_tx", "dma_proxy_rx";
    dma-coherent; /* Include if hardware is configured for coherency */
};
```

**Example 2: AXI MCDMA with multiple channels**
```dts
dma_proxy3 {
    compatible ="xlnx,dma_proxy";
    dmas = <&axi_mcdma_0 0  &axi_mcdma_0 16 &axi_mcdma_0 1 &axi_mcdma_0 17>;
    dma-names = "dma_proxy_tx_0", "dma_proxy_rx_0", "dma_proxy_tx_1", "dma_proxy_rx_1";
};
```

## Compilation

A `Makefile` is provided to build both the kernel module and the user-space application. It defaults to an `aarch64` cross-compilation environment. 

To build both:
```bash
make
```

To cross-compile against a specific kernel source tree:
```bash
make KDIR=/path/to/your/kernel/source CROSS_COMPILE=aarch64-linux-gnu- ARCH=arm64
```

## Usage

1. **Insert the Kernel Module:**
   ```bash
   insmod dma-proxy.ko
   ```
   *(Optional)* An internal self-test can be triggered on insertion to verify the driver without the user-space app:
   ```bash
   insmod dma-proxy.ko internal_test=1
   ```

2. **Verify Device Nodes:**
   Ensure the character devices have been created:
   ```bash
   ls -l /dev/dma_proxy*
   ```

3. **Run the Test Application:**
   The test application evaluates throughput and optionally verifies data integrity.
   
   **Syntax:**
   ```bash
   ./dma-proxy-test <# of transfers> <size of each transfer in KB> <optional verify: 0 or 1>
   ```
   
   **Example:** Run 1000 transfers of 32KB each, with data verification enabled:
   ```bash
   ./dma-proxy-test 1000 32 1
   ```

## Tuning Application Performance

* **Channel Counts:** Update `TX_CHANNEL_COUNT`, `RX_CHANNEL_COUNT`, `tx_channel_names`, and `rx_channel_names` inside `dma-proxy-test.c` to match your specific hardware configuration and device tree.
* **Compiler Optimization:** The application should always be compiled with `-O3` to prevent CPU bottlenecks from negatively skewing the measured DMA performance.

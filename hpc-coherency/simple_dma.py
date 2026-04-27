# simple_dma.py
import time

class SimpleDMADriver:
    def __init__(self, ip_obj, direction='tx', max_chunk_mib=4):
        self.mmio = ip_obj.mmio
        self.dir = direction.upper()
        self.max_chunk = max_chunk_mib * 1024 * 1024
        
        if direction.lower() == 'tx':
            self.base = 0x00
            self.v_l, self.v_h, self.v_len = 0x18, 0x1C, 0x28
        else:
            self.base = 0x30
            self.v_l, self.v_h, self.v_len = 0x48, 0x4C, 0x58

    def reset(self):
        cr = self.mmio.read(self.base)
        self.mmio.write(self.base, cr | 0x4)
        start = time.time()
        while self.mmio.read(self.base) & 0x4:
            if time.time() - start > 0.1: break
            time.sleep(0.001)

    def trigger_raw(self, phys_addr, size):
        self.mmio.write(self.base, 0x0001)
        self.mmio.write(self.v_l, phys_addr & 0xFFFFFFFF)
        self.mmio.write(self.v_h, (phys_addr >> 32) & 0xFFFFFFFF)
        self.mmio.write(self.v_len, int(size))

    def wait_for_completion(self, timeout=5.0):
        start = time.time()
        sr_addr = self.base + 0x04
        while True:
            sr = self.mmio.read(sr_addr)
            if (sr & 0x02): return True, hex(sr)
            if (sr & 0x70): return False, hex(sr)
            if (time.time() - start > timeout):
                return False, f"TIMEOUT (SR={hex(sr)})"
            time.sleep(0.0001)# simple_dma.py
import time

class SimpleDMADriver:
    def __init__(self, ip_obj, direction='tx', max_chunk_mib=4):
        self.mmio = ip_obj.mmio
        self.dir = direction.upper()
        self.max_chunk = max_chunk_mib * 1024 * 1024
        
        if direction.lower() == 'tx':
            self.base = 0x00
            self.v_l, self.v_h, self.v_len = 0x18, 0x1C, 0x28
        else:
            self.base = 0x30
            self.v_l, self.v_h, self.v_len = 0x48, 0x4C, 0x58

    def reset(self):
        cr = self.mmio.read(self.base)
        self.mmio.write(self.base, cr | 0x4)
        start = time.time()
        while self.mmio.read(self.base) & 0x4:
            if time.time() - start > 0.1: break
            time.sleep(0.001)

    def trigger_raw(self, phys_addr, size):
        self.mmio.write(self.base, 0x0001)
        self.mmio.write(self.v_l, phys_addr & 0xFFFFFFFF)
        self.mmio.write(self.v_h, (phys_addr >> 32) & 0xFFFFFFFF)
        self.mmio.write(self.v_len, int(size))

    def wait_for_completion(self, timeout=5.0):
        start = time.time()
        sr_addr = self.base + 0x04
        while True:
            sr = self.mmio.read(sr_addr)
            if (sr & 0x02): return True, hex(sr)
            if (sr & 0x70): return False, hex(sr)
            if (time.time() - start > timeout):
                return False, f"TIMEOUT (SR={hex(sr)})"
            time.sleep(0.0001)

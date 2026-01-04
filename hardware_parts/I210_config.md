# I210 Firmware Programming

### **1. Firmware Burning via External EEPROM Programmer**

Use an external EEPROM programmer (e.g., [Xgpro_T76](https://xgecu.myshopify.com/products/xgecu-t76-usb3-0-universal-programmer-support-eeprom-nor-nand-emmc-mcu-gal-minpro-tl866ii-t56-programmer-replacement-ic-tester)) to burn the file **`ZB25VQ16@SOIC8.BIN`** into the EEPROM.

---

### **2. Updating MAC Address via eeupdate64e**
Refer to: [https://blog.csdn.net/zhaoxinfan/article/details/111052084](https://blog.csdn.net/zhaoxinfan/article/details/111052084)

**Steps:**
1. Extract the downloaded package to obtain `eeupdate64e`.
2. Run the following command to view network card information:
   ```bash
   sudo ./eeupdate64e
   ```
3. Expected output (ignore `QV driver failed` warning if the target adapter is listed):
   ```
   Connection to QV driver failed - please reinstall it!

   Using: Intel (R) PRO Network Connections SDK v2.35.33
   EEUPDATE v5.35.33.04
   Copyright (C) 1995 - 2020 Intel Corporation
   Intel (R) Confidential and not for general distribution.

   Driverless Mode
   Warning: No Adapter Selected

   NIC Bus Dev Fun Vendor-Device  Branding string
   === === === === ============= =================================================
     1   1  00  00   8086-1536    Intel(R) I210 Gigabit Fiber Network Connection
   ```
4. If the adapter with **`8086-1536`** is detected (NIC index = 1), update its MAC address by running:
   ```bash
   sudo ./eeupdate64e /nic=1 /mac=6CB311950809
   ```
   Replace `6CB311950809` with your desired MAC address.

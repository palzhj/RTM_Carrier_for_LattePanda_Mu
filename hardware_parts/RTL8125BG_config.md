# RTL8125BG Initialization Config Notes on Ubuntu

## 1. Remove `r8169` (Required for modifying NVM/EFuse)

Ubuntu 24 automatically detects the RTL8125BG and loads the default
`r8169` driver. However, NVM/EFuse data must be modified using an external utility, so
first remove `r8169`:

``` bash
sudo rmmod r8169
```

------------------------------------------------------------------------

## 2. Download Realtek Programming Utility

Repository: [https://github.com/redchenjs/rtnicpg](https://github.com/redchenjs/rtnicpg)

Change pgdrv.c according to https://github.com/redchenjs/rtnicpg/issues/1, add the following code before the line ```LINUX_VERSION_CODE < KERNEL_VERSION(2,6,11)```.
``` bash
#if LINUX_VERSION_CODE >= KERNEL_VERSION(6,3,0)
    vm_flags_set(vma, VM_IO);
#else
    vma->vm_flags |= VM_IO;
#endif
```

------------------------------------------------------------------------

## 3. Build the Kernel Module

Compile to generate `pgdrv.ko`:

``` bash
make
sudo insmod pgdrv.ko
```

------------------------------------------------------------------------

## 4. Read Original EFuse Configuration

``` bash
sudo ./rtnicpg-x86_64 /r /efuse
```

Expected output for a fresh chip (all `FF`):

    *************************************************************************
    *       EEPROM/EFUSE/FLASH Programming Utility for                      *
    *    Realtek PCI(e) FE/GbE/2.5GbE Family Ethernet Controller            *
    *   Version : 2.76.0.3                                                  *
    * Copyright (C) 2022 Realtek Semiconductor Corp.. All Rights Reserved.  *
    *************************************************************************

     This is RTL8125BG
     Use EFuse
     Start to Dump and Parse EFuse Content
     FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF
     FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF

------------------------------------------------------------------------

## 5. Edit `8125BGEF.cfg`
8125BGEF.cfg (for efuse); 8125BG.cfg (for eeprom)

### 5.1 MAC Address

    NODEID = 00 E0 4C 68 00 04

### 5.2 LED Configuration

``` ini
; LED0 – Yellow – ACT
LED0CFG = 0E 00
; LED1 – Green – 2.5G/1G
LED1CFG = 0C 28
```

### 5.3 MDI / TX Polarity Swap

``` ini
MDISWAP   = 20
TXPOLSWAP = 50
```

------------------------------------------------------------------------

## 6. Write EFuse Configuration

``` bash
sudo ./rtnicpg-x86_64 /w /efuse
```

Example output:

    *************************************************************************
    *       EEPROM/EFUSE/FLASH Programming Utility for                      *
    *    Realtek PCI(e) FE/GbE/2.5GbE Family Ethernet Controller            *
    *   Version : 2.76.0.3                                                  *
    * Copyright (C) 2022 Realtek Semiconductor Corp.. All Rights Reserved.  *
    *************************************************************************

     This is RTL8125BG
     Use EFuse
     FB 00 00 E0 4C 68 00 00 F9 04 00 01 50 2C EC 10
     50 2E 23 01 F8 53 3C 00 F8 78 07 00 F8 F0 3F 00
     ...
     PG EFuse is Successful!!!
     NodeID = 00 E0 4C 68 00 01
     EFuse Remain 1224 Bytes!!!

------------------------------------------------------------------------

## 7. Remove Programming Driver and Reboot

After writing finishes:

``` bash
sudo rmmod pgdrv
sudo reboot
```

Ubuntu will automatically reload the default `r8169` driver after
reboot.

# Renaming the Downloader (FTDI EEPROM Programming)

## 1. Install `ftdi_eeprom` (Linux)
A utility for reading, erasing, and flashing EEPROMs on FTDI USB chips.

**Installation on Ubuntu:**
```bash
sudo apt install libftdi1 ftdi-eeprom
```

## 2. Create Configuration File
Create `jtag.conf` with the following content:

```ini
vendor_id=0x0403
product_id=0x6010

flash_raw=true

filename="example.bin"    # Specify binary file; leave empty to skip writing
```

You can change the VID and PID according to the output of ```lsusb```

## 3. Read Existing EEPROM Content
```bash
sudo ftdi_eeprom --read-eeprom jtag.conf
```

## 4. Generate Renamed Firmware
1. Open `sn_gen.py`
2. Update the `sn_bytes` variable with the new name
3. Save the file
4. Run the script:
```bash
sudo python3 sn_gen.py
```

## 5. Flash Firmware to EEPROM
```bash
sudo ftdi_eeprom --flash-eeprom jtag.conf
```

---

## Additional Information

### Xilinx Official Support
Xilinx has integrated a [built-in tool](https://docs.xilinx.com/r/en-US/ug908-vivado-programming-debugging/JTAG-Cables-and-Devices-Supported-by-hw_server) to convert FTDI devices (FT232H/FT2232H/FT4232H) into Vivado-supported programmers. As a result, this method is primarily for legacy or custom use cases.

### Reference Resources
- **FTDI EEPROM Dumps Repository**: [ftdi_dumps](https://github.com/dragonlock2/ftdi_dumps)
- **Original Source**: Based on [this gist](https://gist.github.com/rikka0w0/24b58b54473227502fa0334bbe75c3c1)

---

### Notes
- Ensure proper permissions when running commands with `sudo`
- Verify FTDI device connection before proceeding
- Backup original EEPROM content before modification
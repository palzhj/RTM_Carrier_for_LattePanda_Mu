#!/usr/bin/python
# This is info. print file
# author: zhj@ihep.ac.cn
# 2024-06-29 created
import sys

print("###########################################################");
print("This program modifies eeprom info of FTDI");

if len(sys.argv) >= 2:
  sn_bytes = str(sys.argv[1])[:13].encode()
  if len(sys.argv) > 2:
    file_name = str(sys.argv[2])
  else:
    file_name = "example.bin"
    print("Use default config file: example.bin")
else:
    sn_bytes = "JieZhang0000".encode()
    print("Use default SN: %s"%sn_bytes)
    file_name = "example.bin"
    print("Use default config file: %s"%file_name)

# print(sn_bytes)

try:
  with open(file_name, 'rb') as file:
    content = file.read()
    # print(content)
except FileNotFoundError:
    print('file NOT found!')
except PermissionError:
    print('No permission to access file!')
except Exception as e:
    print(f'Error:{e}')
file.close()

length = len(content)
if not length:
  raise ValueError('No data to checksum')
if length & 0x1:
  raise ValueError('Length not even')
if length!=256:
  raise ValueError('Length not 256')

serial_number_string_address = content[0x12]
serial_number_string_length = content[0x13]

AddressCounter = 2
old_serial_number_string_descriptor = b''
new_serial_number_string_descriptor = b''
while(AddressCounter < serial_number_string_length):
  old_serial_number_string_descriptor += bytes([content[serial_number_string_address + AddressCounter]])
  new_serial_number_string_descriptor += bytes([sn_bytes[int(AddressCounter/2-1)]]) + bytes([0])
  AddressCounter += 2
print("old sn:%s"%str(old_serial_number_string_descriptor))
print("new sn:%s"%str(sn_bytes))
# print("new sn:%s"%str(new_serial_number_string_descriptor))

new_content = content[:serial_number_string_address+2] + new_serial_number_string_descriptor + content[serial_number_string_address+serial_number_string_length:]
# print(new_content)

Checksum = 0xAAAA           # Variable for checksum value
AddressCounter = 0x00       # Variable for address counter
TempChecksum = 0x0000       # Used whilst calculating checksum
CheckSumLocation = 0x7F     # Address at which checksum stored in FT-X

# Calculation uses addresses from 0x00 up to 0x7E (checksum itself is located at 0x7F)
while(AddressCounter < CheckSumLocation):
  # Read the word from MTP and print it on the screen
  data = (new_content[AddressCounter*2+1]<<8 | new_content[AddressCounter*2]) & 0xFFFF
  # print("Memory location 0x%x is 0x%x"%(AddressCounter, data))

  # EXOR the data with the current checksum and then rotate one bit to the left
  TempChecksum = data ^ Checksum
  # print("0x%x"%TempChecksum)
  Checksum = ((TempChecksum << 1) | (TempChecksum >> 15)) & 0xFFFF
  # print("0x%x"%Checksum)

  #  Go to next word address.
  #  If we have reached word address 0x12, then skip forward to address 0x40
  AddressCounter = AddressCounter + 1
  # if(AddressCounter == 0x12):
  #   AddressCounter = 0x40
print("Checksum is 0x%x"%Checksum)

file_checksum = (new_content[AddressCounter*2+1]<<8 | new_content[AddressCounter*2]) & 0xFFFF
if (Checksum != file_checksum):
  new_new_content = new_content[:CheckSumLocation*2] + bytes([Checksum & 0xFF]) + bytes([(Checksum>>8) & 0xFF])
  # print(new_content)
  try:
    with open(file_name, 'wb') as file:
      file.write(new_new_content)
      print("File checksum updated")
  except FileNotFoundError:
      print('file NOT found!')
  except PermissionError:
      print('No permission to access file!')
  except Exception as e:
      print(f'Error:{e}')
  file.close()

# How to read WHEA_XPF_MCA

To Read a WHEA_XPF_MCA_SECTION, do the following:
- Split up the error packet of the section GUID to right before line `0x30`.
- Take the last 64 bits (In hex, 64 bits are: `35 01 0c 00 00 00 a0 ba` - as an example) - This is the MCI status
- All code are little-endian; I.e. read from right to left. Therefore (`35 01 0c 00 00 00 a0 ba` should be read as `ba a0 00 00 00 0c 01 35`)
- Run MCI status in the WHEA-Analysis-Tool - wheamceerror.py

An example of a WHEA_XPF_MCA_SECTION error record that's been analyzed till the MCI status:
```
04 00 00 00             - VersionNumber
02 00 00 00             - CpuVendor
73 10 5e 8c e5 18 dc 01 - Timestamp
06 00 00 00             - ProcessorNumber
00 00 00 00 00 00 00 00 - GlobalStatus
00 00 00 00 00 00 00 00 - InstructionPointer
00 00 00 00             - BankNumber
35 01 0c 00 00 00 a0 ba - MCI_STATUS - This is the important bit!

REM Remember, this is in little-endian so you read from right to left!
REM Therefore MCI is: ba a0 00 00 00 0c 01 35

REM We ignore the rest! They are uninportant for us for now
00 00 00 00 00 00 00 00 00 00 00 00 ff 0f 13 d0  - 0x30  - ............ÿ..Ð
0a 00 00 00 06 00 00 00 00 00 00 00 b0 00 10 00  - 0x40  - ............°...
...
```
# How to read WHEA_XPF_MCA

To Read a WHEA_XPF_MCA_SECTION, do the following:
- Split up the error packet of the section GUID to right before line `0x30`.
- Take the last 64 bits (In hex, 64 bits are: `35 01 0c 00 00 00 a0 ba` - as an example) - This is the MCI status
- All code are little-endian; I.e. read from right to left. Therefore (`35 01 0c 00 00 00 a0 ba` should be read as `ba a0 00 00 00 0c 01 35`)
- Run MCI status in the WHEA-Analysis-Tool - wheamceerror.py
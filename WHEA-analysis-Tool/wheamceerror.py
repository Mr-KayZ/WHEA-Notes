error = "INVALID"
tt = "N\\A"
ll = "N\\A"
rrrr = "N\\A"
cccc = "N\\A"
mmm = "N\\A"
pp = "N\\A"
ii = "N\\A"
t = "N\\A"

# bc800800060c0859

def print_error():
    print()
    print("Error: " + error)
    print()
    print("Transaction Type: " + tt)
    print("Memory/Cache Level: " + ll)
    print("Request Type: " + rrrr)
    if type == "1":
        print("Channel Number: " + cccc)
        print("Memory Transaction Type: " + mmm)
        print("Participant Type: " + pp)
        print("Memory or I/O?: " + ii)
        print("Timeout?: " + t)
    pause_input = input(". . .")
    exit()
    
def set_tt_amd(arg_tt):
    global tt
    if arg_tt == "00":
        tt = "Instruction"
    if arg_tt == "01":
        tt = "Data"
    if arg_tt == "10":
        tt = "Generic/Unknown"
    if arg_tt == "11":
        tt = "Reserved/Invalid"
        
def set_ll_amd(arg_ll):
    global ll
    if arg_ll == "00":
        ll = "L0: Core"
    if arg_ll == "01":
        ll = "Level 1"
    if arg_ll == "10":
        ll = "Level 2"
    if arg_ll == "11":
        ll = "Generic/Unknown"
        
def set_rrrr_amd(arg_rrrr):
    global rrrr
    if arg_rrrr == "0000":
        rrrr = "Generic/Unknown"
    if arg_rrrr == "0001":
        rrrr = "Generic Read"
    if arg_rrrr == "0010":
        rrrr = "Generic Write"
    if arg_rrrr == "0011":
        rrrr = "Data Read"
    if arg_rrrr == "0100":
        rrrr = "Data Write"
    if arg_rrrr == "0101":
        rrrr = "Instruction Fetch"
    if arg_rrrr == "0110":
        rrrr = "Prefetch"
    if arg_rrrr == "0111":
        rrrr = "Evict"
    if arg_rrrr == "1000":
        rrrr = "Snoop/Probe"
        
type = input("Does the Machine Check Exception stem from an Intel(1) or AMD(2) system?: ")
while(True):
    if type != "1" and type != "2":
        type = input("Please enter 1 for Intel or 2 for AMD: ")
    else:
        break
    

mci_status = input("Input the MCi_Status Register: ")

binary_mci = bin(int(mci_status, 16))[2:].zfill(64)
#print(binary_mci)

lower_mci = binary_mci[-16:]
upper_mci = binary_mci[0:16]

#print(lower_mci)
#print(upper_mci)

lower_one = lower_mci[0:4]
lower_two = lower_mci[4:8]
lower_three = lower_mci[8:12]
lower_four = lower_mci[12:16]

print("\nERROR CODE BITFIELD: " + lower_one + " " + lower_two + " " + lower_three + " " + lower_four)

if type == "1":
    if lower_one != "0000" and lower_one != "0001":
        print("WARNING: Invalid code")

    if lower_mci == "0000000000000000":
        print("ERROR CODE: No Error")
        exit()
    if lower_mci == "0000000000000001":
        print("ERROR CODE: This error has not been classified into the MCA error classes.")
        exit()
    if lower_mci == "0000000000000010":
        print("ERROR CODE: Parity error in internal microcode ROM")
        exit()
    if lower_mci == "0000000000000011":
        print("ERROR CODE: The BINIT# from another processor caused this processor to enter machine check.")
        exit()
    if lower_mci == "0000000000000100":
        print("ERROR CODE: FRC (functional redundancy check) main/secondary error.")
        exit()
    if lower_mci == "0000000000000101":
        print("ERROR CODE: Internal parity error.")
        exit()
    if lower_mci == "0000000000000110":
        print("ERROR CODE: An attempt was made by the SMM Handler to execute outside the ranges specified by SMRR")
        exit()
    if lower_mci == "0000010000000000":
        print("ERROR CODE: Internal timer error")
        exit()
    if lower_mci == "0000111000001011":
        print("ERROR CODE: Generic I/O error")
        exit()
    if lower_one == "0000" and lower_two[0:2] == "01":
        print("ERROR CODE: Internal unclassified error")
        exit()
        
    # COMPOUND ERROR CODES
    if lower_two == "0000" and lower_three == "0000":
        if lower_four[0:2] == "11":
            memory_level = ""
            if lower_four == "1100":
                memory_level = "Level 0"
            if lower_four == "1101":
                memory_level = "Level 1"
            if lower_four == "1110":
                memory_level = "Level 2"
            if lower_four == "1111":
                memory_level = "Generic"
            error = "Generic Cache Heirarchy Error"
            ll = memory_level
            # print("ERROR CODE: Generic Cache Heirarchy Error in Memory Level: " + memory_level)
            exit()
    if lower_two == "0000" and lower_three == "0001":
        if lower_four[0:2] == "00":
            tt = "Instruction"
        if lower_four[0:2] == "01":
            tt = "Data"
        if lower_four[0:2] == "10":
            tt = "Generic"
        if lower_four[2:4] == "00":
            ll = "Level 0"
        if lower_four[2:4] == "01":
            ll = "Level 1"
        if lower_four[2:4] == "10":
            ll = "Level 2"
        if lower_four[2:4] == "11":
            ll = "Generic"
        error = "TLB Error"
        # print("ERROR CODE: TLB Error during " + tt + " transaction in memory level: " + ll)
        print_error()
    if lower_two == "0000" and lower_three[0] == "1":

        if lower_four == "1111":
            cccc = "Channel not specified"
        else:
            cccc = lower_four
        if lower_three == "1000":
            mmm = "Generic undefined request"
        if lower_three == "1001":
            mmm = "Memory read"
        if lower_three == "1010":
            mmm = "Memory write"
        if lower_three == "1011":
            mmm = "Address/Command"
        if lower_three == "1100":
            mmm = "Memory scrubbing"
        error = "Memory Controller Error"
        # print("ERROR CODE: Memory Controller Error: " + mmm + " at channel level: " + cccc)
        print_error()
    if lower_two == "0001":
        if lower_four[0:2] == "00":
            tt = "Instruction"
        if lower_four[0:2] == "01":
            tt = "Data"
        if lower_four[0:2] == "10":
            tt = "Generic/Unknown"
        if lower_four[2:4] == "00":
            ll = "Level 0"
        if lower_four[2:4] == "01":
            ll = "Level 1"
        if lower_four[2:4] == "10":
            ll = "Level 2"
        if lower_four[2:4] == "11":
            ll = "Generic/Unknown"
        if lower_three == "0000":
            rrrr = "Generic Error"
        if lower_three == "0001":
            rrrr = "Generic Read"
        if lower_three == "0010":
            rrrr = "Generic Write"
        if lower_three == "0011":
            rrrr = "Data Read"
        if lower_three == "0100":
            rrrr = "Data Write"
        if lower_three == "0101":
            rrrr = "Instruction Fetch"
        if lower_three == "0110":
            rrrr = "Prefetch"
        if lower_three == "0111":
            rrrr = "Eviction"
        if lower_three == "1000":
            rrrr = "Snoop Error"
        error = "Cache Heirarchy Error"
        # print("ERROR CODE: Cache Heirarchy Error. Subtype: " + rrrr + " - " + tt + " at memory level: " + ll)
        print_error()
    if lower_two == "0010" and lower_three[0] == "1":
        if lower_four == "1111":
            cccc = "Channel not specified"
        else:
            cccc = lower_four
        if lower_three == "1000":
            mmm = "Generic undefined request"
        if lower_three == "1001":
            mmm = "Memory read error"
        if lower_three == "1010":
            mmm = "Memory write error"
        if lower_three == "1011":
            mmm = "Memory Scrubbing Error"
        error = "Extended Memory Error"
        # print("ERROR CODE: Extended Memory Error: " + mmm + " at channel level: " + cccc)
        print_error()
    if lower_two[0] == "1":
        if lower_three == "0000":
            rrrr = "Generic/Unknown"
        if lower_three == "0001":
            rrrr = "Generic Read"
        if lower_three == "0010":
            rrrr = "Generic Write"
        if lower_three == "0011":
            rrrr = "Data Read"
        if lower_three == "0100":
            rrrr = "Data Write"
        if lower_three == "0101":
            rrrr = "Instruction Fetch"
        if lower_three == "0110":
            rrrr = "Prefetch"
        if lower_three == "0111":
            rrrr = "Eviction"
        if lower_three == "1000":
            rrrr = "Snoop"
        if lower_four[2:4] == "00":
            ll = "Level 0"
        if lower_four[2:4] == "01":
            ll = "Level 1"
        if lower_four[2:4] == "10":
            ll = "Level 2"
        if lower_four[2:4] == "11":
            ll = "Generic"
        if lower_two[3] == "0":
            t = "No"
        else:
            t = "Yes"
        if lower_four[0:2] == "00":
            ii = "Memory Access"
        if lower_four[0:2] == "10":
            ii = "I/O"
        if lower_four[0:2] == "11":
            ii = "Other"
        if lower_two[1:3] == "00":
            pp = "Local Processor originated request"
        if lower_two[1:3] == "01":
            pp = "Local Processor originated request"
        if lower_two[1:3] == "10":
            pp = "Local processor observed error as third party"
        if lower_two[1:3] == "11":
            print(pp)
            pp = "Generic"
        error = "Bus and Interconnect Error"
        # print("ERROR CODE: Bus and Interconnect Error: " + pp + " - " + t + " Type: " + rrrr + " Subtype: " + ii + " on memory level " + ll)
        print_error()
        
if type == "2":
    if lower_one != "0000":
        print("WARNING: Invalid Code")
    if lower_two == "0000" and lower_one == "0001":
        error = "TLB Error"
        set_tt_amd(lower_four[0:2])
        set_ll_amd(lower_four[2:4])
        print_error()
    if lower_two == "0001":
        error = "Memory Error"
        set_rrrr_amd(lower_three)
        set_tt_amd(lower_four[0:2])
        set_ll_amd(lower_four[2:4])
        print_error()
    if lower_two[0] == "1":
        error = "Bus Error"
        if lower_two[3] == "0":
            t = "No"
        else:
            t = "Yes"
        set_rrrr_amd(lower_three)
        set_ll_amd(lower_four[2:4])
        print_error()
    if lower_two[0:2] == "01":
        error = "Unclassified Internal Error"
        print_error()
print_error()
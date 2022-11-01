import matplotlib.pyplot as plt
from platform import machine
import sys
MEM = ['0'*16]*256  # actual memory
PC = '0'*8  # initialised at 0
regs = {'000': 'R0', '001': 'R1', '010': 'R2', '011': 'R3',
        '100': 'R4', '101': 'R5', '110': 'R6', '111': 'FLAGS'}
# comR is the set of all registers. Have included lowercase versions too just to adjust for keys
comR = {'R0': '0000000000000000', 'R1': '0000000000000000', 'R2': '0000000000000000', 'R3': '0000000000000000', 'R4': '0000000000000000', 'R5': '0000000000000000', 'R6': '0000000000000000',
        'FLAGS': '0000000000000000'}
InsType = {'00000': 'A', '00001': 'A', '10000': 'A', '10001': 'A', '10110': 'A', '11010': 'A', '11011': 'A', '11100': 'A', '00010': 'B', '10010': 'B', '11001': 'B', '11000': 'B', '10011': 'C',
           '10111': 'C', '11101': 'C', '11110': 'C', '10100': 'D', '10101': 'D', '11111': 'E', '01100': 'E', '01101': 'E', '01110': 'E', '01010': 'F'}
Finstring = ''

#_____Additional_Functions_________#


def ftov(s):
    if s == 'Error':
        return 'Error'
    E = s[0:3]
    # print(E)

    M = s[3:-1]
    M = M+s[-1]
    Ed = 0
    for i in E:
        Ed = Ed*2+eval(i)

    Md = 1
    n = 1
    for i in M:
        Md = Md + eval(i)/2**n
        n += 1
    return 2**Ed * Md


def vtob(V):

    n = abs(V)
    b = 0
    p = 0
    n1 = n//1
    while(n1 > 0):
        b = b + (n1 % 2)*10**p
        n1 = n1//2
        p += 1
    n2 = n - n//1
    bd = 0
    p = 1
    while (n2 != 0):
        bd = bd + ((n2 * 2)//1)/10**p
        n2 = n2 * 2
        if (n2 >= 1):
            n2 -= 1
        p += 1

    if V < 0:
        return str('-') + str(b + bd)
    else:
        return str(b + bd)


def btof(Vb):

    n = Vb

    if n[0] == '-' or n[0] == '0':
        return "Underflow"

    flag = 0
    if '.' in n:
        flag = 1

    if not(flag):
        E = len(n) - 1
        M = n[1:]

        if (E > 7):
            return("Overflow")

        while (len(M) > 5):
            if M[-1] == '0':
                M = M[:-1]
            else:
                return("Error")

        while (len(M) < 5):
            M += '0'

    else:
        E = n.index('.')-1
        if (E > 7):
            return("Overflow")
        M = n[1:]
        A = list(M)
        A.remove('.')
        M = ''.join(A)
        if (len(M) > 5):
            return("Error")
    Es = (vtob(E))
    El = list(Es)
    while (len(El) < 3):
        El.insert(0, '0')

    while (len(M) < 5):
        M += '0'

    E = ''.join(El)

    return E + M


def addf(s1, s2):
    if s1 in ['Error', 'Underflow']:
        return s1
    if s2 in ['Error', 'Underflow']:
        return s2
    Vd = ftov(s1) + ftov(s2)
    Vb = vtob(Vd)
    Vf = btof(Vb)

    return Vf


def subf(s1, s2):
    Vd = ftov(s1) - ftov(s2)
    Vb = vtob(Vd)
    Vf = btof(Vb)

    return Vf


def movf(n):
    Vb = vtob(n)
    Vf = btof(Vb)
    return Vf


def conv2dec(b):  # internally runs the coversion of 8bit bin to decimal for PC
    # if len(b) != 8 or len(b)!= 16:
    #     return 'wrong value'
    # else:
    dec = 0
    b2 = b[::-1]
    for i in range(0, len(b2)):
        dec += int(b2[i])*(2**i)
    return dec


# converting integer x to 16 bit binary val to store in registers
def convert_to_16bit_bin(x):
    binary_num = bin(x)[2:]
    if len(binary_num) > 16:
        binary_num = binary_num[-16:]
    return ((16-len(binary_num))*'0')+str(binary_num)


# converting integer x to 8 bit binary val to store in PC
def convert_to_8_bit_bin(x):
    binary_num = bin(x)[2:]
    if len(binary_num) > 16:
        binary_num = binary_num[-8:]
    return ((8-len(binary_num))*'0')+str(binary_num)


def ones_complement(bin_string):  # takes 16 bit binary as input and performs bitwise NOT
    ret_string = ''
    for i in range(16):
        if bin_string[i] == '0':
            ret_string += '1'
        else:
            ret_string += '0'
    return ret_string


def conv2Lcase(reg):  # checks in case r1 is passed instead of R1. Assume FLAGS is the only correct option
    if reg[0] == 'r':
        return 'R'+reg[1]

#_____Error_Handling_Functions_____#


# inp is a list of strings. Each string is one (ideally) 16bit instruction
def check_full_len(inp):
    if len(inp) > 256:
        return 'Length Exceeded'
    else:
        return 1


# inpline is a string of (ideally) a 16bit instruction.
def check_indv_len(inpline):
    if len(inpline) != 16:
        return 'Length Exceeded'
    else:
        return 1

#_____Type_Check_&_Break_Functions_#


def check_type(inpline):  # takes in he 16bit instruction and returns type
    if inpline[0:5] not in InsType.keys():
        return 'invalid instruction'
    else:
        return InsType[inpline[0:5]]


# checks type and returns list that breaks ins into its components like opcode,regs,variable etc
def Breakin2list(inpline):
    if check_type(inpline) == 'A':
        return Break_A(inpline)
    elif check_type(inpline) == 'B':
        return Break_B(inpline)
    elif check_type(inpline) == 'C':
        return Break_C(inpline)
    elif check_type(inpline) == 'D':
        return Break_D(inpline)
    elif check_type(inpline) == 'E':
        return Break_E(inpline)
    elif check_type(inpline) == 'F':
        return Break_F(inpline)
    else:
        return 'invalid instruction'


def Break_A(inpline):
    l = []
    l += [inpline[0:5]]
    l += [inpline[7:10]]
    l += [inpline[10:13]]
    l += [inpline[13:16]]
    return l


def Break_B(inpline):
    l = []
    l += [inpline[0:5]]
    l += [inpline[5:8]]
    l += [inpline[8:]]
    return l


def Break_C(inpline):
    l = []
    l += [inpline[0:5]]
    l += [inpline[10:13]]
    l += [inpline[13:16]]
    return l


def Break_D(inpline):
    l = []
    l += [inpline[0:5]]
    l += [inpline[5:8]]
    l += [inpline[8:]]
    return l


def Break_E(inpline):
    l = []
    l += [inpline[0:5]]
    l += [inpline[8:]]
    return l


def Break_F(inpline):
    l = []
    l += [inpline[0:]]
    return l

#_____Required_Functions___________#


def PCounter(b):  # returns the instruction at the line number given(in binary)
    return MEM[conv2dec(b)]


def RF(reg):
    if reg not in comR.keys() and reg[0] != 'r':
        return 'wrong value'
    else:
        return comR[conv2Lcase(reg)]


# main code starts from here
binary_input = sys.stdin.read()
machine_code = []
machine_code1 = binary_input.split('\n')
for i in machine_code1:
    if len(i) == 16:
        machine_code += [i]
for i in range(len(machine_code)):
    MEM[i] = machine_code[i]
PC = '0'*8
comR['FLAGS'] = '0000000000000000'
len_check = check_full_len(machine_code)

clock_cycles=[]     #list of clock cycles
mem_addresses=[]    #list of memory addresses corresponding to clock cycles
cycle_count=0       #variable tracking clock cycles

while (int(PC, 2) < len(machine_code)):
    i = int(PC, 2)
    clock_cycles.append(cycle_count)
    mem_addresses.append(i)
    instruction = machine_code[i]
    type = check_type(machine_code[i])
    instruction_list = Breakin2list(machine_code[i])
    if type == 'A':
        if instruction_list[0] == '10000':  # add reg1 reg2 reg3
            sum = int(comR[regs[instruction_list[2]]], 2) + \
                int(comR[regs[instruction_list[1]]], 2)
            comR[regs[instruction_list[3]]] = convert_to_16bit_bin(sum)
            comR['FLAGS'] = '0000000000000000'
            if int(comR[regs[instruction_list[1]]], 2)+int(comR[regs[instruction_list[2]]], 2) > 65535:
                comR['FLAGS'] = '0000000000001000'
            Finstring += PC+" "
            Finstring += " ".join(list(comR.values()))+" "
            Finstring += "\n"

            PC = convert_to_8_bit_bin(i+1)
            
        elif instruction_list[0] == '10001':  # sub reg1 reg2 reg3
            diff = int(comR[regs[instruction_list[1]]], 2) - \
                int(comR[regs[instruction_list[2]]], 2)
            if diff >= 0:
                comR[regs[instruction_list[3]]] = convert_to_16bit_bin(diff)
                comR['FLAGS'] = '0000000000000000'
                Finstring += PC+" "
                Finstring += " ".join(list(comR.values()))+" "
                Finstring += "\n"

                PC = convert_to_8_bit_bin(i+1)
            else:
                comR[regs[instruction_list[3]]] = convert_to_16bit_bin(0)
                comR['FLAGS'] = '0000000000001000'
                Finstring += PC+" "
                Finstring += " ".join(list(comR.values()))+" "
                Finstring += "\n"

                PC = convert_to_8_bit_bin(i+1)
        elif instruction_list[0] == '10110':  # mul reg1 reg2 reg3
            pro = int(comR[regs[instruction_list[2]]], 2) * \
                int(comR[regs[instruction_list[1]]], 2)
            comR['FLAGS'] = '0000000000000000'
            if pro > 65535:
                comR['FLAGS'] = '0000000000001000'
            comR[regs[instruction_list[3]]] = convert_to_16bit_bin(pro)
            Finstring += PC+" "
            Finstring += " ".join(list(comR.values()))+" "
            Finstring += "\n"

            PC = convert_to_8_bit_bin(i+1)
        elif instruction_list[0] == '11010':  # xor reg1 reg2 reg3
            comR[regs[instruction_list[3]]] = convert_to_16bit_bin(
                int(comR[regs[instruction_list[1]]], 2) ^ int(comR[regs[instruction_list[2]]], 2))
            comR['FLAGS'] = '0000000000000000'
            Finstring += PC+" "
            Finstring += " ".join(list(comR.values()))+" "
            Finstring += "\n"

            PC = convert_to_8_bit_bin(i+1)
        elif instruction_list[0] == '11011':  # or reg1 reg2 reg3
            comR[regs[instruction_list[3]]] = convert_to_16bit_bin(
                int(comR[regs[instruction_list[1]]], 2) | int(comR[regs[instruction_list[2]]], 2))
            comR['FLAGS'] = '0000000000000000'
            Finstring += PC+" "
            Finstring += " ".join(list(comR.values()))+" "
            Finstring += "\n"

            PC = convert_to_8_bit_bin(i+1)

        elif instruction_list[0] == '00000':     # addf reg1 reg2 reg3
            f1 = comR[regs[instruction_list[1]]][8:]
            f2 = comR[regs[instruction_list[2]]][8:]
            comR['FLAGS'] = '0000000000000000'
            f3 = addf(f1, f2)
            Finstring += PC+" "
            if f3 == 'Error':
                Finstring += "Error: Not representable".format(i) + " "
                comR[regs[instruction_list[3]]]='0000000000000000'

            elif f3 == 'Overflow':
                # print("Error at Line {}: Not representable".format(i))
                comR['FLAGS']='0000000000001000'
                comR[regs[instruction_list[3]]]='0000000011111111'

            elif f3 == 'Underflow':
                # print("Underflow at Line {}: Not representable".format(i))
                comR['FLAGS']='0000000000001000'
                comR[regs[instruction_list[3]]]='0000000000000000'

            else:
                # print('Y')
                comR[regs[instruction_list[3]]]='00000000' + f3
            
            Finstring += " ".join(list(comR.values()))+" "
            Finstring += "\n"

            PC=convert_to_8_bit_bin(i+1)
            
        elif instruction_list[0] == '00001':  # subf reg1 reg2 reg3
            f1 = comR[regs[instruction_list[1]]][8:]
            f2 = comR[regs[instruction_list[2]]][8:]
            comR['FLAGS'] = '0000000000000000'
            f3 = subf(f1, f2)
            Finstring += PC+" "
            if f3 == 'Error':
                Finstring += "Error: Not representable".format(i) + " "
                comR[instruction_list[3]] = '0000000000000000'

            elif f3 == 'Overflow':
                # print("Error at Line {}: Not representable".format(i))
                comR['FLAGS'] = '0000000000001000'
                comR[regs[instruction_list[3]]] = '0000000011111111'

            elif f3 == 'Underflow':
                # print("Underflow at Line {}: Not representable".format(i))
                comR['FLAGS'] = '0000000000000100'
                comR[regs[instruction_list[3]]] = '0000000000000000'

            else:
                comR[regs[instruction_list[3]]] = '00000000' + f3

            Finstring += " ".join(list(comR.values()))+" "
            Finstring += "\n"            
            PC = convert_to_8_bit_bin(i+1)
    
        else:  # and reg1 reg2 reg3
            comR[regs[instruction_list[3]]]=convert_to_16bit_bin(
                int(comR[regs[instruction_list[1]]], 2) & int(comR[regs[instruction_list[2]]], 2))
            comR['FLAGS']='0000000000000000'
            Finstring += PC+" "
            Finstring += " ".join(list(comR.values()))+" "
            Finstring += "\n"

            PC=convert_to_8_bit_bin(i+1)
            
    elif type == 'B':
        if instruction_list[0] == '10010':  # mov reg1 $Imm
            comR[regs[instruction_list[1]]]=convert_to_16bit_bin(
                int(instruction_list[2], 2))
            comR['FLAGS']='0000000000000000'
            Finstring += PC+" "
            Finstring += " ".join(list(comR.values()))+" "
            Finstring += "\n"

            PC=convert_to_8_bit_bin(i+1)
        
        elif instruction_list[0] == '00010':  #movf reg1 $Imm
            
            f1 = instruction_list[2]
            
            comR[regs[instruction_list[1]]] = '00000000' + f1
            comR['FLAGS'] = '0000000000000000'
            
            Finstring += PC+" "
            Finstring += " ".join(list(comR.values()))+" "
            Finstring += "\n"
            PC = convert_to_8_bit_bin(i+1)
                    
            
        elif instruction_list[0] == '11000':  # rs reg1 $Imm
            comR[regs[instruction_list[1]]]=convert_to_16bit_bin(
                int(comR[regs[instruction_list[1]]], 2) >> int(instruction_list[2], 2))
            comR['FLAGS']='0000000000000000'
            Finstring += PC+" "
            Finstring += " ".join(list(comR.values()))+" "
            Finstring += "\n"

            PC=convert_to_8_bit_bin(i+1)
        else:  # lsreg1 $Imm
            comR[regs[instruction_list[1]]]=convert_to_16bit_bin(
                int(comR[regs[instruction_list[1]]], 2) << int(instruction_list[2], 2))
            comR['FLAGS']='0000000000000000'
            Finstring += PC+" "
            Finstring += " ".join(list(comR.values()))+" "
            Finstring += "\n"

            PC=convert_to_8_bit_bin(i+1)
    elif type == 'C':
        if instruction_list[0] == '10011':  # mov reg1 reg2
            comR[regs[instruction_list[2]]]=comR[regs[instruction_list[1]]]
            comR['FLAGS']='0000000000000000'
            Finstring += PC+" "
            Finstring += " ".join(list(comR.values()))+" "
            Finstring += "\n"

            PC=convert_to_8_bit_bin(i+1)
        elif instruction_list[0] == '10111':  # div reg3 reg4
            quo=int(comR[regs[instruction_list[1]]],
                      2)//int(comR[regs[instruction_list[2]]], 2)
            rem=int(comR[regs[instruction_list[1]]], 2) % int(
                comR[regs[instruction_list[2]]], 2)
            comR['R0']=convert_to_16bit_bin(quo)
            comR['R1']=convert_to_16bit_bin(rem)
            comR['FLAGS']='0000000000000000'
            Finstring += PC+" "
            Finstring += " ".join(list(comR.values()))+" "
            Finstring += "\n"

            PC=convert_to_8_bit_bin(i+1)
        elif instruction_list[0] == '11101':  # not reg1 reg2
            comR[regs[instruction_list[2]]]=ones_complement(
                comR[regs[instruction_list[1]]])
            comR['FLAGS']='0000000000000000'
            Finstring += PC+" "
            Finstring += " ".join(list(comR.values()))+" "
            Finstring += "\n"

            PC=convert_to_8_bit_bin(i+1)
        else:  # cmp reg1 reg2
            if int(comR[regs[instruction_list[1]]], 2) > int(comR[regs[instruction_list[2]]], 2):
                comR['FLAGS']='0000000000000010'
                Finstring += PC+" "
                Finstring += " ".join(list(comR.values()))+" "
                Finstring += "\n"

                PC=convert_to_8_bit_bin(i+1)
            elif int(comR[regs[instruction_list[1]]], 2) < int(comR[regs[instruction_list[2]]], 2):
                comR['FLAGS']='0000000000000100'
                Finstring += PC+" "
                Finstring += " ".join(list(comR.values()))+" "
                Finstring += "\n"

                PC=convert_to_8_bit_bin(i+1)
            else:
                comR['FLAGS']='0000000000000001'
                Finstring += PC+" "
                Finstring += " ".join(list(comR.values()))+" "
                Finstring += "\n"

                PC=convert_to_8_bit_bin(i+1)
    elif type == 'D':
        clock_cycles.append(cycle_count)
        mem_addresses.append(int(instruction_list[2],2))
        if instruction_list[0] == '10100':  # load reg1 mem
            new_val=MEM[conv2dec(instruction_list[2])]
            comR[regs[instruction_list[1]]]=new_val
            comR['FLAGS']='0000000000000000'
            Finstring += PC+" "
            Finstring += " ".join(list(comR.values()))+" "
            Finstring += "\n"

            PC=convert_to_8_bit_bin(i+1)
        else:
            MEM[conv2dec(instruction_list[2])
                ] = comR[regs[instruction_list[1]]]
            comR['FLAGS'] = '0000000000000000'
            Finstring += PC+" "
            Finstring += " ".join(list(comR.values()))+" "
            Finstring += "\n"

            PC = convert_to_8_bit_bin(i+1)

    elif type == 'E':
        if instruction_list[0] == '11111':  # jmp mem
            new = int(conv2dec(str(instruction_list[1])))
            comR['FLAGS'] = '0000000000000000'
            Finstring += PC+" "
            Finstring += " ".join(list(comR.values()))+" "
            Finstring += "\n"
            clock_cycles.append(cycle_count)
            mem_addresses.append(int(instruction_list[1],2))
            PC = convert_to_8_bit_bin(new)
            # continue
        elif instruction_list[0] == '01100':  # jlt mem
            if comR['FLAGS'][-3] == '1':
                new = int(conv2dec(str(instruction_list[1])))
                comR['FLAGS'] = '0000000000000000'
                Finstring += PC+" "
                Finstring += " ".join(list(comR.values()))+" "
                Finstring += "\n"
                clock_cycles.append(cycle_count)
                mem_addresses.append(int(instruction_list[1],2))
                PC = convert_to_8_bit_bin(new)
                # continue
            else:
                comR['FLAGS'] = '0000000000000000'
                Finstring += PC+" "
                Finstring += " ".join(list(comR.values()))+" "
                Finstring += "\n"

                PC = convert_to_8_bit_bin(i+1)
        elif instruction_list[0] == '01101':  # jgt mem
            if comR['FLAGS'][-2] == '1':
                new = int(conv2dec(str(instruction_list[1])))
                comR['FLAGS'] = '0000000000000000'
                Finstring += PC+" "
                Finstring += " ".join(list(comR.values()))+" "
                Finstring += "\n"
                clock_cycles.append(cycle_count)
                mem_addresses.append(int(instruction_list[1],2))
                PC = convert_to_8_bit_bin(new)
                # continue
            else:
                comR['FLAGS'] = '0000000000000000'
                Finstring += PC+" "
                Finstring += " ".join(list(comR.values()))+" "
                Finstring += "\n"

                PC = convert_to_8_bit_bin(i+1)
        else:  # je mem
            if comR['FLAGS'][-1] == '1':
                new = int(conv2dec(str(instruction_list[1])))
                comR['FLAGS'] = '0000000000000000'
                Finstring += PC+" "
                Finstring += " ".join(list(comR.values()))+" "
                Finstring += "\n"
                clock_cycles.append(cycle_count)
                mem_addresses.append(int(instruction_list[1],2))
                PC = convert_to_8_bit_bin(new)
                # continue
            else:
                comR['FLAGS'] = '0000000000000000'
                Finstring += PC+" "
                Finstring += " ".join(list(comR.values()))+" "
                Finstring += "\n"

                PC = convert_to_8_bit_bin(i+1)
    else:
        comR['FLAGS'] = '0000000000000000'
        Finstring += PC+" "
        Finstring += " ".join(list(comR.values()))+" "
        Finstring += "\n"

        break
    cycle_count+=1
Finstring += "\n".join(MEM)
sys.stdout.write(Finstring)

plt.scatter(clock_cycles,mem_addresses)
plt.xlabel("Clock cycles")
plt.ylabel("Memory addresses")
plt.show()
# cook your dish here

import sys
"""CO Project Q1 Assembler Group B15"""

comA = {'addf':'00000','subf':'00001','add': '10000', 'sub': '10001', 'mul': '10110', 'xor': '11010', 'or': '11011', 'and': '11100'}  # dictionaries for diff commands
comB = {'movf':'00010','mov': '10010', 'ls': '11001', 'rs': '11000'}
comC = {'mov': '10011', 'div': '10111', 'not': '11101', 'cmp': '11110'}
comD = {'ld': '10100', 'st': '10101'}
comE = {'jmp': '11111', 'jlt': '01100', 'jgt': '01101', 'je': '01111'}
comF = {'hlt': '01010'}
comR = {'R0': '000', 'R1': '001', 'R2': '010', 'R3': '011', 'R4': '100', 'R5': '101', 'R6': '110', 'r0': '000', 'r1': '001', 'r2': '010', 'r3': '011', 'r4': '100', 'r5': '101', 'r6': '110'}
comR2 = {'R0': '000', 'R1': '001', 'R2': '010', 'R3': '011', 'R4': '100', 'R5': '101', 'R6': '110',
         'FLAGS': '111', 'r0': '000', 'r1': '001', 'r2': '010', 'r3': '011', 'r4': '100', 'r5': '101', 'r6': '110'}
comlist = list(comA.keys())+list(comB.keys())+list(comC.keys())+list(comD.keys()) + \
    list(comE.keys())+list(comF.keys())  # combined list fo all commands
var = {}
keywords = comlist+["FLAGS", "var"]+list(comR.keys())
labels = {}
comlist2 = comlist+list(list(comR.keys()))
Error_List = []
Error_Listnum = []
mem = ['0'*16]*256  # memory

def ftov(s):
    if s=='Error':
        return 'Error'
    E=s[0:3]
    # print(E)
    
    M=s[3:-1]
    M=M+s[-1]
    Ed=0
    for i in E:
        Ed=Ed*2+eval(i)
    
    Md=1
    n=1
    for i in M:
        Md = Md + eval(i)/2**n
        n+=1
    return 2**Ed * Md

def vtob(V):
    
    n=V
    b=0
    p=0
    n1=n//1
    while(n1>0):
        b = b + (n1 % 2)*10**p
        n1=n1//2
        p+=1
    n2 = n - n//1
    bd=0
    p=1
    while ( n2!= 0 ) :
        bd = bd + ((n2 * 2)//1)/10**p
        n2 = n2 * 2
        if (n2>=1):
            n2-=1
        p+=1
    return str(b+bd)

def btof(Vb):
    
    n=Vb

    if n[0]== '-' or n[0]=='0':
        return "Underflow"

    flag=0
    if '.' in n:
        flag=1

    if not(flag):
        E = len(n) - 1
        M = n[1:]
        
        if ( E > 7):
            return("Overflow")

        while (len(M) > 5):
            if M[-1] == '0':
                M=M[:-1]
            else:
                return("Error")
        
        while (len(M)<5):
            M+='0'

    else:
        E = n.index('.')-1
        if ( E > 7):
            return("Overflow")
        M=n[1:]
        A=list(M)
        A.remove('.')
        M=''.join(A)
        if (len(M) > 5 ):
            return("Error")
    Es=(vtob(E))
    El=list(Es)
    while (len(El) < 3):
        El.insert(0,'0')
    
    while (len(M)<5):
        M+='0'

    E=''.join(El)

    return E + M

def addf(s1,s2):
    if s1 in ['Error', 'Underflow']:
        return s1
    if s2 in ['Error','Underflow']:
        return s2
    Vd = ftov(s1) + ftov(s2)
    # print(Vd)
    Vb = vtob(Vd)
    # print(Vb)
    Vf = btof(Vb)

    return Vf

def subf(s1,s2):
    Vd = ftov(s1) - ftov(s2)
    Vb = vtob(Vd)
    Vf = btof(Vb)

    return Vf

def movf(n):
    Vb = vtob(n)
    Vf = btof(Vb)
    return Vf

# print( addf ( btof('1010'),btof('10.01') ))        

def check_len_error(l):  # check memory excess
    if len(l) > 256:
        return 0
    else:
        return 1


def check_halt(l):  # check halt is final statement
    check = 0
    for i in range(0, len(l)):
        if l[i] == 'hlt':
            check = 1
            if i == len(l)-1:
                return [1, i+1]
            else:
                return [0, i+1]
    if check == 0:
        return [-1, i+1]


def check_syn_error(l):  # returns 0 for syntax errors
    for i in range(0, len(l)-1):
        if l[i][0] == 'var':  # checks for variables
            return [1, i-varl]
        elif l[i][0] in comlist:  # checks for commands
            return [2, i-varl]
        elif l[i][0] not in comlist and l[i][0][-1] == ':':  # checks for labels
            if l[i][0][:-1].isalnum():
                return [3, i-varl]
            else:
                return [0, i-varl]
        else:
            return [0, i-varl]


def error_response(l):
    global Error_List
    global Error_Listnum
    global totlen
    e1, e2 = check_halt(l), check_len_error(l)
    if e1[0] <= 0:
        if e1[0] == 0:
            Error_List += ['Incorrect Halt Declaration at line: ']
            Error_Listnum += [int(e1[1])]
        else:
            Error_List += ['No Halt Declaration at line: ']
            Error_Listnum += [totlen]
    if e2 == 0:
        Error_List += ['Exceeded Memory Length']
    else:
        return('pass')


def check_type(l):  # including label
    if l == ['hlt']:
        type = 'F'
    elif l[0] == 'mov':
        if l[-1][0] == '$':
            type = 'B'
        else:
            type = 'C'
    elif l[0] in comA.keys():
        type = 'A'
    elif l[0] in comB.keys():
        type = 'B'
    elif l[0] in comC.keys():
        type = 'C'
    elif l[0] in comD.keys():
        type = 'D'
    elif l[0] in comE.keys():
        type = 'E'
    elif len(l) == 0:
        return raiseerror()
    else:
        if l[0][-1] == ':':
            l = l[1:]
            return check_type(l)
        else:
            return raiseerror()

    return type


def merge_lists(a, b, c, d):
    L1 = a+c
    L2 = b+d
    L3 = []
    while L2 != []:
        k = L2.index(min(L2))
        L3.append(L1[k]+str(L2[k]))
        del L1[k]
        del L2[k]
    return L3


def make_8(s):
    if len(s) > 8:
        s = 'error'
    elif len(s) < 8:
        while(len(s) != 8):
            s = '0'+s
    else:
        pass
    return s


def raiseerror():
    return('Syntax Error at line: ')


def Flag_as_reg():
    return('Flag used instead of register at line: ')


def TypoError():  # errorA
    return('Typo at line: ')


def var_not_at_start(x):
    return('Variable {} not declared at start at line: '.format(x))


def UndefVar():  # errorB
    return('Undefined Variable at line: ')


def UndefLabel():  # errorC
    return('Undefined Label at line: ')


def VarinsLabel():
    return('Used Variable instead of Label at line: ')


def LabelinsVar():
    return('Used Label instead of Variable at line: ')


def Over8Bit():  # errorE
    return('Illegal Immediate Value at line: ')


def CodeA(l):
    c = ''
    if len(l) != 4:
        return raiseerror()
    if l[0] in comA.keys():
        c += comA[l[0]]+'00'
    else:
        return raiseerror()
    if l[1] in list(comR.keys()) and l[2] in list(comR.keys()) and l[3] in list(comR.keys()):
        c += comR[l[1]]+comR[l[2]]+comR[l[3]]
    else:
        return TypoError()
    return c


def CodeB(l):
    c = ''
    if len(l) != 3:
        return raiseerror()
    if l[0] in comB.keys():
        c += comB[l[0]]
        if l[1] in list(comR.keys()):
            c += comR[l[1]]
        else:
            return TypoError()
    else:
        return raiseerror()

    if l[0]=='movf':
        if '.' in l[2][1:]:
            L=list(l[2][1:])
            try:
                L.remove('-')    
            except:
                pass
            
            try:
                L.remove('.')
            except:
                pass
            L2=''.join(L)
            if l[2][0] == '$' and L2.isnumeric():
                a = btof(vtob( eval(l[2][1:]) ))
                if a in ['Error','Overflow','Underflow']:
                    return ('Error - Not representable at line : ')
                else:
                    c+=a
            else:
                return raiseerror()
        else:
            return "Integer instead of float at line : "
    else:
        if l[2][0] == '$' and l[2][1:].isnumeric():
            if int(l[2][1:]) < 0:
                return Over8Bit()
            else:
                e = make_8(format(int(l[2][1:]), "b"))
                if e == 'error':
                    return Over8Bit()
                else:
                    c += e
        else:
            return raiseerror()
    return c


def CodeC(l):
    c = ''
    if len(l) != 3:
        return raiseerror()
    if l[0] in comC.keys():
        c += comC[l[0]]+'00000'
    else:
        return raiseerror()
    if l[2] in list(comR.keys()) and l[1] in list(comR2.keys()):
        c += comR2[l[1]]+comR[l[2]]
    else:
        if l[2] == 'FLAGS':
            return Flag_as_reg()
        else:
            return TypoError()
    return c


def CodeD(l):
    c = ''
    if len(l) != 3:
        return raiseerror()
    if l[0] in comD.keys():
        c += comD[l[0]]
    else:
        return raiseerror()
    if l[1] in list(comR.keys()):
        c += comR[l[1]]
    else:
        return TypoError()
    if l[2] in var.keys():
        e = make_8(format(int(var[l[2]]), "b"))
        if e == 'error':
            return Over8Bit()
        else:
            c += e
    else:
        if l[2] in labels.keys():
            return LabelinsVar()
        else:
            return UndefVar()
    return c


def CodeE(l):
    c = ''
    if len(l) != 2:
        return raiseerror()
    if l[0] in comE.keys():
        c += comE[l[0]]+'000'
    else:
        return raiseerror()
    if l[1] in labels.keys():
        e = make_8(format(int(labels[l[1]]), "b"))
        if e == 'error':
            return Over8Bit()
        else:
            c += e
    else:
        if l[1] in var.keys():
            return VarinsLabel()
        else:
            return UndefLabel()
    return c


def CodeF(l):
    if l == ['hlt']:
        return '0101000000000000'
    else:
        return raiseerror()


def ins_coder(l):
    t = check_type(l)  # now encode for each case

    if t == 'A':
        return CodeA(l)
    elif t == 'B':
        return CodeB(l)
    elif t == 'C':
        return CodeC(l)
    elif t == 'D':
        return CodeD(l)
    elif t == 'E':
        return CodeE(l)
    else:
        return CodeF(l)


def binary_encoder_all_line(l):
    L = []  # final list of all codes
    global var
    for i in l:  # each command
        t = check_type(i)
        if t == 'var':
            continue
        elif t != 'syntax error':
            L += [ins_coder(i)]
        else:
            L += [TypoError()]
    return L


allL = {}
s = sys.stdin.read()
varchek, inscheck = 0, 0
s2 = s.split('\n')
totlen = len(s2)
t = []
for i in s2:
    if i != '':
        t += [i]
allD = []
allDnum = []
for i in range(0, len(t)):
    allD += [t[i]]
    allDnum += [i+1]
varlist = []
lablist = []
listwithcommands = []
lwcnum = []
totlen = len(allD)
# 2ndpass
varflag = 1
j = 1
for i in range(0, len(allD)):
    g = allD[i].split()
    if g[0] == 'var':
        if len(g) == 2:
            if g[1] not in keywords:
                if varflag == 1:
                    listwithcommands += [allD[i]]
                    lwcnum += [j]
                    varlist += [g[1]]
                else:
                    v = var_not_at_start(g[1])
                    listwithcommands += [v]
                    lwcnum += [j]
            else:
                listwithcommands += [raiseerror()]
                lwcnum += [j]
        else:
            listwithcommands += [raiseerror()]
            lwcnum += [j]
    elif g[0][-1] == ':':
        varflag = -1
        if len(g) != 1:
            if g[0][:-1].isalnum():
                if g[0][:-1] not in keywords:
                    if g[1][-1] != ':':
                        listwithcommands += [" ".join(g[1:])]
                        lwcnum += [j]
                        lablist += [g[0][:-1]]
                        labels[g[0][:-1]] = j
                    else:
                        listwithcommands += [raiseerror()]
                        lwcnum += [j]
                else:
                    listwithcommands += [raiseerror()]
                    lwcnum += [j]
            else:
                listwithcommands += [raiseerror()]
                lwcnum += [j]
        else:
            listwithcommands += [raiseerror()]
            lwcnum += [j]
    elif g[0] in comlist:
        varflag = -1
        listwithcommands += [allD[i]]
        lwcnum += [j]
    else:
        varflag = -1
        listwithcommands += [TypoError()]
        lwcnum += [j]
    j += 1
var = {}
c = 0
for i in varlist:
    var[i] = totlen-len(varlist)+c
    c += 1
for i in labels:
    labels[i] = labels[i]-len(varlist)-1
listwithcommands2 = []  
error_response(listwithcommands)
for i in range(0, len(listwithcommands)):
    if listwithcommands[i].split()[0] == 'var' or listwithcommands[i][-2] == ':':
        listwithcommands2 += [listwithcommands[i]]
    else:
        listwithcommands2 += [ins_coder(listwithcommands[i].split())]

Final_Error = []
Final_Errornum = []

FinalFinal = []
FinalFinalnum = []
listwithcommands2 = listwithcommands2[len(var):]
lwcnum = lwcnum[len(var):]
for i in range(0, len(listwithcommands2)):
    if listwithcommands2[i].isnumeric() == False:
        Final_Error += [listwithcommands2[i]]
        Final_Errornum += [lwcnum[i]]
FinalFinal = merge_lists(Error_List, Error_Listnum,
                         Final_Error, Final_Errornum)

if len(FinalFinal) > 0:
    sys.stdout.write('\n'.join(FinalFinal))

else:
    sys.stdout.write('\n'.join(listwithcommands2))
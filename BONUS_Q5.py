from math import log2
s=input("Enter the space in memory: ")
space=s.split()
memory_space=int(space[0])    #in bits

if space[1]=='B':
    memory_space*=2**3
elif space[1]=='b':
    memory_space*=2**0
elif space[1]=='KB':
    memory_space*=2**13         #2^10 for kilo and 8 for bytes
elif space[1]=='Kb':
    memory_space*=2**10         #2^10 for kilo
elif space[1]=='MB':
    memory_space*=2**23
elif space[1]=='Mb':
    memory_space*=2**20
elif space[1]=='GB':
    memory_space*=2**33
elif space[1]=='Gb':
    memory_space*=2**30
elif space[1]=='TB':
    memory_space*=2**43
elif space[1]=='Tb':
    memory_space*=2**40

cpu_bits=int(input("\nEnter how many bits does the CPU have: "))

print(f"""\nMemory can be addressed in the following ways:
1. Bit Addressable Memory - Cell Size = 1 bit
2. Nibble Addressable Memory - Cell Size = 4 bit
3. Byte Addressable Memory - Cell Size = 8 bits(standard)
4. Word Addressable Memory - Cell Size = Word Size ({cpu_bits} bits)
""")

choice=int(input("Enter number corresponding to how memory is addressed: "))

if choice==1:
    mem_address_len=int(log2(memory_space))     #bit addressable memory
elif choice==2:
    mem_address_len=int(log2(memory_space/4))   #nibble addressable memory
elif choice==3:
    mem_address_len=int(log2(memory_space/8))   #byte addressable memory
elif choice==4:
    mem_address_len=int(log2(memory_space/cpu_bits))    #word addressable memory


address_pins=mem_address_len

query_cont='Y'

while(query_cont.upper()=='Y'):
    print("""\nYou can run the following queries:
    1. ISA Related query(outputs details related to the ISA)
    2. System Enhancement Related query(outputs the change in address pins after change in system addresability)
    3. Memory size related(outputs how big the main memory can be in Bytes)
    """)

    query=int(input("Enter number corresponding to the query you wish to perform: "))

    if query==1:
        instruction_len=int(input("\nEnter length of one instruction in bits: "))
        register_len=int(input("Enter length of register in bits: "))
        opcode_len=instruction_len-register_len-mem_address_len
        print("\nMinimum bits required to represent an address=",mem_address_len)
        print("Number of bits needed by opcode=",opcode_len)
        print("Number of filler bits in instruction type 2=",(instruction_len-(2*register_len)-opcode_len))
        print("Maximum number of instructions this ISA can support=",2**opcode_len)
        print("Maximum number of registers this ISA can support=",2**register_len)

    elif query==2:
        cpu_bits=int(input("\nEnter how many bits does the CPU have: "))
        print(f"""\nMemory can be addressed in the following ways:
        1. Bit Addressable Memory - Cell Size = 1 bit
        2. Nibble Addressable Memory - Cell Size = 4 bit
        3. Byte Addressable Memory - Cell Size = 8 bits(standard)
        4. Word Addressable Memory - Cell Size = Word Size ({cpu_bits} bits)
        """)
        
        choice=int(input("Enter number corresponding to how memory is addressed: "))
        if choice==1:
            new_address_pins=int(log2(memory_space))     #bit addressable memory
        elif choice==2:
            new_address_pins=int(log2(memory_space/4))   #nibble addressable memory
        elif choice==3:
            new_address_pins=int(log2(memory_space/8))   #byte addressable memory
        elif choice==4:
            new_address_pins=int(log2(memory_space/cpu_bits))    #word addressable memory
        print()
        print(new_address_pins-address_pins)

    elif query==3:
        cpu_bits=int(input("\nEnter how many bits does the CPU have: "))
        add_pins=(int(input("Enter number of address pins: ")))
        mem_space=2**add_pins
        print(f"""\nMemory can be addressed in the following ways:
        1. Bit Addressable Memory - Cell Size = 1 bit
        2. Nibble Addressable Memory - Cell Size = 4 bit
        3. Byte Addressable Memory - Cell Size = 8 bits(standard)
        4. Word Addressable Memory - Cell Size = Word Size ({cpu_bits} bits)
        """)
        choice=int(input("Enter number corresponding to how memory is addressed: "))

        if choice==1:
            mem_space*=1
        elif choice==2:
            mem_space*=4
        elif choice==3:
            mem_space*=8
        elif choice==4:
            mem_space*=cpu_bits
        

        print()
        if mem_space%8==0:
            power=int(log2(mem_space/8))
            num=2**(power%10)
            exp=power//10
            if exp==0:
                print(f"{num} B")
            elif exp==1:
                print(f"{num} KB")
            elif exp==2:
                print(f"{num} MB")
            elif exp==3:
                print(f"{num} GB")
            elif exp==4:
                print(f"{num} TB")
        else:
            print(f"{mem_space} bits")
    
    query_cont=input("\nDo you wish to run more queries? (Enter Y for Yes,  N for No): ")
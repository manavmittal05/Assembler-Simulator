import math

def btoGB(x):
    return x/(8*1024*1024*1024)

def MBtob(x):
    return x*(2**10)*(2**10)*8

def type1():
    global x,z,y, bbb , rrr
    print("-----------------------------------------------------------------------------------------------------")
    print("                                             Type 1                                                ")
    print("-----------------------------------------------------------------------------------------------------")
    if(w[1] != 'kWord'):
        a=int(input("Enter number of bits the CPU is: "))
    else:
        a= rrr
    if(y==1):
        P2 =math.log2(x)
    elif(y==2):
        P2=math.log2(x/4)
    elif(y==3): 
        P2=math.log2(x/8)
    elif(y==4):
        P2=math.log2(x/a)
    print("What would you like to change the current adressing to?\n1.Bit addressable\n2.Nibble addressable\n3.Byte addressable\n4.Word addressable")
    z1 = int(input("Enter the memory addressable type: "))
    if(z1==1):
        P1 =math.log2(x)
    elif(z1==2):
        P1=math.log2(x/4)
    elif(z1==3): 
        P1=math.log2(x/8)
    elif(z1==4):
        P1=math.log2(x/a)
    if(P1-P2 <0):
        print(f"-{(-(P1-P2))}")
    else:
        print(f"+{(P1-P2)}")
    return 

def type2():
    print("-----------------------------------------------------------------------------------------------------")
    print("                                           Type 2                                                 ")
    print("-----------------------------------------------------------------------------------------------------")
    x = int(input("Enter number of bits the CPU is: "))
    y = int(input("Enter the number of address pins it has: "))
    print("1.Bit addressable\n2.Nibble addressable\n3.Byte addressable\n4.Word addressable")
    z = int(input("Enter the memory addressable type: "))
    if(z==1):
        m=btoGB((2**y)*1)
        if(m>1):
            print(math.ceil(m),"GB")
        elif(m*1024 >1):
            print(math.ceil(m*1024),"MB")
        elif(m*1024*1024 >1):
            print(math.ceil(m*1024*1024), "KB")
        elif(m*1024*1024*1024>1):
            print(math.ceil(m*1024*1024*1024),"B")
        else:
            print(math.ceil(m) , "GB")
    if(z==2):
        m=btoGB((2**y)*4)
        if(m>1):
            print(math.ceil(m),"GB")
        elif(m*1024 >1):
            print(math.ceil(m*1024),"MB")
        elif(m*1024*1024 >1):
            print(math.ceil(m*1024*1024), "KB")
        elif(m*1024*1024*1024>1):
            print(math.ceil(m*1024*1024*1024),"B")
        else:
            print(math.ceil(m) , "GB")
    if(z==3):
        m=btoGB((2**y)*8)
        if(m>1):
            print(math.ceil(m),"GB")
        elif(m*1024 >1):
            print(math.ceil(m*1024),"MB")
        elif(m*1024*8 >1):
            print(math.ceil(m*1024*8),"Mb")
        elif(m*1024*1024 >1):
            print(math.ceil(m*1024*1024), "KB")
        elif(m*1024*1024*8 >1):
            print(math.ceil(m*1024*1024*8), "Kb")
        elif(m*1024*1024*1024>1):
            print(math.ceil(m*1024*1024*1024),"B")
        elif(m*1024*1024*1024*8>1):
            print(math.ceil(m*1024*1024*1024*8),"B")
        else:
            print(math.ceil(m) , "GB")
    if(z==4):
        m=btoGB((2**y)*x)
        if(m>1):
            print(math.ceil(m),"GB")
        elif(m*1024 >1):
            print(math.ceil(m*1024),"MB")
        elif(m*1024*1024 >1):
            print(math.ceil(m*1024*1024), "KB")
        elif(m*1024*1024*1024>1):
            print(math.ceil(m*1024*1024*1024),"B")
        else:
            print(math.ceil(m) , "GB")
    print("-----------------------------------------------------------------------------------------------------")
    print("                                          PROGRAM ENDED                                              ")
    print("-----------------------------------------------------------------------------------------------------")


print("-----------------------------------------------------------------------------------------------------")
print("                                       WELCOME TO BONUS Q5                                           ")
print("-----------------------------------------------------------------------------------------------------")
print("                                         INITIALISATION                                              ")
print("-----------------------------------------------------------------------------------------------------")
w = [i for i in input("Enter space in memory: ").split(" ")]
bbb=w[0]
if(w[1]=='MB'): x = MBtob(int(w[0]))
elif(w[1]=='KB'): x = 1024*int(w[0])*8
elif(w[1]=='GB'): x = 1024*1024*1024*int(w[0])*8
elif(w[1]=='Kb'): x = 1024*int(w[0])
elif(w[1]=='Gb'): x = 1024*1024*1024*int(w[0])
elif(w[1]=='Mb'): x = 1024*1024*int(w[0])
elif(w[1]=='kB'): x = 1024*int(w[0])*8
elif(w[1]=='kWord'): 
    rrr = int(input("Enter number of bits the CPU is: "))
    x = int(w[0])*1024*rrr
    y=4

if(w[1] != 'kWord'):
    print("1.Bit addressable\n2.Nibble addressable\n3.Byte addressable\n4.Word addressable")
    y = int(input("Enter the type of addressing: "))
print()
print("-----------------------------------------------------------------------------------------------------")
print("                                      ISA AND INSTRUCTIONS                                           ")
print("-----------------------------------------------------------------------------------------------------")
instruction_length= int(input("Enter length of 1 instruction in bits: "))
register_size = int(input("Enter size of register in bits: "))
if(y==1):
    P =math.log2(x)
elif(y==2):
    P=math.log2(x/4)
elif(y==3): 
    P=math.log2(x/8)
elif(y==4):
    rrr = int(input("Enter number of bits the CPU is: "))
    P=math.log2(x/rrr)
P=math.ceil(P)
Q=instruction_length - (P+register_size)
Q=math.ceil(Q)
R=instruction_length -(Q+ (2*register_size))
print("Minimum bits needed to represent an address in this architecture is: ", math.ceil(P))
print("Number of bits needed by opcode: ",math.ceil(Q))
print("Number of filler bits in instruction type 2: ", math.ceil(R))
print("Maximum nuber of instructions this ISA can support: ",math.ceil(2**Q))
print("Maximum nuber of registers this ISA can support: ", math.ceil(2**register_size))
print()
print("-----------------------------------------------------------------------------------------------------")
print("                                       SYSTEM ENHANCEMENT                                            ")
print("-----------------------------------------------------------------------------------------------------")
type1()
type2()


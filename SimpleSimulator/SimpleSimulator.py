import sys
import matplotlib.pyplot
import struct

program = [x for x in sys.stdin.read().split('\n') if x != '']
# program = [x for x in input().split() if x != '']
program_counter = 0
flags = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
file_registers = {'000': '0000000000000000',
                  '001': '0000000000000000',
                  '010': '0000000000000000',
                  '011': '0000000000000000',
                  '100': '0000000000000000',
                  '101': '0000000000000000',
                  '110': '0000000000000000',
                  '111': flags}
memory = program + ['0000000000000000' for _ in range(0, 256-len(program))]
len_of_program = len(program)

x = []
y = []

flag_affected = False

cycle = 1


def fetch_typeA(instruction):
    result = instruction[13:16]
    operand1 = instruction[7:10]
    operand2 = instruction[10:13]
    return result, operand1, operand2


def add(instruction):
    result, operand1, operand2 = fetch_typeA(instruction)
    global file_registers, flag_affected, flags
    value = int(file_registers[operand2], 2) + int(file_registers[operand1], 2)
    if value >= 65536:
        flags = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        flags[-4] = '1'
        flag_affected = True
    value = value % 65536
    file_registers[result] = format(value, '016b')
    print_reg_state()


def sub(instruction):
    result, operand1, operand2 = fetch_typeA(instruction)
    global file_registers, flag_affected, flags
    value = (int(file_registers[operand1], 2) - int(file_registers[operand2], 2))
    if value < 0:
        flags = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        flags[-4] = '1'
        file_registers[result] = f'{0:016b}'
        flag_affected = True
    else:
        file_registers[result] = format(value, '016b')
    print_reg_state()


def mul(instruction):
    result, operand1, operand2 = fetch_typeA(instruction)
    global file_registers, flag_affected, flags
    value = int(file_registers[operand1], 2) * int(file_registers[operand2], 2)
    if value >= 65536:
        flags = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        flags[-4] = '1'
        flag_affected = True
    value = value % 65536
    file_registers[result] = format(value, '016b')
    print_reg_state()


def XOR(instruction):
    result, operand1, operand2 = fetch_typeA(instruction)
    global file_registers
    file_registers[result] = format((int(file_registers[operand1], 2) ^ int(file_registers[operand2], 2)), '016b')
    print_reg_state()


def OR(instruction):
    result, operand1, operand2 = fetch_typeA(instruction)
    global file_registers
    file_registers[result] = format((int(file_registers[operand1], 2) | int(file_registers[operand2], 2)), '016b')
    print_reg_state()


def AND(instruction):
    result, operand1, operand2 = fetch_typeA(instruction)
    global file_registers
    file_registers[result] = format((int(file_registers[operand1], 2) & int(file_registers[operand2], 2)), '016b')
    print_reg_state()


def fetch_typeB(instruction):
    register = instruction[5:8]
    immediate = instruction[8:16]
    return register, immediate


def binTofloat(number):
    exponent = number[8:11]
    mantissa = number[11:16]
    int_exponent = int(exponent, 2)
    decimal_part = '1'+mantissa[:int_exponent]
    float_part = mantissa[int_exponent:]
    val = 0.0
    multiplier = 1
    for bit in decimal_part[::-1]:
        val += int(bit)*multiplier
        multiplier *= 2
    multiplier = 0.5
    for bit in float_part:
        val += int(bit)*multiplier
        multiplier /= 2
    return val


def floatTobin(num):
    bits, = struct.unpack('!I', struct.pack('!f', num))
    bin_num = "{:032b}".format(bits)
    exponent = format(int(bin_num[1:9], 2)-127, '03b')
    mantissa = bin_num[9:]
    return '00000000'+(exponent+mantissa)[:8]


def f_add(instruction):
    global flags, flag_affected
    result, operand1, operand2 = fetch_typeA(instruction)
    value = binTofloat(file_registers[operand1]) + binTofloat(file_registers[operand2])
    if value > 252:
        flags = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        flags[-4] = '1'
        flag_affected = True
        file_registers[result] = '0000000011111111'
    else:
        file_registers[result] = floatTobin(value)
    print_reg_state()


def f_sub(instruction):
    global flags, flag_affected
    result, operand1, operand2 = fetch_typeA(instruction)
    value = binTofloat(file_registers[operand1]) - binTofloat(file_registers[operand2])
    if value < 1:
        flags = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        flags[-4] = '1'
        flag_affected = True
        file_registers[result] = format(0, '016b')
    else:
        file_registers[result] = floatTobin(value)
    print_reg_state()


def f_mov(instruction):
    register, immediate = fetch_typeB(instruction)
    file_registers[register] = floatTobin(binTofloat('00000000'+immediate))
    print_reg_state()


def mov_I(instruction):
    register, immediate = fetch_typeB(instruction)
    global file_registers
    file_registers[register] = '00000000' + immediate
    print_reg_state()


def right_shift(instruction):
    register, immediate = fetch_typeB(instruction)
    global file_registers
    file_registers[register] = format((int(file_registers[register], 2) // (2**int(immediate, 2))) % 65536, '016b')
    print_reg_state()


def left_shift(instruction):
    register, immediate = fetch_typeB(instruction)
    global file_registers
    file_registers[register] = format((int(file_registers[register], 2) * (2**int(immediate, 2))) % 65536, '016b')
    print_reg_state()


def fetch_typeC(instruction):
    register1 = instruction[10:13]
    register2 = instruction[13:16]
    return register1, register2


def mov_R(instruction):
    register1, register2 = fetch_typeC(instruction)
    global file_registers
    if register1 == '111':
        file_registers[register2] = ''.join(flags)
    else:
        file_registers[register2] = file_registers[register1]
    print_reg_state()


def div(instruction):
    register1, register2 = fetch_typeC(instruction)
    global file_registers
    if int(file_registers[register2], 2) == 0:
        raise ZeroDivisionError("Cannot divide by zero, value stored in R%d is 0." % int(register2, 2))
    file_registers['000'] = format(int(file_registers[register1], 2) // int(file_registers[register2], 2), '016b')
    file_registers['001'] = format(int(file_registers[register1], 2) % int(file_registers[register2], 2), '016b')
    print_reg_state()


def cmp(instruction):
    register1, register2 = fetch_typeC(instruction)
    global file_registers, flag_affected, flags
    flags = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
    if int(file_registers[register1], 2) < int(file_registers[register2], 2):
        flags[-3] = '1'
    elif int(file_registers[register1], 2) > int(file_registers[register2], 2):
        flags[-2] = '1'
    else:
        flags[-1] = '1'
    flag_affected = True
    print_reg_state()


def invert(instruction):
    register1, register2 = fetch_typeC(instruction)
    global file_registers
    file_registers[register2] = format(65535 - int(file_registers[register1], 2), '016b')
    print_reg_state()


def fetch_typeD(instruction):
    register = instruction[5:8]
    index = int(instruction[8:16], 2)
    return register, index


def load(instruction):
    register, mem_address = fetch_typeD(instruction)
    global file_registers
    file_registers[register] = memory[mem_address]
    x.append(cycle)
    y.append(mem_address)
    print_reg_state()


def store(instruction):
    register, mem_address = fetch_typeD(instruction)
    global file_registers
    memory[mem_address] = file_registers[register]
    x.append(cycle)
    y.append(mem_address)
    print_reg_state()


def fetch_typeE(instruction):
    mem_address = int(instruction[8:16], 2)
    return mem_address


def jmp(instruction):
    mem_address = fetch_typeE(instruction)
    global program_counter
    print_reg_state()
    program_counter = mem_address


def jlt(instruction):
    mem_address = fetch_typeE(instruction)
    global file_registers, program_counter
    if flags[-3] == '1':
        print_reg_state()
        program_counter = mem_address
    else:
        print_reg_state()


def jgt(instruction):
    mem_address = fetch_typeE(instruction)
    global file_registers, program_counter
    if flags[-2] == '1':
        print_reg_state()
        program_counter = mem_address
    else:
        print_reg_state()


def jeq(instruction):
    mem_address = fetch_typeE(instruction)
    global file_registers, program_counter
    if flags[-1] == '1':
        print_reg_state()
        program_counter = mem_address
    else:
        print_reg_state()


opcode = {'10000': add, '10001': sub, '10010': mov_I, '10011': mov_R, '10100': load, '10101': store, '10110': mul,
          '10111': div, '11000': right_shift, '11001': left_shift, '11010': XOR, '11011': OR, '11100': AND,
          '11101': invert, '11110': cmp, '11111': jmp, '01100': jlt, '01101': jgt, '01111': jeq, '00000': f_add,
          '00001': f_sub, '00010': f_mov}


def print_reg_state():
    global cycle, flag_affected, program_counter, flags

    x.append(cycle)
    y.append(program_counter)
    if not flag_affected:
        flags = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']

    print("%s %s %s %s %s %s %s %s %s" % (f'{program_counter:08b}', file_registers['000'],
                                          file_registers['001'], file_registers['010'],
                                          file_registers['011'], file_registers['100'],
                                          file_registers['101'], file_registers['110'],
                                          ''.join(flags)))
    cycle += 1
    program_counter += 1
    flag_affected = False


while program[program_counter] != '0101000000000000':
    command = program[program_counter]
    opcode[command[0:5]](command)

if not flag_affected:
    flags = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']

print("%s %s %s %s %s %s %s %s %s" % (f'{program_counter:08b}', file_registers['000'],
                                      file_registers['001'], file_registers['010'],
                                      file_registers['011'], file_registers['100'],
                                      file_registers['101'], file_registers['110'],
                                      ''.join(flags)))

x.append(cycle)
y.append(program_counter)

for i in memory:
    print(i)

# matplotlib.pyplot.scatter(x, y, alpha=0.8)
# matplotlib.pyplot.xlabel("Cycle")
# matplotlib.pyplot.ylabel("Memory Address")
# matplotlib.pyplot.xticks(x)
# matplotlib.pyplot.show()


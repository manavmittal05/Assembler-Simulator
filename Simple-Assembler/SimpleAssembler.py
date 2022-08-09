import sys
import struct
decode = {'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5, 'R6': 6, 'FLAGS': 7}


def getcode(o):
    codes = {'add': '10000', 'sub': '10001', 'movI': '10010', 'movR': '10011', 'ld': '10100', 'st': '10101',
             'mul': '10110', 'divi': '10111', 'rs': '11000', 'ls': '11001', 'xor': '11010', 'or': '11011',
             'and': '11100', 'not': '11101', 'cmp': '11110', 'jmp': '11111', 'jlt': '01100', 'jgt': '01101',
             'je': '01111', 'hlt': '01010', 'addf': '00000', 'subf': '00001', 'movf': '00010'}
    return codes[o]


def floatTobin(num):
    bits, = struct.unpack('!I', struct.pack('!f', num))
    bin_num = "{:032b}".format(bits)
    exponent = format(int(bin_num[1:9], 2)-127, '03b')
    mantissa = bin_num[9:]
    return (exponent+mantissa)[:8]


def A(opcode, reg1, reg2, reg3):
    a = list(getcode(opcode))
    x1 = list(f'{decode.get(reg1):03b}')
    x2 = list(f'{decode.get(reg2):03b}')
    x3 = list(f'{decode.get(reg3):03b}')

    a = a + ['0', '0']
    a = a + x1
    a = a + x2
    a = a + x3
    print(''.join(a))


def B(opcode, reg1, imm):
    a = list(getcode(opcode))
    x1 = list(str(f'{decode.get(reg1):03b}'))
    # imm = int(imm)
    if '.' not in imm:
        imm = list(f'{int(imm):08b}')
    else:
        imm = list(floatTobin(float(imm)))
    a = a + x1
    a = a + imm
    print(''.join(a))


def C(opcode, reg1, reg2):
    a = list(str(getcode(opcode)))
    x1 = list(f'{decode.get(reg1):03b}')
    x2 = list(f'{decode.get(reg2):03b}')
    a = a + ['0', '0', '0', '0', '0']
    a = a + x1
    a = a + x2
    print(''.join(a))


def D(opcode, reg1, addr):
    a = list(str(getcode(opcode)))
    x1 = list(f'{decode.get(reg1):03b}')
    addr = list(f'{addr:08b}')
    a = a + x1
    a = a + addr
    print(''.join(a))


def E(opcode, addr):
    a = list(str(getcode(opcode)))
    addr = list(f'{addr:08b}')
    a = a + ['0', '0', '0']
    a = a + addr
    print(''.join(a))


def F(opcode):
    a = list(str(getcode(opcode)))
    a = a + ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
    print(''.join(a))


cmd = sys.stdin.read().split('\n')
cmd = [x.split() for x in cmd if x != '\n' and x != '']

ops_A = ['add', 'sub', 'mul', 'xor', 'or', 'and', 'addf', 'subf']
ops_B = ['mov', 'ls', 'rs', 'movf']
ops_C = ['mov', 'div', 'not', 'cmp']
ops_D = ['ld', 'st']
ops_E = ['jmp', 'jlt', 'jgt', 'je']
ops_F = ['hlt']
regs = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R0']
variables = {}
var_count = 0
labels = {}
no_cmds = len(cmd)
e_count = 0

if not cmd:
    exit()

while cmd != [] and cmd[0][0] == 'var':
    variables[cmd[0][1]] = var_count
    if cmd[0][1] in ['R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'FLAGS']:
        e_count += 1
        print('Syntax Error: Invalid variable declaration.')
    cmd.pop(0)
    var_count += 1

for i in variables.keys():
    variables[i] += no_cmds-var_count

for w in range(len(cmd)):
    i = cmd[w]
    if ':' in i[0]:
        labels[i[0][:-1]] = w
        if i[0][:-1] in ['R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'FLAGS']:
            e_count += 1
            print('Syntax Error: Invalid label declaration.')
        i.pop(0)

if len(cmd) > 256:
    print("Compilation Error: Memory Overflow!")
    exit()

if ['hlt'] not in cmd:
    e_count += 1
    print('Syntax Error: hlt instruction is not present in the file.')

if cmd[-1] != ['hlt'] and ['hlt'] in cmd:
    e_count += 1
    print('Syntax Error: hlt instruction is not found at the EOF')

if cmd.count(['hlt']) > 1:
    e_count += 1
    print('Syntax Error: There are more than 1 hlt instructions in the file.')

for w in range(len(cmd)):
    i = cmd[w]
    if 'var' in i:
        e_count += 1
        print('Syntax Error: Invalid variable declaration in line %d' % (w + var_count + 1))
        continue
    if ':' in ''.join(i):
        e_count += 1
        print('Syntax Error: Invalid label declaration in line %d' % (w + var_count + 1))
        continue
    if 'FLAGS' in i:
        if i[0] != 'mov':
            e_count += 1
            print('Syntax Error: Invalid use of Flag registers in line %d' % (w + var_count + 1))
            continue
        if i[2] == 'FLAGS':
            e_count += 1
            print('Syntax Error: Invalid use of Flag registers in line %d' % (w + var_count + 1))
            continue

    try:
        if i[0] not in ops_A + ops_B + ops_C + ops_D + ops_E + ops_F:
            e_count += 1
            print('Syntax Error: Invalid instruction in line %d' % (w + var_count + 1))
            continue
    except IndexError:
        e_count += 1
        print('Syntax Error: Incorrect use of syntax in line %d' % (w + var_count + 1))
        continue

    if i[0] == 'mov' or i[0] == 'movf':
        try:
            if i[1] not in regs+['FLAGS']:
                e_count += 1
                print('Syntax Error: Invalid use of registers in line %d' % (w + var_count + 1))
                continue
            if '$' in i[2] and '.' in i[2] and (1 > float(i[2][1:]) or float(i[2][1:]) > 252) and i[0] == 'movf':
                e_count += 1
                print('Syntax Error: Invalid literal value in line %d' % (w + var_count + 1))
                continue
            if '$' in i[2] and '.' in i[2] and i[0] == 'mov':
                e_count += 1
                print('Syntax Error: Invalid literal value in line %d' % (w + var_count + 1))
                continue
            if '$' in i[2] and '.' not in i[2] and (0 > int(i[2][1:]) or int(i[2][1:]) > 255):
                e_count += 1
                print('Syntax Error: Invalid literal value in line %d' % (w + var_count + 1))
                continue
            if '$' not in i[2] and i[2] not in regs:
                e_count += 1
                print('Syntax Error: Invalid use of registers in line %d' % (w + var_count + 1))
                continue
        except IndexError:
            e_count += 1
            print("Syntax Error: Incorrect use of syntax at line %d" % (w + var_count + 1))
            continue

    else:
        if i[0] in ops_A:
            try:
                if i[1] not in regs or i[2] not in regs or i[3] not in regs:
                    e_count += 1
                    print('Syntax Error: Invalid use of registers in line %d' % (w + var_count + 1))
                    continue
            except IndexError:
                print('General Syntax Error: Invalid use of syntax in line %d' % (w + var_count + 1))
                continue
        if i[0] in ops_C:
            if i[1] not in regs or i[2] not in regs:
                e_count += 1
                print('Syntax Error: Invalid use of registers in line %d' % (w + var_count + 1))
                continue

        if i[0] in ops_B:
            try:
                if i[1] not in regs + ['FLAGS']:
                    e_count += 1
                    print('Syntax Error: Invalid use of registers in line %d' % (w + var_count + 1))
                    continue
                if '$' in i[2] and '.' in i[2] and (1 > float(i[2][1:]) or float(i[2][1:]) > 252) and i[0] == 'movf':
                    e_count += 1
                    print('Syntax Error: Invalid literal value in line %d' % (w + var_count + 1))
                    continue
                if '$' in i[2] and '.' in i[2] and i[0] == 'mov':
                    e_count += 1
                    print('Syntax Error: Invalid literal value in line %d' % (w + var_count + 1))
                    continue
                if '$' in i[2] and '.' not in i[2] and (0 > int(i[2][1:]) or int(i[2][1:]) > 255):
                    e_count += 1
                    print('Syntax Error: Invalid literal value in line %d' % (w + var_count + 1))
                    continue
                if '$' not in i[2] and i[2] not in regs:
                    e_count += 1
                    print('Syntax Error: Invalid use of registers in line %d' % (w + var_count + 1))
                    continue
            except IndexError:
                e_count += 1
                print("Syntax Error: Incorrect use of syntax at line %d" % (w + var_count + 1))
                continue
    if i[0] in ops_D:
        try:
            if i[1] not in regs:
                e_count += 1
                print('Syntax Error: Invalid use of registers in line %d' % (w + var_count + 1))
                continue
            if i[2] not in variables:
                e_count += 1
                print("Syntax Error: Use of undefined variable '%s' in line %d" % (i[2], (w + var_count + 1)))
                continue
        except IndexError:
            e_count += 1
            print("Syntax Error: Incorrect use of syntax at line %d" % (w + var_count + 1))
            continue
    if i[0] in ops_E:
        try:
            if i[1] not in labels:
                e_count += 1
                print("Syntax Error: Use of undefined label '%s' in line %d" % (i[1], (w + var_count + 1)))
                continue
        except IndexError:
            e_count += 1
            print("Syntax Error: Incorrect use of syntax at line %d" % (w + var_count + 1))
            continue


p_counter = 0
c_addr = len(cmd)-var_count

while p_counter < len(cmd) and e_count == 0:
    c = cmd[p_counter]
    if ':' in c[0]:
        labels[c[0][:-1]] = p_counter
        c.pop(0)

    if c[0] == 'var':
        variables[c[1]] = c_addr
        c_addr += 1
        cmd.pop(p_counter)
        p_counter -= 1

    elif len(c) == 4:
        A(c[0], c[1], c[2], c[3])

    elif len(c) == 3 and '$' in c[2]:
        if c[0] == 'mov':
            B('movI', c[1], c[2][1:])
        elif c[0] == 'ls':
            B(c[0], c[1], c[2][1:])
        elif c[0] == 'rs':
            B(c[0], c[1], c[2][1:])
        elif c[0] == 'movf':
            B(c[0], c[1], c[2][1:])

    elif len(c) == 3:
        if 'R' in c[2]:
            if c[0] == 'mov':
                C('movR', c[1], c[2])
            elif c[0] == 'div':
                C('divi', c[1], c[2])
            elif c[0] == 'not':
                C('not', c[1], c[2])
            elif c[0] == 'cmp':
                C('cmp', c[1], c[2])

        elif c[2] == 'FLAGS':
            C('movR', c[1], c[2])

        else:
            D(c[0], c[1], variables[c[2]])

    elif len(c) == 2:
        E(c[0], labels[c[1]])

    elif c[0] == 'hlt':
        F(c[0])

    p_counter += 1




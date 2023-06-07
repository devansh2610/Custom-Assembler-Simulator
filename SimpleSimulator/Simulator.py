import sys

def fetchA(instruction):
    final = instruction[7:10]
    operand1 = instruction[10:13]
    operand2 = instruction[13:16]
    return final, operand1, operand2



def fetchB(instruction):
    register = instruction[6:9]
    immediate = instruction[9:16]
    return register, immediate


def fetchfB(instruction):
    register = instruction[5:8]
    immediate = instruction[8:16]
    return register, immediate




def fetchC(instruction):
    register1 = instruction[10:13]
    register2 = instruction[13:16]
    return register1, register2


def fetchD(instruction):
    register = instruction[6:9]
    index = int(instruction[10:16], 2)
    return register, index

def fetchE(instruction):
    memory_addr = int(instruction[9:16], 2)
    return memory_addr

def add(instruction):
    final, operand1, operand2 = fetchA(instruction) 
    global dict, tag, flags
    value = int(dict[operand2], 2) + int(dict[operand1], 2)
    if value >= 65536:
        flags = ['0']*16
        flags[-4] = '1'
        tag = True
    value = value % 65536
    dict[final] = format(value, '016b')
    print_output()








def sub(instruction):
    final, operand1, operand2 = fetchA(instruction)
    global dict, tag, flags
    value = (int(dict[operand1], 2) - int(dict[operand2], 2))
    if value < 0:
        flags = ['0']*16
        flags[-4] = '1'
        dict[final] = f'{0:016b}'
        tag = True
    else:
        dict[final] = format(value, '016b')
    print_output()

def mul(instruction):
    final, operand1, operand2 = fetchA(instruction)
    global dict, tag, flags
    value = int(dict[operand1], 2) * int(dict[operand2], 2)
    if value >= 65536:
        flags = ['0']*16
        flags[-4] = '1'
        tag = True
    value = value % 65536
    dict[final] = format(value, '016b')
    print_output()

def XOR(instruction):
    final, operand1, operand2 = fetchA(instruction)
    global dict
    dict[final] = format((int(dict[operand1], 2) ^ int(dict[operand2], 2)), '016b')
    print_output()


def jlt(instruction):
    memory_addr = fetchE(instruction)
    global dict, pc
    if flags[-3] == '1':
        print_output()
        pc = memory_addr
    else:
        print_output()

def OR(instruction):
    final, operand1, operand2 = fetchA(instruction)
    global dict
    dict[final] = format((int(dict[operand1], 2) | int(dict[operand2], 2)), '016b')
    print_output()

def ori(instruction):
    register,immediate=fetchB(instruction)
    global dict
    dict[register] = format((int(dict[register], 2) | int(immediate, 2)), '016b')
    print_output()

def AND(instruction):
    final, operand1, operand2 = fetchA(instruction)
    global dict
    dict[final] = format((int(dict[operand1], 2) & int(dict[operand2], 2)), '016b')
    print_output()

def andi(instruction):
    register,immediate=fetchB(instruction)
    global dict
    dict[register] = format((int(dict[register], 2) & int(immediate, 2)), '016b')
    print_output()



def muli(instruction):
    register,immediate=fetchB(instruction)
    global dict
    value = int(immediate, 2) * int(dict[register], 2)
    value = value % 65536
    dict[register] = format(value, '016b')
    print_output()

def subi(instruction):
    register,immediate=fetchB(instruction)
    global dict
    value = int(immediate, 2) - int(dict[register], 2)
    value = value % 65536
    dict[register] = format(value, '016b')
    print_output()

def jgt(instruction):
    memory_addr = fetchE(instruction)
    global dict, pc
    if flags[-2] == '1':
        print_output()
        pc = memory_addr
    else:
        print_output()
def mov_I(instruction):
    register, immediate = fetchB(instruction)
    global dict
    dict[register] = '000000000' + immediate
    print_output()


def ftb(num):
    x = bin(int(num))[2:]
    y = len(x)-1
    exp = y+3
    num = float(num)
    integer, decimal = str(num).split(".")
    integer = bin(int(integer))[2:]
    decimal = float("0." + decimal)
    tempdecimal = decimal
    string,ans = "", 0
    count = 0
    while(True):
        count = count + 1
        ans = tempdecimal*2
        if ans==1 or count==6:
            string = string + "1" 
            break
        else:
            ans = str(ans)
            string = string + ans[0]
            tempdecimal = float("0." + ans[2])
    string = string[::-1]
    ans = integer + "." + string
    x = ans.find(".")
    ans = ans.replace(".","")
    ans = ans[0] + "." + ans[1:]
    end = (bin(exp)[2:]) + ans[2:]
    if len(end)>=9: return '00000000' + end[0:8]
    else: return '00000000' + end.zfill(8)


def btf(num):
    exp = num[8:11]
    mantissa = num[11:16]
    intexp = int(exp, 2) - 3
    newvar = mantissa[0:len(mantissa)]
    newmantissa = "1" + "." + mantissa[0:len(mantissa)]
    newvar2 = newvar[0:intexp] + "." + newvar[intexp:]
    mantissa = "1" + newvar2
    count = 0
    for i in mantissa:
        if i==".":
            break
        else:
            count = count + 1
    countdec = len(mantissa) - count - 1
    count = count - 1
    newi = count+2
    i = 0
    integer = 0
    while(count>=0):
        integer = integer + int(mantissa[i])*(2**count)
        count = count - 1
        i = i + 1
    decimal = 0
    while(countdec>0):
        decimal = decimal + int(mantissa[newi])*(2**(-countdec))
        countdec = countdec - 1
        newi = newi + 1
    val = float(integer) + float(decimal)
    return val

def f_add(instruction):
    global flags, tag
    final, operand1, operand2 = fetchA(instruction)
    value = btf(dict[operand1]) + btf(dict[operand2])
    if value > 252:
        flags = ['0']*16
        flags[-4] = '1'
        tag = True
        dict[final] = '0000000011111111'
    else:
        dict[final] = ftb(value)
    print_output()


def f_sub(instruction):
    global flags, tag
    final, operand1, operand2 = fetchA(instruction)
    value = btf(dict[operand1]) - btf(dict[operand2])
    if value < 1:
        flags = ['0']*16
        flags[-4] = '1'
        tag = True
        dict[final] = format(0, '016b')
    else:
        dict[final] = ftb(value)
    print_output()




def f_mov(instruction):
    register, immediate = fetchfB(instruction)
    dict[register] = ftb(btf('000000000'+immediate))
    print_output()


def right_shift(instruction):
    register, immediate = fetchB(instruction)
    global dict
    dict[register] = format((int(dict[register], 2) // (2**int(immediate, 2))) % 65536, '016b')
    print_output()




def mov_R(instruction):
    register1, register2 = fetchC(instruction)
    global dict
    if register1 == '111':
        dict[register2] = ''.join(flags)
        #dict[register2]=dict[register2][:-1]+'1'
    elif register2=='111':
        dict[register1] = ''.join(flags)
    else:
        dict[register2] = dict[register1]
        dict[register2] = dict[register2][:-1]+'1'
    print_output()

def left_shift(instruction):
    register, immediate = fetchB(instruction)
    global dict
    dict[register] = format((int(dict[register], 2) * (2**int(immediate, 2))) % 65536, '016b')
    print_output()



def div(instruction):
    register1, register2 = fetchC(instruction)
    global dict
    if int(dict[register2], 2) == 0:
        raise ZeroDivisionError("Cannot divide by zero, value stored in R%d is 0." % int(register2, 2))
    dict['000'] = format(int(dict[register1], 2) // int(dict[register2], 2), '016b')
    dict['001'] = format(int(dict[register1], 2) % int(dict[register2], 2), '016b')
    print_output()



def cmp(instruction):
    register1, register2 = fetchC(instruction)
    global dict, tag, flags
    flags = ['0']*16
    if int(dict[register1], 2) < int(dict[register2], 2):
        flags[-3] = '1'
    elif int(dict[register1], 2) > int(dict[register2], 2):
        flags[-2] = '1'
    else:
        flags[-1] = '1'
    tag = True
    print_output()






'''def fetch(instruction):
    opcode = instruction[:5]
    register1 = instruction[5:8]
    register2 = instruction[8:11]
    register3 = instruction[11:14]
    immediate = instruction[8:16]
    return opcode, register1, register2, register3, immediate'''


def jeq(instruction):
    memory_addr = fetchE(instruction)
    global dict, pc
    if flags[-1] == '1':
        print_output()
        pc = memory_addr
    else:
        print_output()


def jmp(instruction):
    memory_addr = fetchE(instruction)
    global pc
    print_output()
    pc = memory_addr







def load(instruction):
    register, memory_addr = fetchD(instruction)
    global dict
    dict[register] = memory[memory_addr]
    x.append(cycle)
    y.append(memory_addr)
    print_output()



def store(instruction):
    register, memory_addr = fetchD(instruction)
    global dict
    memory[memory_addr] = dict[register]
    x.append(cycle)
    y.append(memory_addr)
    print_output()

def addi(instruction):
    register,immediate=fetchB(instruction)
    global dict
    value = int(immediate, 2) + int(dict[register], 2)
    value = value % 65536
    dict[register] = format(value, '016b')
    print_output()

def invert(instruction):
    register1, register2 = fetchC(instruction)
    global dict
    dict[register2] = format(65535 - int(dict[register1], 2), '016b')
    print_output()

opcode = {'00000': add, '00001': sub, '00010': mov_I, '00011': mov_R, '00100': load, 
        '00101': store, '00110': mul,'00111': div, '01000': right_shift, '01001': left_shift,
        '01010': XOR, '01011': OR, '01100': AND, '01101': invert, '01110': cmp, '01111': jmp,
        '11100': jlt, '11101': jgt, '11111': jeq, '10000': f_add, '10001': f_sub, 
        '10010': f_mov, '10011':addi,'10100':subi,'10101':muli,'10111':andi,'11000':ori}

def print_output():
    global cycle, tag, pc, flags
    x.append(cycle)
    y.append(pc)
    if not tag:
        flags = ['0']*16

    print("%s        %s %s %s %s %s %s %s %s" % (f'{pc:07b}', dict['000'],dict['001'], dict['010'],dict['011'], dict['100'],dict['101'], dict['110'],''.join(flags)))
    cycle += 1
    pc += 1
    tag = False

def hlt(instruction):
    mem_address = fetchE(instruction)
    global file_registers, program_counter
    print_output()
    for i in memory:
        print(i)
    exit(0)

'''def print_output():
    print(f"Cycle: {cycle}")
    print(f"PC: {pc}")
    for i, reg in enumerate(registers):
        print(f"Register {i}: {int(reg, 2)}")
    print(f"Flags: {flags}\n")'''



program = [x for x in sys.stdin.read().split('\n') if x != '']
pc = 0 #program counter
flags = ['0']*16
dict = {'000': '0000000000000000','001': '0000000000000000','010': '0000000000000000','011': '0000000000000000','100': '0000000000000000','101': '0000000000000000','110': '0000000000000000','111': flags}
memory = program + ['0000000000000000' for _ in range(0, 128-len(program))]
len_of_program = len(program)

x = []
y = []

tag = False

cycle = 1

while program[pc] != '1101000000000000':
    command = program[pc]
    instruction=opcode[command[0:5]]
    instruction(command)

if not tag:
    flags = ['0']*16

print("%s        %s %s %s %s %s %s %s %s" % (f'{pc:07b}', dict['000'], dict['001'], dict['010'], dict['011'], dict['100'], dict['101'], dict['110'], ''.join(flags)))

x.append(cycle)
y.append(pc)

#printing memory
for i in memory:
    print(i)
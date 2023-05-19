import sys
myfile = sys.stdin.read().splitlines()
count = 0
output = []
labels = {}
variables = {}
register = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"}

def mul(arr, register, count):
    if "FLAGS" in arr:
        raise SyntaxError(f"ERROR: Flags used as operands: line {count}")
    if len(arr) != 4:
        raise SyntaxError(f"ERROR: Invalid Arguments: line {count}")
    else:
        c = 0
        opcode = "0011000"
        for j in range(1, 4):
            for i in register:
                if i == arr[j]:
                    opcode = opcode + register[i]
                    c = 0
                    break
                else:
                    c = 1
            if c == 1:
                raise SyntaxError(f"ERROR: Invalid Register:   line {count}")
        return opcode
        
def add(arr, register, count):
    if "FLAGS" in arr:
        raise SyntaxError(f"ERROR: Flags used as operands: line {count}")
    if len(arr) != 4:
        raise SyntaxError(f"ERROR: Invalid Arguments: line {count}")
    else:
        c = 0
        opcode = "0000000"
        for j in range(1, 4):
            for i in register:
                if i == arr[j]:
                    opcode = opcode + register[i]
                    c = 0
                    break
                else:
                    c = 1
            if c == 1:
                raise SyntaxError(f"ERROR: Invalid Register: line {count}")
        return opcode
    
def ld(arr, variables, count):
    out = "001000"
    if len(arr) == 3:
        if arr[1] in register:
            out = out + register.get(arr[1])
            if variables.get(arr[2]):
                extend = variables.get(arr[2])
                out = out + (extend).zfill(8)
                n_str = out[0:9] + out[10:]
                return n_str
            else:
                raise SyntaxError(f"ERROR: Var not found: line {count}")
        elif arr[1] == "FLAGS":
            raise SyntaxError(f"ERROR: Writing to flag register: line {count}")
        else:
            raise SyntaxError(f"ERROR: Register not found: line {count}")
    else:
        raise SyntaxError(f"ERROR: Invalid Arguments: line {count}")

def div(arr, register, count):
    if "FLAGS" in arr:
        raise SyntaxError(f"ERROR: Flags used as operand:  line {count}")
    if len(arr) != 3:
        raise SyntaxError(f"ERROR: Invalid Arguments: line {count}")
    else:
        c = 0
        opcode = "0011100000"
        for j in range(1, 3):
            for i in register:
                if i == arr[j]:
                    opcode = opcode + register[i]
                    c = 0
                    break
                else:
                    c = 1
            if c == 1:
                raise SyntaxError(f"ERROR: Invalid Register:   line {count}")
        return opcode

def mov(arr, register, count):
    if len(arr) != 3:
        raise SyntaxError(f"ERROR: Invalid Arguments: line {count}")
    if arr[2][0] == "$":
        opcode = "000100"
        if arr[1] not in register:
            raise SyntaxError(f"ERROR: Invalid register: line {count}")
        opcode = opcode + register[arr[1]]
        opcode = opcode + bin(int(arr[2][1:]))[1:]
        return opcode
    else:
        opcode = "0001100000"
        if arr[1] not in register and arr[2] not in register:
            raise SyntaxError(f"ERROR: Invalid register: line {count}")
        elif arr[1] == "FLAGS" and arr[2] == "FLAGS":
            raise SyntaxError(f"ERROR: Improper use of flag: line {count}")
        opcode = opcode + register[arr[1]] + register[arr[2]]
        return opcode

def sub(arr, register, count):
    if "FLAGS" in arr:
        raise SyntaxError(f"ERROR: Flags used as operand:  line {count}")
    if len(arr) != 4:
        raise SyntaxError(f"ERROR: Invalid Arguments: line {count}")
    else:
        c = 0
        opcode = "0000100"
        for j in range(1, 4):
            for i in register:
                if i == arr[j]:
                    opcode = opcode + register[i]
                    c = 0
                    break
                else:
                    c = 1
            if c == 1:
                raise SyntaxError(f"ERROR: Invalid Register:  line {count}")
        return opcode

def st(arr, variables, register, count):
    out = "001010"
    if len(arr) == 3:
        if arr[1] in register:
            out += register.get(arr[1])
            if variables.get(arr[2]):
                extend = variables.get(arr[2])
                out += extend.zfill(8)
                n_str = out[0:9] + out[10:]
                return n_str
            else:
                raise SyntaxError(f"ERROR: Var not found: at line {count}")

        elif arr[1] == "FLAGS":
            raise SyntaxError(
                f"ERROR: Trying to save flag register to extendory: at line {count}"
            )

        else:
            raise SyntaxError(f"ERROR: Invalid Register: line {count}")

    else:
        raise SyntaxError(f"ERROR: Invalid Arguments: line {count}")

def Compare(arr, register, count):
    if "FLAGS" in arr:
        raise SyntaxError(f"ERROR: Flags used as operands: line {count}")
    if len(arr) != 3:
        raise SyntaxError(f"ERROR: Invalid Arguments: line {count}")
    else:
        c = 0
        opcode = "0111000000"
        for j in range(1, 3):
            for i in register:
                if i == arr[j]:
                    opcode = opcode + register[i]
                    c = 0
                    break
                else:
                    c = 1
            if c == 1:
                raise SyntaxError(f"ERROR: Invalid Register:   line {count}")
        return opcode
     
def bin(dec):
    s = ""
    while dec != 0:
        s += str(dec % 2)
        dec = dec // 2
    s = s[::-1]
    s = "0" * (8 - len(s)) + s
    return s

halt_count = 0
var_count = 0
for line in myfile:
    var_list = line.strip().split()
    if ":" in var_list[0]:
        var_list[0] = var_list[0][:-1]
    if var_list[0] == "":
        continue
    else:
        count += 1
        var_list = line.strip().split()
        if ":" in var_list[0]:
            var_list[0] = var_list[0][:-1]
        if line.split(":")[-1].strip() == "hlt":
            halt_count += 1
        if var_list[0] == "var":
            var_count += 1
            if len(var_list) != 2:
                raise SyntaxError(
                    f"Invalid definition of variable {var_list[0]}: line {count}"
                )
            if count > var_count:
                raise SyntaxError(
                    f"Invalid definition of variable {var_list[1]}: line {count}"
                )
        elif ":" in line:
            if line.split(":")[1].strip() == "":
                raise SyntaxError(f"No argument passed after the label: line {count}")
            if line.split(":")[0].strip() in labels:
                raise SyntaxError(f"Invalid definition of label {line.split(':')[0].strip()}: line {count}")
            labels[line.split(":")[0].strip()] = bin(count - var_count - 1)
if halt_count == 0:
    raise SyntaxError("No halt defined")
if halt_count > 1 or myfile[-1].split(":")[-1].strip() != "hlt":
    raise SyntaxError(f"Invalid definition of halt: line {count}")

count = 0
for line in myfile:
    var_list = line.strip().split()
    if line == "":
        continue
    else:
        count += 1
        if var_list[0] == "var":
            if var_list[1] in variables:
                raise SyntaxError(
                    f"Invalid definition of variable {var_list[0]}: line {count}"
                )
            variables[var_list[1]] = bin(len(myfile) - var_count + count - 1)
        else:
            if ":" in line and len(line.split(":")) > 2:
                raise SyntaxError(f"2 labels found: at line {count}")
            if ":" in line:
                var_list = line.split(":")[1].strip().split()

            if var_list[0] == "mov":
                output.append(mov(var_list, register, count))

            elif var_list[0] == "hlt":
                output.append("1101000000000000")

            elif var_list[0] == "add":
                output.append(add(var_list, register, count))

            elif var_list[0] == "sub":
                output.append(sub(var_list, register, count))

            elif var_list[0] == "mul":
                output.append(mul(var_list, register, count))

            elif var_list[0] == "div":
                output.append(div(var_list, register, count))

            elif var_list[0] == "mov":
                output.append(mov(var_list, register, count))

            elif var_list[0] == "and":
                output.append(AND(var_list, register, count))

            elif var_list[0] == "cmp":
                output.append(Compare(var_list, register, count))

            elif var_list[0] == "not":
                output.append(Invert(var_list, register, count))

            elif var_list[0] == "ls":
                output.append(Lshift(var_list, register, count))

            elif var_list[0] == "rs":
                output.append(Rshift(var_list, register, count))

            elif var_list[0] == "or":
                output.append(OR(var_list, register, count))

            elif var_list[0] == "xor":
                output.append(XOR(var_list, register, count))

            elif var_list[0] == "ld":
                x = ld(var_list, variables, count)
                if type(x) != list:
                    output.append(ld(var_list, variables, count))

            elif var_list[0] == "st":
                output.append(st(var_list, variables, register, count))

            elif var_list[0] == "jgt":
                arr = var_list
                out = "11101"
                if len(arr) == 2:
                    out += "000"
                    if labels.get(arr[1]) is not None:
                        extend = labels.get(arr[1])
                        out += extend.zfill(8)
                        output.append(out)
                    else:
                        raise SyntaxError(f"ERROR: Label not found: line {count}")
                else:
                    raise SyntaxError(f"ERROR: Invalid Arguments: line {count}")

            elif var_list[0] == "jmp":
                arr = var_list
                out = "01111000"
                if len(arr) == 2:
                    if labels.get(arr[1]) is not None:
                        extend = labels.get(arr[1])
                        out += extend.zfill(8)
                        output.append(out)
                    else:
                        raise SyntaxError(f"ERROR: Label not found: line {count}")
                else:
                    raise SyntaxError(f"ERROR: Invalid Arguments: line {count}")

            elif var_list[0] == "jlt":
                arr = var_list
                out = "11100000"
                if len(arr) == 2:
                    if labels.get(arr[1]) is not None:
                        extend = labels.get(arr[1])
                        out += extend.zfill(8)
                    else:
                        raise SyntaxError(f"ERROR: Label not found: line {count}")
                else:
                    raise SyntaxError(f"ERROR: Invalid Arguments: line {count}")
                output.append(out)

            elif var_list[0] == "je":
                arr = var_list
                out = "11111000"
                if len(arr) == 2:
                    if labels.get(arr[1]) is not None:
                        extend = labels.get(arr[1])
                        out += extend.zfill(8)
                        output.append(out)
                    else:
                        raise SyntaxError(f"ERROR: Label not found: line {count}")
                else:
                    raise SyntaxError(f"ERROR: Invalid Arguments: line {count}")
            else:
                raise SyntaxError(f"Syntax error: line {count}")

machine_code = output
for ip in machine_code:
    sys.stdout.write(ip + "\n")
    
'''def Invert(arr, register, count):
    if "FLAGS" in arr:
        raise SyntaxError(f"ERROR: Flags used as operands: line {count}")
    if len(arr) != 3:
        raise SyntaxError(f"ERROR: Invalid Arguments: line {count}")
    else:
        c = 0
        opcode = "0110100000"
        for j in range(1, 3):
            for i in register:
                if i == arr[j]:
                    opcode = opcode + register[i]
                    c = 0
                    break
                else:
                    c = 1
            if c == 1:
                raise SyntaxError(f"ERROR: Invalid Register: line {count}")
        return opcode
        
def AND(arr, register, count):
    if "FLAGS" in arr:
        raise SyntaxError(f"ERROR: Flags used as operand:  line {count}")
    if len(arr) != 4:
        raise SyntaxError(f"ERROR: Incorrect number of operands: line {count}")
    else:
        c = 0
        opcode = "0110000"
        for j in range(1, 4):
            for i in register:
                if i == arr[j]:
                    opcode += register[i]
                    c = 0
                    break
                else:
                    c = 1
            if c == 1:
                raise SyntaxError(f"ERROR: Invalid Register:  line {count}")
        return opcode
        
def XOR(arr, register, count):
    if "FLAGS" in arr:
        raise SyntaxError(f"ERROR: Flags used as operand:  line {count}")
    if len(arr) != 4:
        raise SyntaxError(f"ERROR: Invalid Arguments: line {count}")
    else:
        c = 0
        opcode = "0101000"
        for j in range(1, 4):
            for i in register:
                if i == arr[j]:
                    opcode = opcode + register[i]
                    c = 0
                    break
                else:
                    c = 1
            if c == 1:
                raise SyntaxError(f"ERROR: Invalid Register:  line {count}")
        return opcode

def OR(arr, register, count):
    if "FLAGS" in arr:
        raise SyntaxError(f"ERROR: Flags used as operand:  line {count}")
    if len(arr) != 4:
        raise SyntaxError(f"ERROR: Invalid Arguments: line {count}")
    else:
        c = 0
        opcode = "0101100"
        for j in range(1, 4):
            for i in register:
                if i == arr[j]:
                    opcode = opcode + register[i]

                    c = 0
                    break
                else:
                    c = 1
            if c == 1:
                raise SyntaxError(f"ERROR: Invalid Register:  line {count}")
        return opcode
        
def Rshift(arr, register, count):
    out = "01000"
    if "FLAGS" in arr:
        raise SyntaxError(f"ERROR: Flags used as operand:  line {count}")
    if len(arr) == 3:
        if arr[1] == "FLAGS":
            raise SyntaxError(f"ERROR: Improper use of flag:  line {count}")
        if arr[1] in register:
            out += register.get(arr[1])
        else:
            raise SyntaxError(f"ERROR: Invalid Register:  line {count}")
        imm = arr[2]
        if imm[0] == "$":
            imm = int(imm[1 : len(imm)])
            if imm in range(256):
                imm_bin = str(bin(imm))
                imm_bin = imm_bin[2 : len(imm_bin)]
                if len(imm_bin) < 8:
                    imm_bin = (8 - len(imm_bin)) * "0" + imm_bin
                out += imm_bin
            else:
                raise SyntaxError(f"ERROR: Immediate out of bound: line {count}")
        else:
            raise SyntaxError(f"ERROR: Invalid Immediate Input: line {count}")
        return out
    else:
        raise SyntaxError(f"ERROR: Invalid Arguments: line {count}")

def Lshift(arr, register, count):
    out = "01001V"
    if "FLAGS" in arr:
        raise SyntaxError(f"ERROR: Flags used as operand: line {count}")
    if len(arr) == 3:
        if arr[1] == "FLAGS":
            raise SyntaxError(f"ERROR: Improper use of flag: line {count}")
        if arr[1] in register:
            out += register.get(arr[1])
        else:
            raise SyntaxError(f"ERROR: Invalid register: line {count}")
        imm = arr[2]
        if imm[0] == "$":
            imm = int(imm[1 : len(imm)])
            if imm in range(256):
                imm_bin = str(bin(imm))
                imm_bin = imm_bin[2 : len(imm_bin)]
                if len(imm_bin) < 8:
                    imm_bin = (8 - len(imm_bin)) * "0" + imm_bin
                out += imm_bin
            else:
                raise SyntaxError(f"ERROR: Immediate out of bound: line {count}")
        else:
            raise SyntaxError(f"ERROR: Invalid Immediate Input: line {count}")
        return out
    else:
        raise SyntaxError(f"ERROR: Invalid Arguments: line {count}")'''


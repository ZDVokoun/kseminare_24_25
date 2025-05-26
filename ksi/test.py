from enum import Enum


class Operation(Enum):
    ADD = 1
    SUB = 2
    INC = 3
    DEC = 4
    CMP = 5

    MOV = 11
    READ = 12
    WRITE = 13
    SET = 14

    PUSH = 21
    POP = 22

    HLT = 31
    NOP = 32

    CALL = 41
    RET = 42

    JMP = 51
    JZ = 52
    JNZ = 53
    JO = 54
    JNO = 55
    JS = 56
    JNS = 57
    JP = 58
    JNP = 59

    INPUT = 61
    OUTPUT = 62


class Status(Enum):
    OK = 1
    HALTED = 2
    BAD_OPERAND = 3
    MEMORY_ERROR = 4
    BAD_INSTRUCTION = 5


class Instruction:
    def __init__(self, op: Operation, operands: list[str]):
        self.op = op
        self.operands = operands


class KPU:
    def __init__(self, memory_size: int, registers: set[str], min_number: int, max_number: int, operations: set[Operation] | None = None):
        if memory_size < 0 or min_number > max_number or memory_size - 1 > max_number or min_number > 0 or max_number < 0:
            raise ValueError("Invalid memory size or number range")
        if any(reg.isdecimal() for reg in registers):
            raise ValueError("Registers must have non-numeric names")
        
        self.memory_size = memory_size
        self.min_number = min_number
        self.max_number = max_number
        self.memory = [0] * memory_size
        self.registers = {reg: 0 for reg in registers}
        self.registers["PC"] = 0
        self.registers["SP"] = memory_size - 1
        self.flags = {"Overflow": False, "Sign": False, "Zero": False, "Parity": False}
        self.status = Status.OK
        self.operations = operations if operations is not None else set(Operation)
    
    def run_program(self, code: list[Instruction]) -> tuple[Status, list[int], int]:
        self.cur_code_len = len(code)
        while self.status == Status.OK:
            if not (0 <= self.registers["PC"] < len(code)):
                self.status = Status.MEMORY_ERROR
                break
            # print(self.registers["PC"], code[self.registers["PC"]].op, code[self.registers["PC"]].operands)
            
            instr = code[self.registers["PC"]]
            self.registers["PC"] = (self.registers["PC"] + 1) % self.max_number

            if instr.op not in self.operations:
                self.status = Status.BAD_INSTRUCTION
                break

            if instr.op == Operation.HLT:
                if instr.operands:
                    self.status = Status.BAD_OPERAND
                    break
                self.status = Status.HALTED
                break
            elif instr.op == Operation.NOP:
                if instr.operands:
                    self.status = Status.BAD_OPERAND
                    break
                continue
            elif instr.op == Operation.PUSH:
                if self.registers["SP"] < 0 or self.registers["SP"] >= self.memory_size:
                    self.status = Status.MEMORY_ERROR
                    break
                if len(instr.operands) != 1 or instr.operands[0] not in self.registers:
                    self.status = Status.BAD_OPERAND
                    break
                self.memory[self.registers["SP"]] = self.registers[instr.operands[0]]
                self.registers["SP"] -= 1
                if self.registers["SP"] < self.min_number:
                    self.registers["SP"] = self.max_number + ((self.registers["SP"] - self.max_number) % (self.max_number - self.min_number + 1))
                
            elif instr.op == Operation.POP:
                if len(instr.operands) != 1 or instr.operands[0] not in self.registers:
                    self.status = Status.BAD_OPERAND
                    break
                if self.registers["SP"] < 0 or self.registers["SP"] >= self.memory_size:
                    self.status = Status.MEMORY_ERROR
                    break
                self.registers["SP"] += 1
                if self.registers["SP"] > self.max_number:
                    self.registers["SP"] = self.min_number + ((self.registers["SP"] - self.min_number) % (self.max_number - self.min_number + 1))
                if self.registers["SP"] < 0 or self.registers["SP"] >= self.memory_size:
                    self.status = Status.MEMORY_ERROR
                    break
                self.registers[instr.operands[0]] = self.memory[self.registers["SP"]]
            elif instr.op == Operation.CALL:
                if len(instr.operands) != 1:
                    self.status = Status.BAD_OPERAND
                    break
                if not instr.operands[0].lstrip('-').isdigit():
                    self.status = Status.BAD_OPERAND
                    break
                operand = int(instr.operands[0])
                if not (self.min_number <= operand <= self.max_number):
                    self.status = Status.BAD_OPERAND
                    break
                if self.registers["SP"] < 0 or self.registers["SP"] >= self.memory_size:
                    self.status = Status.MEMORY_ERROR
                    break
                self.memory[self.registers["SP"]] = self.registers["PC"]
                self.registers["PC"] = operand
                self.registers["SP"] -= 1
                if self.registers["SP"] < self.min_number:
                    self.registers["SP"] = self.max_number + ((self.registers["SP"] - self.max_number) % (self.max_number - self.min_number + 1))
            elif instr.op == Operation.RET:
                if self.registers["SP"] < 0 or self.registers["SP"] >= self.memory_size:
                    self.status = Status.MEMORY_ERROR
                    break
                if len(instr.operands) != 0:
                    self.status = Status.BAD_OPERAND
                    break
                self.registers["SP"] += 1
                if self.registers["SP"] > self.max_number:
                    self.registers["SP"] = self.min_number + ((self.registers["SP"] - self.min_number) % (self.max_number - self.min_number + 1))
                if self.registers["SP"] < 0 or self.registers["SP"] >= self.memory_size:
                    self.status = Status.MEMORY_ERROR
                    break
                self.registers["PC"] = self.memory[self.registers["SP"]]
            elif instr.op == Operation.ADD:
                self._add(instr.operands)
            elif instr.op == Operation.SUB:
                self._sub(instr.operands)
            elif instr.op == Operation.INC:
                self._inc(instr.operands)
            elif instr.op == Operation.DEC:
                self._dec(instr.operands)
            elif instr.op == Operation.CMP:
                self._cmp(instr.operands)
            elif instr.op == Operation.MOV:
                self._mov(instr.operands)
            elif instr.op == Operation.READ:
                self._read(instr.operands)
            elif instr.op == Operation.WRITE:
                self._write(instr.operands)
            elif instr.op == Operation.SET:
                self._set(instr.operands)

            elif instr.op in {Operation.JMP, Operation.JZ, Operation.JNZ, Operation.JO, Operation.JNO, Operation.JS, Operation.JNS, Operation.JP, Operation.JNP}:
                self._jump(instr.op, instr.operands)
            elif instr.op == Operation.INPUT:
                if len(instr.operands) != 1 or instr.operands[0] not in self.registers:
                    self.status = Status.BAD_OPERAND
                    break
                char = input()[0]
                self.registers[instr.operands[0]] = ord(char)
                if self.registers[instr.operands[0]] > self.max_number:
                    self.registers[instr.operands[0]] = self.min_number + ((self.registers[instr.operands[0]] - self.min_number) % (self.max_number - self.min_number + 1))
                if self.registers[instr.operands[0]] < self.min_number:
                    self.registers[instr.operands[0]] = self.max_number + ((self.registers[instr.operands[0]] - self.max_number) % (self.max_number - self.min_number + 1))
            elif instr.op == Operation.OUTPUT:
                if len(instr.operands) != 1 or instr.operands[0] not in self.registers:
                    self.status = Status.BAD_OPERAND
                    break
                try:
                    print(chr(self.registers[instr.operands[0]]), end="")
                except ValueError:
                    self.status = Status.MEMORY_ERROR
            else:
                self.status = Status.BAD_INSTRUCTION
                break
        
        return self.status, self.memory, self.registers["PC"]
    
    def reset(self) -> None:
        self.memory = [0] * self.memory_size
        for reg in self.registers:
            self.registers[reg] = 0
        self.registers["SP"] = self.memory_size - 1
        self.flags = {"Overflow": False, "Sign": False, "Zero": False, "Parity": False}
        self.status = Status.OK
    
    def _add(self, operands):
        if len(operands) != 2 or operands[0] not in self.registers or operands[1] not in self.registers:
            self.status = Status.BAD_OPERAND
            return
        result = self.registers[operands[0]] + self.registers[operands[1]]
        if result > self.max_number or result < self.min_number:
            result = self.min_number + ((result - self.min_number) % (self.max_number - self.min_number + 1))
            self.flags["Overflow"] = True
        self.registers[operands[0]] = result
        self._set_flag(result)
    
    def _sub(self, operands):
        if len(operands) != 2 or operands[0] not in self.registers or operands[1] not in self.registers:
            self.status = Status.BAD_OPERAND
            return
        result = self.registers[operands[0]] - self.registers[operands[1]]
        if result > self.max_number or result < self.min_number:
            result = self.min_number + ((result - self.min_number) % (self.max_number - self.min_number + 1))
            self.flags["Overflow"] = True
        self.registers[operands[0]] = result
        self._set_flag(result)
    
    def _inc(self, operands):
        if len(operands) != 1 or operands[0] not in self.registers:
            self.status = Status.BAD_OPERAND
            return
        result = self.registers[operands[0]] + 1
        if result > self.max_number:
            result = self.min_number + ((result - self.min_number) % (self.max_number - self.min_number + 1))
            self.flags["Overflow"] = True
        self.registers[operands[0]] = result
        self._set_flag(result)
    
    def _dec(self, operands):
        if len(operands) != 1 or operands[0] not in self.registers:
            self.status = Status.BAD_OPERAND
            return
        result = self.registers[operands[0]] - 1
        if result < self.min_number:
            result = self.max_number + ((result - self.max_number) % (self.max_number - self.min_number + 1))
            self.flags["Overflow"] = True
        self.registers[operands[0]] = result
        self._set_flag(result)
    
    def _mov(self, operands):
        if len(operands) != 2 or operands[0] not in self.registers or operands[1] not in self.registers:
            self.status = Status.BAD_OPERAND
            return
        self.registers[operands[0]] = self.registers[operands[1]]
    
    def _set(self, operands):
        if len(operands) != 2 or operands[0] not in self.registers or not operands[1].lstrip('-').isdigit():
            self.status = Status.BAD_OPERAND
            return
        value = int(operands[1])
        if not (self.min_number <= value <= self.max_number):
            self.status = Status.BAD_OPERAND
            return
        self.registers[operands[0]] = value
    def _read(self, operands):
        if len(operands) != 2 or operands[0] not in self.registers:
            self.status = Status.BAD_OPERAND
            return
        if not operands[1].lstrip('-').isdigit():
            if operands[1] not in self.registers:
                self.status = Status.BAD_OPERAND
                return
            address = self.registers[operands[1]]
        else:
            address = int(operands[1])
        if not (0 <= address < len(self.memory)):
            self.status = Status.MEMORY_ERROR
            return
        self.registers[operands[0]] = self.memory[address]
    def _write(self, operands):
        if len(operands) != 2:
            self.status = Status.BAD_OPERAND
            return
        [address, val_reg] = operands
        if val_reg not in self.registers:
            self.status = Status.BAD_OPERAND
            return
        value = self.registers[val_reg]
        if not address.lstrip('-').isdigit():
            if address not in self.registers:
                self.status = Status.BAD_OPERAND
                return
            address = self.registers[address]
        else:
            address = int(address.strip())
        if 0 <= address < len(self.memory):
            self.memory[address] = value
        else:
            self.status = Status.MEMORY_ERROR

    
    def _set_flag(self, value: int):
        self.flags["Zero"] = (value == 0)
        self.flags["Sign"] = (value < 0)
        self.flags["Parity"] = ((bin(abs(value)).count('1') + (1 if value < 0 else 0)) % 2 == 0)
        self.flags["Overflow"] = self.flags["Overflow"] or (value > self.max_number or value < self.min_number)
    
    def _cmp(self, operands):
        if len(operands) != 2 or operands[0] not in self.registers or operands[1] not in self.registers:
            self.status = Status.BAD_OPERAND
            return
        result = self.registers[operands[0]] - self.registers[operands[1]]
        self._set_flag(result)
    
    def _jump(self, op, operands):
        if len(operands) != 1 or not operands[0].isdigit():
            self.status = Status.BAD_OPERAND
            return
        address = int(operands[0])
        if not (0 <= address < self.cur_code_len):
            self.status = Status.BAD_OPERAND
            return
        
        if op == Operation.JMP:
            self.registers["PC"] = address
        elif op == Operation.JZ and self.flags["Zero"]:
            self.registers["PC"] = address
        elif op == Operation.JNZ and not self.flags["Zero"]:
            self.registers["PC"] = address
        elif op == Operation.JO and self.flags["Overflow"]:
            self.registers["PC"] = address
        elif op == Operation.JNO and not self.flags["Overflow"]:
            self.registers["PC"] = address
        elif op == Operation.JS and self.flags["Sign"]:
            self.registers["PC"] = address
        elif op == Operation.JNS and not self.flags["Sign"]:
            self.registers["PC"] = address
        elif op == Operation.JP and self.flags["Parity"]:
            self.registers["PC"] = address
        elif op == Operation.JNP and not self.flags["Parity"]:
            self.registers["PC"] = address

cpu = KPU(15, {"AX", "BX", "CX"}, -10, 255)

# program [[SET A, 97], [OUTPUT A], [HLT]] 

program = [
    Instruction(Operation.SET, ["AX", "97"]),
    Instruction(Operation.OUTPUT, ["AX"]),
    Instruction(Operation.HLT, [])
]

# print(cpu.run_program(program))


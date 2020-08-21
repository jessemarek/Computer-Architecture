"""CPU functionality."""

import sys

# instruction machine codes
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
ADD = 0b10100000
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
ST = 0b10000100
CALL = 0b01010000
RET = 0b00010001
# SPRINT CHALLENGE
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
# SPRINT CHALLENGE STRETCH
AND = 0b10101000
OR = 0b10101010
XOR = 0b10101011
NOT = 0b01101001
SHL = 0b10101100
SHR = 0b10101101
MOD = 0b10100100

PRA = 0b01001000
INC = 0b01100101
DEC = 0b01100110
LD = 0b10000011

# stack pointer
SP = 7


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # memory

        self.reg = [0] * 8  # registers
        self.reg[SP] = 0xF4  # stack pointer

        self.pc = 0  # program counter
        self.running = False

        self.fl = 0b00000000  # flag register

        self.branchtable = {}   # instruction lookup table
        self.branchtable[HLT] = self.HLT
        self.branchtable[LDI] = self.LDI
        self.branchtable[PRN] = self.PRN
        self.branchtable[ADD] = self.ADD
        self.branchtable[MUL] = self.MUL
        self.branchtable[PUSH] = self.PUSH
        self.branchtable[POP] = self.POP
        self.branchtable[ST] = self.ST
        self.branchtable[CALL] = self.CALL
        self.branchtable[RET] = self.RET
        # SPRINT CHALLENGE
        self.branchtable[CMP] = self.CMP
        self.branchtable[JMP] = self.JMP
        self.branchtable[JEQ] = self.JEQ
        self.branchtable[JNE] = self.JNE
        # SPRINT CHALLENGE STRETCH
        self.branchtable[AND] = self.AND
        self.branchtable[OR] = self.OR
        self.branchtable[XOR] = self.XOR
        self.branchtable[NOT] = self.NOT
        self.branchtable[SHL] = self.SHL
        self.branchtable[SHR] = self.SHR
        self.branchtable[MOD] = self.MOD

        self.branchtable[PRA] = self.PRA
        self.branchtable[INC] = self.INC
        self.branchtable[DEC] = self.DEC
        self.branchtable[LD] = self.LD

    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print("usage: comp.py progname")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    line = line.strip()
                    temp = line.split()

                    if len(temp) == 0:
                        continue

                    if temp[0][0] == '#':
                        continue

                    try:
                        self.ram[address] = int(temp[0], 2)

                    except ValueError:
                        print(f"Invalid number: {temp[0]}")
                        sys.exit(1)

                    address += 1

        except FileNotFoundError:
            print(f"Couldn't open {sys.argv[1]}")
            sys.exit(2)

        if address == 0:
            print("Program was empty!")
            sys.exit(3)

    def alu(self, op, reg_a, reg_b=None):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            if reg_b == 0:
                print("Error: Cannot divide by 0")
                sys.exit(1)
            else:
                self.reg[reg_a] /= self.reg[reg_b]
        elif op == "INC":
            self.reg[reg_a] += 1
        elif op == "DEC":
            self.reg[reg_a] -= 1
        # SPRINT CHALLENGE
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 0b00000001
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b00000010
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 0b00000100

        # SPRINT CHALLENGE STRETCH
        elif op == "AND":
            self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]
        elif op == "OR":
            self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
        elif op == "XOR":
            self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]
        elif op == "NOT":
            self.reg[reg_a] = ~self.reg[reg_a]
        elif op == "SHL":
            self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]
        elif op == "SHR":
            self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b]
        elif op == "MOD":
            if reg_b == 0:
                print("Error: Cannot divide by 0")
                sys.exit(1)
            else:
                self.reg[reg_a] %= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    # instruction methods
    def HLT(self):
        self.running = False

    def LDI(self):
        address = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        self.reg[address] = value

    def PRN(self):
        address = self.ram_read(self.pc + 1)
        print(self.reg[address])

    def PRA(self):
        address = self.ram_read(self.pc + 1)
        print(chr(self.ram_read(self.reg[address])))

    def ADD(self):
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)
        self.alu("ADD", reg_a, reg_b)

    def MUL(self):
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)
        self.alu("MUL", reg_a, reg_b)

    def AND(self):
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)
        self.alu("AND", reg_a, reg_b)

    def OR(self):
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)
        self.alu("OR", reg_a, reg_b)

    def XOR(self):
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)
        self.alu("XOR", reg_a, reg_b)

    def NOT(self):
        reg_a = self.ram_read(self.pc + 1)
        self.alu("NOT", reg_a)

    def SHL(self):
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)
        self.alu("SHL", reg_a, reg_b)

    def SHR(self):
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)
        self.alu("SHR", reg_a, reg_b)

    def MOD(self):
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)
        self.alu("MOD", reg_a, reg_b)

    def CMP(self):
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)
        self.alu("CMP", reg_a, reg_b)

    def INC(self):
        reg_a = self.ram_read(self.pc + 1)
        self.alu("INC", reg_a)

    def DEC(self):
        reg_a = self.ram_read(self.pc + 1)
        self.alu("DEC", reg_a)

    def PUSH(self):
        self.reg[SP] -= 1
        sp = self.reg[SP]
        value = self.reg[self.ram_read(self.pc + 1)]
        self.ram_write(sp, value)

    def POP(self):
        sp = self.reg[SP]
        value = self.ram_read(sp)
        self.reg[self.ram_read(self.pc + 1)] = value
        self.reg[SP] += 1

    def ST(self):
        address = self.ram_read(self.pc + 1)
        value = self.reg[self.ram_read(self.pc + 2)]
        self.reg[address] = value

    def JMP(self):
        address = self.ram_read(self.pc + 1)
        self.pc = self.reg[address]

    def JEQ(self):
        equal = self.fl & 0b00000001

        if equal:
            self.JMP()
        else:
            self.pc = self.pc + 2

    def JNE(self):
        equal = self.fl & 0b00000001

        if not equal:
            self.JMP()
        else:
            self.pc = self.pc + 2

    def CALL(self):
        ret_addr = self.pc + 2

        self.reg[SP] -= 1
        self.ram_write(self.reg[SP], ret_addr)

        self.JMP()

    def RET(self):
        ret_addr = self.ram_read(self.reg[SP])

        self.reg[SP] += 1
        self.pc = ret_addr

    def LD(self):
        address = self.ram_read(self.pc + 1)
        value = self.reg[self.ram_read(self.pc + 2)]

        self.reg[address] = value

    # ---------------------------------

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def run(self):
        """Run the CPU."""
        self.running = True

        while self.running:
            # self.trace()
            # instruction register
            ir = self.ram_read(self.pc)

            # lookup the instruction from the branchtable and execute it
            if ir in self.branchtable:
                self.branchtable[ir]()
            else:
                print(f"Instruction {bin(ir)} not in Branch Table")

            instruction_sets_pc = ir & 0b00010000  # (if >> 4) & 1 works also
            # check to see if the instruction sets the PC
            if instruction_sets_pc:
                continue
            else:
                # move the PC dynamically based off the value
                # in the IR at bits AA
                end_of_instruction = ir >> 6
                self.pc += (end_of_instruction + 1)

import data as d
import random as rand

def Inst0NNN(NNN):
    if NNN != 0x0:
        print("NOT NEEDED")

# clear screen
def Inst00E0():
    d.graphics = bytearray(2048)
    d.drawFlag = True

# return from subroutine
def Inst00EE():
    if d.sp <= 0:
        raise Exception('No Subroutine to return to')
    d.sp -= 1
    d.pc = d.stack[d.sp]
    d.stack[d.sp] = 0

# jump to adress NNN
def Inst1NNN(NNN):
     d.pc = NNN -2

# call subroutine at NNN
def Inst2NNN(NNN):
    if d.sp >= 15:
        raise Exception('Max Stacksize reached')
    d.stack[d.sp] = d.pc
    d.sp += 1
    d.pc = NNN -2

# skip next instr if reg X == NN
def Inst3XNN(X,NN):
    if d.register[X] == NN:
        d.pc += 2
        if d.pc >= 4096:
            raise Exception('Out of Memory')

# skip next instr if reg X != NN
def Inst4XNN(X,NN):
    if d.register[X] != NN:
        d.pc += 2
        if d.pc >= 4096:
            raise Exception('Out of Memory')

# skip next instr if reg X == reg Y
def Inst5XY0(X,Y):
    if d.register[X] == d.register[Y]:
        d.pc += 2
        if d.pc >= 4096:
            raise Exception('Out of Memory')

# set reg X to NN
def Inst6XNN(X,NN):
    d.register[X] = NN

# adds NN to reg X
def Inst7XNN(X,NN):
    h = d.register[X] + NN
    d.register[X] = h % 256

# set reg X to value of reg Y
def Inst8XY0(X,Y):
    d.register[X] = d.register[Y]

# set reg X to reg X bitOr reg Y
def Inst8XY1(X,Y):
    d.register[X] = d.register[X] | d.register[Y]

# set reg X to reg X bitAnd reg Y
def Inst8XY2(X,Y):
    d.register[X] = d.register[X] & d.register[Y]

# set reg X to reg X bitXor reg Y
def Inst8XY3(X,Y):
    d.register[X] = d.register[X] ^ d.register[Y]

# set reg X to reg X + reg Y (carry flag is set)
def Inst8XY4(X,Y):
    h = d.register[X] + d.register[Y]
    d.register[15] = h > 255
    d.register[X] = h % 256

# set reg X to reg X - reg Y (carry flag is set)
def Inst8XY5(X,Y):
    h = d.register[X] - d.register[Y]
    d.register[15] = h >= 0
    d.register[X] = (h + 256) % 256

# right bitshift
def Inst8XY6(X):
    d.register[15] = d.register[X] & 1
    d.register[X] = d.register[X] >> 1

# set reg X to reg X - reg Y (carry flag is set)
def Inst8XY7(X,Y):
    h = d.register[Y] - d.register[X]
    d.register[15] = h >= 0
    d.register[X] = (h + 256) % 256

# left bitshift
def Inst8XYE(X):
    d.register[15] = (d.register[X] & 0x80) >> 7
    d.register[X] = (d.register[X] << 1) % 256

# skip next instr if reg X != reg Y
def Inst9XY0(X,Y):
    if d.register[X] != d.register[Y]:
        d.pc += 2
        if d.pc >= 0xFFF:
            raise Exception('Out of Memory')

# set iReg to address NNN
def InstANNN(NNN):
    d.iReg = NNN

# jumps to address reg 0 + NNN
def InstBNNN(NNN):
    d.pc = d.register[0] + NNN -2
    if d.pc >= 0xFFF:
        raise Exception('Out of Memory')

# sets reg X to bitAnd on NN and random Number 0 to 256
def InstCXNN(X,NN):
    d.register[X] = int(rand.randint(0,0xFF)) & NN

# draw sprite from address iReg at Coord X,Y
def InstDXYN(X,Y,N):
    d.register[15] = 0
    for y in range(N):
        if d.register[Y]+y > 0x1F:     # end of ScreenHeight
            break
        byte = d.memory[d.iReg+y]
        for x in range(8):
            if d.register[X]+x > 0x3F:     # end of Screenwidth
                break
            pos = ((d.register[Y]+y)*64)+d.register[X]+x
            if (byte & (0x80 >> x)) != 0:
                if d.graphics[pos] != 0:
                    d.register[0xF] = 1      # collision detected
                    d.graphics[pos] = 0
                else:
                    d.graphics[pos] = 1
    d.drawFlag = True

# skips next instr if kex in reg X is pressed
def InstEX9E(X):
    if d.keys[d.register[X]]:
        d.pc += 2
        if d.pc >= 0xFFF:
            raise Exception('Out of Memory')

# skips next instr if kex in reg X is not pressed
def InstEXA1(X):
    if not d.keys[d.register[X]]:
        d.pc += 2
        if d.pc >= 0xFFF:
            raise Exception('Out of Memory')

# sets reg X to delaytimer
def InstFX07(X):
    d.register[X] = d.delayTimer

# wait for certain key press
def InstFX0A(X):
    keyPressed = 0x10
    for c in range(0x10):
        if d.keys[c] != 0:
            keyPressed = c
            break
    if c < 0x10:
        d.register[X] = c
    else:
        d.pc -= 2


# set delaytimer to value of reg X
def InstFX15(X):
    d.delayTimer = d.register[X]

# set soundtimer to value of reg X
def InstFX18(X):
    d.soundTimer = d.register[X]

# add rex X to iReg
def InstFX1E(X):
    d.iReg += d.register[X]
    if d.iReg >= 0xFFF:
        raise Exception('Out of Memory')

def InstFX29(X):
    d.iReg = 0x050 + d.register[X]*5

def InstFX33(X):
    d.memory[d.iReg] = int(d.register[X] /100)
    d.memory[d.iReg+1] = int((d.register[X] /10) % 10)
    d.memory[d.iReg+2] = int((d.register[X] %100) % 10)

def InstFX55(X):
    for i in range(X+1):
        d.memory[d.iReg + i] = d.register[i]

def InstFX65(X):
    for i in range(X+1):
        d.register[i] = d.memory[d.iReg + i]
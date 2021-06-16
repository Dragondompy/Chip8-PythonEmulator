from pynput.keyboard import Key, Listener, KeyCode
import math
import time
import data
import cpuCore as core

def loadProgramm(filename):
    with open(filename, "r+b") as f:
        i = 0
        while (b := f.read(1)):
            if b == 0xf085:
                print(b)
            data.memory[0x200+i] = ord(b)
            i += 1

def on_press(key):
    global keyList
    if key == KeyCode.from_char('x'):
        data.keys[0] = 1
        if not (0 in keyList):
            keyList.append(0)
    elif key == KeyCode.from_char('1'):
        data.keys[1] = 1
        if not (1 in keyList):
            keyList.append(1)
    elif key == KeyCode.from_char('2'):
        data.keys[2] = 1
        if not (2 in keyList):
            keyList.append(2)
    elif key == KeyCode.from_char('3'):
        data.keys[3] = 1
        if not (3 in keyList):
            keyList.append(3)
    elif key == KeyCode.from_char('q'):
        data.keys[4] = 1
        if not (4 in keyList):
            keyList.append(4)
    elif key == KeyCode.from_char('w'):
        data.keys[5] = 1
        if not (5 in keyList):
            keyList.append(5)
    elif key == KeyCode.from_char('e'):
        data.keys[6] = 1
        if not (6 in keyList):
            keyList.append(6)
    elif key == KeyCode.from_char('a'):
        data.keys[7] = 1
        if not (7 in keyList):
            keyList.append(7)
    elif key == KeyCode.from_char('s'):
        data.keys[8] = 1
        if not (8 in keyList):
            keyList.append(8)
    elif key == KeyCode.from_char('d'):
        data.keys[9] = 1
        if not (9 in keyList):
            keyList.append(9)
    elif key == KeyCode.from_char('y'):
        data.keys[10] = 1
        if not (10 in keyList):
            keyList.append(10)
    elif key == KeyCode.from_char('c'):
        data.keys[11] = 1
        if not (11 in keyList):
            keyList.append(11)
    elif key == KeyCode.from_char('4'):
        data.keys[12] = 1
        if not (12 in keyList):
            keyList.append(12)
    elif key == KeyCode.from_char('r'):
        data.keys[13] = 1
        if not (13 in keyList):
            keyList.append(13)
    elif key == KeyCode.from_char('f'):
        data.keys[14] = 1
        if not (14 in keyList):
            keyList.append(14)
    elif key == KeyCode.from_char('v'):
        data.keys[15] = 1
        if not (15 in keyList):
            keyList.append(15)

def on_release(key):
    if key == KeyCode.from_char('x'):
        keyList.remove(0)
    elif key == KeyCode.from_char('1'):
        keyList.remove(1)
    elif key == KeyCode.from_char('2'):
        keyList.remove(2)
    elif key == KeyCode.from_char('3'):
        keyList.remove(3)
    elif key == KeyCode.from_char('q'):
        keyList.remove(4)
    elif key == KeyCode.from_char('w'):
        keyList.remove(5)
    elif key == KeyCode.from_char('e'):
        keyList.remove(6)
    elif key == KeyCode.from_char('a'):
        keyList.remove(7)
    elif key == KeyCode.from_char('s'):
        keyList.remove(8)
    elif key == KeyCode.from_char('d'):
        keyList.remove(9)
    elif key == KeyCode.from_char('y'):
        keyList.remove(10)
    elif key == KeyCode.from_char('c'):
        keyList.remove(11)
    elif key == KeyCode.from_char('4'):
        keyList.remove(12)
    elif key == KeyCode.from_char('r'):
        keyList.remove(13)
    elif key == KeyCode.from_char('f'):
        keyList.remove(14)
    elif key == KeyCode.from_char('v'):
        keyList.remove(15)

def getKeys():
    for key in keyList:
        data.keys[key] = 1

def clearKeys():
    for i in range(0xF):
        data.keys[i] = 0

def getOpcode():
    data.opcode = (data.memory[data.pc] << 8) | data.memory[data.pc+1]

def con4(a,b,c,d):
    return (a << 0xC)|(b << 0x8)|(c << 0x4 )|d

def con3(a,b,c):
    return (a << 0x8)|(b << 0x4 )|c

def con2(a,b):
    return (a << 0x4 )|b

def executeOpcode():
    a = (data.opcode & 0xF000) >> 0xC
    b = (data.opcode & 0x0F00) >> 0x8
    c = (data.opcode & 0x00F0) >> 0x4
    d = (data.opcode & 0x000F) >> 0x0

    if a == 0x0:
        if con2(c,d) == 0xE0:
            core.Inst00E0()
        elif con2(c,d) == 0xEE:
            core.Inst00EE()
        else:
            core.Inst0NNN(con3(b,c,d))
    elif a == 0x1:
        core.Inst1NNN(con3(b,c,d))
    elif a == 0x2:
        core.Inst2NNN(con3(b,c,d))
    elif a == 0x3:
        core.Inst3XNN(b, con2(c,d))
    elif a == 0x4:
        core.Inst4XNN(b, con2(c,d))
    elif a == 0x5:
        core.Inst5XY0(b, c)
    elif a == 0x6:
        core.Inst6XNN(b, con2(c,d))
    elif a == 0x7:
        core.Inst7XNN(b, con2(c,d))
    elif a == 0x8:
        if d == 0x0:
            core.Inst8XY0(b, c)
        elif d == 0x1:
            core.Inst8XY1(b, c)
        elif d == 0x2:
            core.Inst8XY2(b, c)
        elif d == 0x3:
            core.Inst8XY3(b, c)
        elif d == 0x4:
            core.Inst8XY4(b, c)
        elif d == 0x5:
            core.Inst8XY5(b, c)
        elif d == 0x6:
            core.Inst8XY6(b)
        elif d == 0x7:
            core.Inst8XY7(b, c)
        elif d == 0xE:
            core.Inst8XYE(b)
        else:
            raise Exception("instruction " + hex(data.opcode) + " not found")
    elif a == 0x9:
        core.Inst9XY0(b, c)
    elif a == 0xA:
        core.InstANNN(con3(b,c,d))
    elif a == 0xB:
        core.InstBNNN(con3(b,c,d))
    elif a == 0xC:
        core.InstCXNN(b, con2(c,d))
    elif a == 0xD:
        core.InstDXYN(b, c, d)
    elif a == 0xE:
        if c == 0x9:
            core.InstEX9E(b)
        elif c == 0xA:
            core.InstEXA1(b)
        else:
            raise Exception("instruction " + hex(data.opcode) + " not found")
    elif a == 0xF:
        if con2(c, d) == 0x07:
            core.InstFX07(b)
        elif con2(c, d) == 0x0A:
            core.InstFX0A(b)
        elif con2(c, d) == 0x15:
            core.InstFX15(b)
        elif con2(c, d) == 0x18:
            core.InstFX18(b)
        elif con2(c, d) == 0x1E:
            core.InstFX1E(b)
        elif con2(c, d) == 0x29:
            core.InstFX29(b)
        elif con2(c, d) == 0x33:
            core.InstFX33(b)
        elif con2(c, d) == 0x55:
            core.InstFX55(b)
        elif con2(c, d) == 0x65:
            core.InstFX65(b)
        else:
            raise Exception("instruction " + hex(data.opcode) + " not found")
    else:
        raise Exception("instruction " + hex(data.opcode) + " not found")
    data.pc += 2
    if data.pc >= 0xFFF:
        raise Exception('Out of Memory')

def updateTimers():
    if data.delayTimer > 0:
        data.delayTimer -= 1
    if data.soundTimer > 0:
        data.soundTimer -= 1

def drawGraphics():
    start = time.time()
    buffer = "________________________________________________________________________"
    buffer += "\n"
    for y in range(32):
        buffer += "|"
        for x in range(64):
            if data.graphics[y*64+x] == 0:
                buffer += " "
            else:
                buffer += "8"
        buffer += "|\n"
    buffer += "------------------------------------------------------------------------"
    print(buffer)
    f = 0

def emulCycle():
    getOpcode()
    getKeys()
    executeOpcode()
    clearKeys()
    getKeys()

if __name__ == "__main__":
    data.initialize()

    print("Programm to load into Chip8")
    file = input()
    loadProgramm(file)

    #start Keyboard listener
    global keyList
    keyList = [0] * 0
    listener = Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()

    # Timings
    cpuClock = 1/500
    opPerCircle = 5
    frame60 = 1/60
    frameDelta = 0
    deltaTime = 0
    rest = 0
    start = time.time()

    frame60Number = 0
    framenumber = 0
    startTime = time.time()

    data.opcode = 0x1
    while(data.opcode != 0x0):
        newStart = time.time()
        deltaTime = newStart - start
        start = newStart
        frameDelta += deltaTime

        deltaTime += rest
        opPerCircle = math.floor(deltaTime/cpuClock)
        rest = deltaTime-(opPerCircle*cpuClock)

        for i in range(opPerCircle):
            emulCycle()
            framenumber += 1
            if data.drawFlag:
                drawGraphics() 
                data.drawFlag = False
                print(frame60Number/(time.time()-startTime))
                print(framenumber/(time.time()-startTime))
                #print(opPerCircle)
        
        if frameDelta >= frame60:
            updateTimers()
            frameDelta -= frame60
            frame60Number += 1

    listener.stop

#01110000
#10001000
#10001000
#01110000
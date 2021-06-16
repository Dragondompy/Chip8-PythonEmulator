def loadFontSet():
    global memory
    # Fontset
    fontSet = [
        0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
        0x20, 0x60, 0x20, 0x20, 0x70, # 1
        0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
        0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
        0x90, 0x90, 0xF0, 0x10, 0x10, # 4
        0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
        0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
        0xF0, 0x10, 0x20, 0x40, 0x40, # 7
        0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
        0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
        0xF0, 0x90, 0xF0, 0x90, 0x90, # A
        0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
        0xF0, 0x80, 0x80, 0x80, 0xF0, # C
        0xE0, 0x90, 0x90, 0x90, 0xE0, # D
        0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
        0xF0, 0x80, 0xF0, 0x80, 0x80  # F
    ]

    # loadfontset
    i = 0
    for font in fontSet:
        memory[0x50+i] = font
        i += 1

def initialize():
    # MemoryObject
    memoryObject = bytearray(4096)
    # Create MemoryView of te Bytearray for faster access
    global memory
    memory = memoryview(memoryObject)

    # current opcode
    global opcode
    opcode = int(0)

    # current Index Register
    global iReg
    iReg = int(0)

    # current programm counter
    global pc
    pc  = int(0x200) # Programm starts at 0x200 first 0x000 to 0x1FF is reserved

    # Registers 
    registerObject = bytearray(16)
    # Create MemoryView of te Bytearray for faster access
    global register
    register = memoryview(registerObject)

    # graphicBuffer
    graphicObject = bytearray(2048)
    # Create MemoryView of te Bytearray for faster access
    global graphics
    graphics = memoryview(graphicObject)

    # current Index Register
    global drawFlag
    drawFlag = False

    # timers
    global delayTimer
    delayTimer = int(0)
    global soundTimer
    soundTimer = int(0)

    #stack and stackpointer
    global stack
    stack = [0]*16
    global sp
    sp = int(0)

    # KeyArray
    keysObject = bytearray(16)
    # Create MemoryView of te Bytearray for faster access
    global keys
    keys = memoryview(keysObject)

    loadFontSet()

from collections import deque
import sys

# Returns shifted value of the operand, and proper flags
def shiftLeft(a):
    carryFlag = False
    zeroFlag = True
    signedFlag = False
    # Firstly operand is converted to binary
    binA = bin(int(a, 16))[2:].zfill(16)
    # Determining CF by looking 16th bit
    if binA[0] == "1":
        carryFlag = True
    # Performing shifting
    shifted = binA[1:] + "0"
    # Determining ZF by checking if it contains 1 
    if shifted.__contains__("1"):
        zeroFlag = False
    # Determining SF by checking if its 16th bit is 1 
    if shifted[0] == "1":
        signedFlag = True
    return str(hex(int(shifted, 2)))[2:], signedFlag, zeroFlag, carryFlag 

# Returns shifted value of the operand, and proper flags
def shiftRight(a):
    zeroFlag = True
    signedFlag = False
    # Firstly operand is converted to binary
    binA = bin(int(a, 16))[2:].zfill(16)
    # Performing shifting
    shifted = "0" + binA[:-1]
    # Determining ZF by checking if it contains 1 
    if shifted.__contains__("1"):
        zeroFlag = False
    # Determining SF by checking if its 16th bit is 1 
    if shifted[0] == "1":
        signedFlag = True
    return str(hex(int(shifted, 2)))[2:], signedFlag, zeroFlag

# A function checks SF and ZF for result of instructions 
def zeroSignFlag(a):
    signFlag = False
    zeroFlag = True
    # Operand is converted to binary
    binA = bin(a)[2:].zfill(16)
    # Determining SF by checking if 16th bit is 1
    if(binA[0] == "1"):
        signFlag = True
    # Determining ZF by checking if it contains 1
    if(binA.__contains__("1")):
        zeroFlag = False
    return signFlag, zeroFlag

# Returns XOR of given values, and proper flags
def xorFunc(a, b):
    # Hex to int
    intA = int(a, 16)
    intB = int(b, 16)
    # Getting XOR by using bitwise operator
    XOR = intA ^ intB
    # Checking flags
    sign, zero = zeroSignFlag(XOR)
    return str(hex(XOR))[2:].zfill(4), sign, zero

# Returns AND of given values, and proper flags
def andFunc(a, b):
    # Hex to int
    intA = int(a, 16)
    intB = int(b, 16)
    # Getting AND by using bitwise operator
    AND = intA & intB
    # Checking flags
    sign, zero = zeroSignFlag(AND)
    return str(hex(AND))[2:].zfill(4), sign, zero

# Returns OR of given values, and proper flags
def orFunc(a, b):
    # Hex to int
    intA = int(a, 16)
    intB = int(b, 16)
    # Getting OR by using bitwise operator
    OR = intA | intB
    # Checking flags
    sign, zero = zeroSignFlag(OR)
    return str(hex(OR))[2:].zfill(4), sign, zero

# Returns NOT of given value, and proper flags
def notFunc2(a):
    # Hex to int
    a = int(a,16)
    # Int to binary
    stringversion = bin(a)[2:].zfill(16)
    # Taking its not value
    stringversion = notFunc(stringversion)
    # Setting flags according to result
    signFlag = False
    zeroFlag = True
    # Determining SF by checking if 16th bit is 1
    if(stringversion[0] == "1"):
        signFlag = True
    # Determining ZF by checking if it contains 1
    if(stringversion.__contains__("1")):
        zeroFlag = False
    return str(hex(int(stringversion, 2)))[2:].zfill(4), signFlag, zeroFlag

# Returns not of given binary value
def notFunc(a):
    a = a.replace("0", "2")
    a = a.replace("1", "0")
    a = a.replace("2", "1")
    return a

# Returns a - b and proper flags, b's default value is set to 1 for using also as DEC
def substraction(a, b = "1"):
    # Hex to int
    intA = int(a, 16)
    intB = int(b, 16)
    # Int to binary
    binB = bin(intB)[2:].zfill(16)
    cflag = False
    # Taking not of B for performing substraction in form of A + (-B) + 1
    notB = notFunc(binB)
    NotVersionValue =  int(notB, 2)
    initally = NotVersionValue + 1 

    # Getting rid of carried value
    if(initally >= 65536):
        initally -= 65536
    result = initally + intA   

    if(result < -65535):
        result += 65535
        cflag == True
        check = bin(result)[2:].zfill(16)
        # Checking SF and ZF
        signflag, zeroflag = zeroSignFlag(int(check, 2))
        return hex(int((bin(result)[2:].zfill(16)), 2))[2:].zfill(4), cflag, signflag, zeroflag
    
    if(result > 65535):
        result -= 65536
        cflag = True
        check = bin(result)[2:].zfill(16)
        # Checking SF and ZF
        signflag, zeroflag = zeroSignFlag(int(check,2))
        return hex(int((bin(result)[2:].zfill(16)), 2))[2:].zfill(4), cflag, signflag, zeroflag
    
    else:
        check = bin(result)[2:].zfill(16)
        # Checking SF and ZF
        signflag, zeroflag = zeroSignFlag(int(check,2))
        return hex(int((bin(result)[2:].zfill(16)), 2))[2:].zfill(4), cflag, signflag, zeroflag  

# Returns a + b and flags, b's default value is set to 1 for using as INC
def adding(a, b = "1"):
    # Hex to int
    temp1 = int(a, 16)
    temp2 = int(b, 16)
    result = temp1 + temp2
    cflag = False
    
    # Checking carry flag, and getting rid of carried value
    if result > 65535:
        cflag = True
        result -= 65536
        check = bin(result)[2:].zfill(16)
        # Setting SF and ZF
        signflag,zeroflag = zeroSignFlag(int(check,2))
        result = str(hex(result))[2:].zfill(4)
        return result.upper(), cflag, signflag, zeroflag
    else:
        check = bin(result)[2:].zfill(16)
        # Setting SF and ZF
        signflag,zeroflag = zeroSignFlag(int(check,2))
        result = str(hex(result))[2:].zfill(4)
        return result.upper(), cflag, signflag, zeroflag

# Returns opcode, addressing mode and operand of given instructions
def instruction(instr):
    # Opcode + addressing mode part
    value = instr[2:]
    # Operand
    instr = instr[:2]
    # Hex to int
    intInstr = int(instr, 16)
    # Getting addressing mode
    addres = intInstr % 4
    # Getting instruction Code
    intInstr -= addres
    intInstr /= 4
    intInstr = int(intInstr)
    return [str(hex(intInstr))[2:].upper(), str(addres), str(value)]

# A dictionary used for registers and its current values
dict_Register = {
    "0000" : "0000",
    "0001" : "",
    "0002" : "",
    "0003" : "",
    "0004" : "",
    "0005" : "",
    "0006" : "ffff",
}

# Memory used for addresses and its current values
Memory = {

}


instructions = [] 

# Taking input file as an arg
inputFile = sys.argv[1]
with open(inputFile, "r") as file:
    for line in file:
        # Getting rid of unnecessary blank spaces
        stripped_line = line.strip()
        instructions.append(stripped_line)

# Producing output file
outputFile = inputFile[:-3] + "txt"
outFile = open(outputFile, "w")

# Creating Stack
stack = deque()

# Flags
ZF = False
SF = False
CF = False

# Following program counter
i = 0

while i < len(instructions):

    # Accessing the current instruction
    stripped_line = instructions[i]
    i += 1
    # Extracting opcode, addressing mode and operand
    Array = instruction(stripped_line)
    instructionCode = Array[0]
    adressingMode = Array[1]
    operand = Array[2]
    
    # For LOAD instruction and "00", "01", "10", "11" addressing modes
    # Loading operand to A register
    if(instructionCode == "2"):
        if(adressingMode == "0"):
            dict_Register["0001"] = operand
        if(adressingMode == "1"):
            dict_Register["0001"] = dict_Register.get(operand)
        if(adressingMode == "2"):
            dict_Register["0001"] = Memory.get(dict_Register.get(operand))    
            # If accessed memory is undefined, then it is taken as 0000
            if(not dict_Register["0001"]):
                dict_Register["0001"] = "0000"
        if(adressingMode == "3"):
            dict_Register["0001"] = Memory.get(operand)
            # If accessed memory is undefined, then it is taken as 0000
            if(not dict_Register["0001"]):
                dict_Register["0001"] = "0000"

    # For STORE instruction and "01", "10", "11" addressing modes
    # Stores values in A register to the operand
    elif(instructionCode == "3"):
        if(adressingMode == "1"):
            dict_Register[operand] = dict_Register["0001"]
        if(adressingMode == "2"):
            Memory[dict_Register[operand]] = dict_Register["0001"]
        if(adressingMode == "3"):
            Memory[operand] = dict_Register["0001"]

    # For ADD instruction and "00", "01", "10", "11" addressing modes    
    elif(instructionCode=="4"):
        if(adressingMode=="0"):
            dict_Register["0001"], CF, SF, ZF = adding(dict_Register["0001"],operand)
        if(adressingMode=="1"):
            dict_Register["0001"], CF, SF, ZF = adding(dict_Register["0001"],dict_Register[operand])    
        if(adressingMode=="2"):
            dict_Register["0001"], CF, SF, ZF = adding(dict_Register["0001"],Memory[dict_Register[operand]])     
        if(adressingMode=="3"):
            dict_Register["0001"], CF, SF, ZF = adding(dict_Register["0001"],Memory[operand]) 

    # For SUB instruction and "00", "01", "10", "11" addressing modes  
    elif(instructionCode=="5"):
        if(adressingMode=="0"):
            dict_Register["0001"], CF, SF, ZF = substraction(dict_Register["0001"],operand)
        if(adressingMode=="1"):
            dict_Register["0001"], CF, SF, ZF = substraction(dict_Register["0001"],dict_Register[operand])    
        if(adressingMode=="2"):
            dict_Register["0001"], CF, SF, ZF = substraction(dict_Register["0001"],Memory[dict_Register[operand]])     
        if(adressingMode=="3"):
            dict_Register["0001"], CF, SF, ZF = substraction(dict_Register["0001"],Memory[operand])     

    # For INC instruction and "00", "01", "10", "11" addressing modes  
    elif(instructionCode=="6"):
        if(adressingMode=="0"):
            operand, CF, SF, ZF = adding(operand)
        if(adressingMode=="1"):
            dict_Register[operand], CF, SF, ZF = adding(dict_Register[operand])    
        if(adressingMode=="2"):
            Memory[dict_Register[operand]], CF, SF, ZF = adding(Memory[dict_Register[operand]])     
        if(adressingMode=="3"):
            Memory[operand], CF, SF, ZF = adding(Memory[operand]) 

    # For DEC instruction and "00", "01", "10", "11" addressing modes  
    elif(instructionCode=="7"):
        if(adressingMode=="0"):
            operand, CF, SF, ZF = substraction(operand)
        if(adressingMode=="1"):            
            dict_Register[operand], CF, SF, ZF = substraction(dict_Register[operand])                 
        if(adressingMode=="2"):
            Memory[dict_Register[operand]], CF, SF, ZF = substraction(Memory[dict_Register[operand]])     
        if(adressingMode=="3"):
            Memory[operand], CF, SF, ZF = substraction(Memory[operand]) 

    # For XOR instruction and "00", "01", "10", "11" addressing modes  
    elif(instructionCode=="8"):
        if(adressingMode=="0"):
            dict_Register["0001"], SF, ZF = xorFunc(dict_Register["0001"],operand)
        if(adressingMode=="1"):
            dict_Register["0001"], SF, ZF = xorFunc(dict_Register["0001"],dict_Register[operand])    
        if(adressingMode=="2"):
            dict_Register["0001"], SF, ZF = xorFunc(dict_Register["0001"],Memory[dict_Register[operand]])     
        if(adressingMode=="3"):
            dict_Register["0001"], SF, ZF = xorFunc(dict_Register["0001"],Memory[operand]) 

    # For AND instruction and "00", "01", "10", "11" addressing modes              
    elif(instructionCode=="9"):
        if(adressingMode=="0"):
            dict_Register["0001"], SF, ZF = andFunc(dict_Register["0001"],operand)
        if(adressingMode=="1"):
            dict_Register["0001"], SF, ZF = andFunc(dict_Register["0001"],dict_Register[operand])    
        if(adressingMode=="2"):
            dict_Register["0001"], SF, ZF = andFunc(dict_Register["0001"],Memory[dict_Register[operand]])     
        if(adressingMode=="3"):
            dict_Register["0001"], SF, ZF = andFunc(dict_Register["0001"],Memory[operand]) 

    # For OR instruction and "00", "01", "10", "11" addressing modes  
    elif(instructionCode=="A"):
        if(adressingMode=="0"):
            dict_Register["0001"], SF, ZF = orFunc(dict_Register["0001"],operand)
        if(adressingMode=="1"):
            dict_Register["0001"], SF, ZF = orFunc(dict_Register["0001"],dict_Register[operand])    
        if(adressingMode=="2"):
            dict_Register["0001"], SF, ZF = orFunc(dict_Register["0001"],Memory[dict_Register[operand]])     
        if(adressingMode=="3"):
            dict_Register["0001"], SF, ZF = orFunc(dict_Register["0001"],Memory[operand]) 

    # For NOT instruction and "00", "01", "10", "11" addressing modes  
    elif(instructionCode=="B"):
        if(adressingMode=="0"):
            dict_Register["0001"], SF, ZF = notFunc2(operand)
        if(adressingMode=="1"):
            dict_Register["0001"], SF, ZF = notFunc2(dict_Register[operand])    
        if(adressingMode=="2"):
            dict_Register["0001"], SF, ZF = notFunc2(Memory[dict_Register[operand]])     
        if(adressingMode=="3"):
            dict_Register["0001"], SF, ZF = notFunc2(Memory[operand]) 

    # For SHL instruction and "00", "01", "10", "11" addressing modes  
    elif(instructionCode=="C"):
        if(adressingMode=="0"):
            dict_Register["0001"], SF, ZF, CF = shiftLeft(operand)
        if(adressingMode=="1"):
            dict_Register["0001"], SF, ZF, CF = shiftLeft(dict_Register[operand])    
        if(adressingMode=="2"):
            dict_Register["0001"], SF, ZF, CF = shiftLeft(Memory[dict_Register[operand]])     
        if(adressingMode=="3"):
            dict_Register["0001"], SF, ZF, CF = shiftLeft(Memory[operand]) 

    # For SHR instruction and "00", "01", "10", "11" addressing modes  
    elif(instructionCode=="D"):
        if(adressingMode=="0"):
            dict_Register["0001"], SF, ZF = shiftRight(operand)
        if(adressingMode=="1"):
            dict_Register["0001"], SF, ZF = shiftRight(dict_Register[operand])    
        if(adressingMode=="2"):
            dict_Register["0001"], SF, ZF = shiftRight(Memory[dict_Register[operand]])     
        if(adressingMode=="3"):
            dict_Register["0001"], SF, ZF = shiftRight(Memory[operand]) 

    # For NOP instruction
    elif(instructionCode=="E"):
        continue

    # For PUSH instruction and "01", "10", "11" addressing modes
    # Pushes operand to the stack
    # Decrements S by two
    elif(instructionCode=="F"):
        if(adressingMode=="1"):
            stack.append(dict_Register[operand])
            dict_Register["0006"], t, y,z = substraction(dict_Register["0006"],"2")
        if(adressingMode=="2"):
            stack.append(Memory[dict_Register[operand]])
            dict_Register["0006"], t, y, z = substraction(dict_Register["0006"],"2")    
        if(adressingMode=="3"):
            stack.append(Memory[operand])
            dict_Register["0006"], t, y, z = substraction(dict_Register["0006"],"2") 

    # For POP instruction and "01", "10", "11" addressing modes
    # Pops operand from the stack
    # Increments S by two
    elif(instructionCode=="10"):
        if(adressingMode=="1"):
            dict_Register[operand]=stack.pop()
            dict_Register["0006"], t, y,z = adding(dict_Register["0006"],"2")
        if(adressingMode=="2"):
            Memory[dict_Register[operand]]=stack.pop()
            dict_Register["0006"], t, y, z = adding(dict_Register["0006"],"2")    
        if(adressingMode=="3"):
            Memory[operand]=stack.pop()
            dict_Register["0006"], t, y, z = adding(dict_Register["0006"],"2")     
    
    # For CMP instruction and "00", "01", "10", "11" addressing modes
    elif(instructionCode == "11"):
        CF = False
        SF = False
        ZF = False

        if(adressingMode == "0"):
            if(int(dict_Register["0001"], 16) == int(operand,16)):
                ZF = True
            if(int(dict_Register["0001"], 16) > int(operand,16)):
                CF = True
            if(int(dict_Register["0001"], 16) < int(operand,16)):
                SF = True                
        
        if(adressingMode == "1"):
            if(int(dict_Register["0001"], 16) == int(dict_Register[operand], 16)):
                ZF = True
            if(int(dict_Register["0001"], 16) > int(dict_Register[operand], 16)):
                CF = True  
            if(int(dict_Register["0001"], 16) < int(dict_Register[operand], 16)):
                SF = True         

        if(adressingMode == "2"):
            if(int(dict_Register["0001"], 16) == int(Memory[dict_Register[operand]], 16)):
                ZF = True
            if(int(dict_Register["0001"], 16) > int(Memory[dict_Register[operand]], 16)):
                CF = True
            if(int(dict_Register["0001"], 16) < int(Memory[dict_Register[operand]], 16)):
                SF = True    
        
        if(adressingMode == "3"):
            if(int(dict_Register["0001"], 16) == int(Memory[operand],16)):
                ZF = True 
            if(int(dict_Register["0001"], 16) > int(Memory[operand],16)):
                CF = True  
            if(int(dict_Register["0001"], 16) < int(Memory[operand],16)):
                SF = True              

    # For JMP instruction and "00", "01", "10", "11" addressing modes
    elif(instructionCode == "12"):
        if(adressingMode == "0"):
            i = int(int(operand,16)/3)
        if(adressingMode == "1"):
            i = int(int(dict_Register[operand],16)/3)
        if(adressingMode == "2"):
            i = int(int(Memory[dict_Register[operand]],16)/3)
        if(adressingMode == "3"):
            i = int(int(Memory[operand],16)/3)
    
    # For JZ and JE instructions and "00", "01", "10", "11" addressing modes
    elif(instructionCode == "13"):
        if(ZF):
            if(adressingMode == "0"):
                i = int(int(operand,16)/3)
            if(adressingMode == "1"):
                i = int(int(dict_Register[operand],16)/3)
            if(adressingMode == "2"):
                i = int(int(Memory[dict_Register[operand]],16)/3)
            if(adressingMode == "3"):
                i = int(int(Memory[operand],16)/3)

    # For JNZ and JNE instructions and "00", "01", "10", "11" addressing modes
    elif(instructionCode == "14"):
        if(not ZF):
            if(adressingMode == "0"):
                i = int(int(int(operand,16)/3))
            if(adressingMode == "1"):
                i = int(int(int(dict_Register[operand],16)/3))
            if(adressingMode == "2"):
                i = int(int(int(Memory[dict_Register[operand]],16)/3))
            if(adressingMode == "3"):
                i = int(int(int(Memory[operand],16)/3))

    # For JC instruction and "00", "01", "10", "11" addressing modes
    elif(instructionCode == "15"):
        if(CF):
            if(adressingMode == "0"):
                i = int(int(operand,16)/3)
            if(adressingMode == "1"):
                i = int(int(dict_Register[operand],16)/3)
            if(adressingMode == "2"):
                i = int(int(Memory[dict_Register[operand]],16)/3)
            if(adressingMode == "3"):
                i = int(int(Memory[operand],16)/3)

    # For JNC instruction and "00", "01", "10", "11" addressing modes
    elif(instructionCode == "16"):
        if(not CF):
            if(adressingMode == "0"):
                i = int(int(operand,16)/3)
            if(adressingMode == "1"):
                i = int(int(dict_Register[operand],16)/3)
            if(adressingMode == "2"):
                i = int(int(Memory[dict_Register[operand]],16)/3)
            if(adressingMode == "3"):
                i = int(int(Memory[operand],16)/3)
    
    # For JA instruction and "00", "01", "10", "11" addressing modes
    elif(instructionCode == "17"):
        if(CF):
            if(adressingMode == "0"):
                i = int(int(operand,16)/3)
            if(adressingMode == "1"):
                i = int(int(dict_Register[operand],16)/3)
            if(adressingMode == "2"):
                i = int(int(Memory[dict_Register[operand]],16)/3)
            if(adressingMode == "3"):
                i = int(int(Memory[operand],16)/3)

    # For JAE instruction and "00", "01", "10", "11" addressing modes    
    elif(instructionCode == "18"):
        if(CF or ZF):
            if(adressingMode == "0"):
                i = int(int(operand,16)/3)
            if(adressingMode == "1"):
                i = int(int(dict_Register[operand],16)/3)
            if(adressingMode == "2"):
                i = int(int(Memory[dict_Register[operand]],16)/3)
            if(adressingMode == "3"):
                i = int(int(Memory[operand],16)/3 )

    # For JB instruction and "00", "01", "10", "11" addressing modes
    elif(instructionCode == "19"):
        if(SF):
            if(adressingMode == "0"):
                i = int(int(operand,16)/3)
            if(adressingMode == "1"):
                i = int(int(dict_Register[operand],16)/3)
            if(adressingMode == "2"):
                i = int(int(Memory[dict_Register[operand]],16)/3)
            if(adressingMode == "3"):
                i = int(int(Memory[operand],16)/3  )

    # For JBE instruction and "00", "01", "10", "11" addressing modes
    elif(instructionCode == "1A"):
        if(SF or ZF):
            if(adressingMode == "0"):
                i = int(int(operand,16)/3)
            if(adressingMode == "1"):
                i = int(int(dict_Register[operand],16)/3)
            if(adressingMode == "2"):
                i = int(int(Memory[dict_Register[operand]],16)/3)
            if(adressingMode == "3"):
                i = int(int(Memory[operand],16)/3 )

    # For READ instruction and "01", "10", "11" addressing modes
    elif(instructionCode == "1B"):
        myInput = input("Please give me an input in a string format")
        asci = ord(myInput)
        myHex = hex(asci)[2:].zfill(4)
        if(adressingMode == "1"):
            dict_Register[operand] = myHex
        if(adressingMode == "2"):
            Memory[dict_Register[operand]] = myHex 
        if(adressingMode == "3"):
            Memory[operand] = myHex     

    # For PRINT instruction and "00", "01", "10", "11" addressing modes
    elif(instructionCode == "1C"):
        if(adressingMode == "0"):
            outFile.write(chr(int(operand, 16)))
        if(adressingMode == "1"):
            outFile.write(chr(int(dict_Register[operand], 16)))
        if(adressingMode == "2"):
            outFile.write(chr(int(Memory[dict_Register[operand]], 16))) 
        if(adressingMode == "3"):
            outFile.write(chr(int(Memory[operand], 16)))
        outFile.write("\n")

    # For HALT instruction terminates the program                               
    elif(instructionCode == "1"):
        break
    else:
        continue 
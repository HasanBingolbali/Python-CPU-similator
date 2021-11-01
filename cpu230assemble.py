import sys
# Produces instructions as a hex code according to given opcode, addressing mode and operand
def convert(instr, addrs, value):
    intInstr = int(instr, 16)
    intInstr *= 4
    intAddrs = int(addrs, 2)

    intInstr += intAddrs
    hexCode = hex(intInstr)

    if len(str(hexCode)) == 3:
        code = "0" + hexCode[2:] + value
    else:
        code = hexCode[2:] + value
    return code.upper()

# Taking input file
inputFile = sys.argv[1]

# Tracking syntax issues
syntax = True

# Determining immediate values of labels (unitialized variables)
dict_forLabels = {}
with open(inputFile, "r") as a_file:
    a = 0
    for line in a_file:
        stripped_line = line.strip()
        if len(stripped_line) == 0:
            continue
        if(":" in stripped_line):
            index = stripped_line.index(':')
            stripped_line = stripped_line[ :index]
            if dict_forLabels.__contains__(stripped_line.upper()):
                syntax = False
            b = str(hex(a)[2:])
            dict_forLabels[stripped_line.upper()] = b.zfill(4)
            a -= 3 
        a += 3

# A dictionary used for converting instructions to opcode
dict_forInstructions = {
    "HALT"  : "1",
    "LOAD"  : "2",
    "STORE" : "3",
    "ADD"   : "4",
    "SUB"   : "5",
    "INC"   : "6",
    "DEC"   : "7",
    "XOR"   : "8",
    "AND"   : "9",
    "OR"    : "A",
    "NOT"   : "B",
    "SHL"   : "C",
    "SHR"   : "D",
    "NOP"   : "E",
    "PUSH"  : "F",
    "POP"   : "10",
    "CMP"   : "11",
    "JMP"   : "12",
    "JZ"    : "13",
    "JE"    : "13",
    "JNZ"   : "14",
    "JNE"   : "14",
    "JC"    : "15",
    "JNC"   : "16",
    "JA"    : "17",
    "JAE"   : "18",
    "JB"    : "19",
    "JBE"   : "1A",
    "READ"  : "1B",
    "PRINT" : "1C"
}

# Another dictionary for matching registers with their bit patterns
dict_forRegister = {
    "PC"    : "0000",
    "A"     : "0001",
    "B"     : "0002",
    "C"     : "0003",
    "D"     : "0004",
    "E"     : "0005",
    "S"     : "0006"
}

# Producing output file
outputFile = inputFile[:-4] + ".bin"
f = open(outputFile, "w")

if syntax:
    with open(inputFile, "r") as a_file:
        a = 0
        
        for line in a_file:
            # Formatting input by getting rid of unnecessary spaces
            stripped_line = line.strip()        
            ary = line.split()
            # Skipping empty lines
            if len(stripped_line) == 0:
                continue   

            # Outputting NOP instruction
            elif(ary[0] == "NOP"):
                f.write("0E0000")
                f.write( '\n')

            # Outputting HALT instruction
            elif(ary[0] == "HALT"):
                f.write("040000")
                f.write( '\n')

            # Skipping labels
            elif(len(ary) == 1):
                continue

            # Outputting instructions with addressing mode 10
            elif((ary[1] == "[A]" or ary[1] == "[B]" or ary[1] == "[C]" or ary[1] == "[D]" or ary[1] == "[E]" or ary[1] == "[SP]")):   
                # Syntax checks
                if len(dict_forRegister.get(ary[1][1:2])) > 4:
                    syntax = False
                    break
                f.write(convert(dict_forInstructions.get(ary[0]), "10", dict_forRegister.get(ary[1][1:2])))
                f.write('\n')

            # Outputting instructions with addressing mode 11   
            elif("[" in ary[1]):
                stringg = ary[1].replace("[","")
                stringg = stringg.replace("]","")
                stringg = stringg.replace("'","")
                # Syntax checks
                if len(stringg) > 4:
                    syntax = False
                    break
                f.write(convert(dict_forInstructions.get(ary[0]), "11", stringg))
                f.write('\n')
            
            # Outputting instructions with addressing mode 00 and char type operand
            elif( "'" in ary[1]):
                mystring = ary[1].replace("'","")
                
                a = str(hex(ord(mystring)))[2:]
                result = a.zfill(4)
                # Syntax checks
                if len(result) > 4:
                    syntax = False
                    break
                f.write(convert(dict_forInstructions.get(ary[0]), "00", result))
                f.write('\n')
            
            # Outputting instructions with addressing mode 01
            elif(ary[1] == "A" or ary[1] == "B" or ary[1] == "C" or ary[1] == "D" or ary[1] == "E" or ary[1] == "SP" ):    
                # Syntax checks
                if len(dict_forRegister.get(ary[1])) > 4:
                    syntax = False
                    break
                f.write(convert(dict_forInstructions.get(ary[0]), "01", dict_forRegister.get(ary[1])))
                f.write('\n')

            # Outputting instructions with addressing mode 00 and a label
            elif(ary[1] in dict_forLabels):
                # Syntax checks
                if len(dict_forLabels.get(ary[1])) > 4:
                    syntax = False
                    break                
                f.write(convert(dict_forInstructions.get(ary[0]), "00", dict_forLabels.get(ary[1])))
                f.write('\n')
            
            # Outputting instructions with addressing mode 00 and immediate hex operand
            elif(True):
                # Syntax checks
                if len(ary[1]) > 4:
                    syntax = False
                    break  
                f.write(convert(dict_forInstructions.get(ary[0]), "00", ary[1])) 
                f.write('\n')
if not syntax:
    f.write("Syntax error")
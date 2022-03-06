def parseS(input_string,l,labels):
    out = ""
    function_1 = ""
    function_2 = ""
    function_3 = ""
    opcode = "0100011"

    w = "010"
    h = "001"
    d = "011"
    b = "000"

    input_string = input_string.replace('(',' ')
    input_string = input_string.replace(')',' ')
    p = input_string.split()


    if len(p) != 4:
        raise Exception(f"Store excepts 4 arguments but got {len(p)} >>"+input_string)
    [operation, value_1 , instant , value] = p

    if operation[1] == 'w':
        function_1 = w

    elif operation[1] == 'b':
        function_1 = b

    elif operation[1] == 'h':
        function_1 = h

    else:
        function_1 = d


    if value_1[0] != 'p':
        raise Exception(f"{value_1} is not a valid register_all. >>"+input_string)

    value_1 = value_1.replace('p','')
    value_1 = int(value_1)


     # Using Exception Handling
    if value_1 < 0 or value_1 > 31:
        raise Exception("Register value out of bounds. >>"+input_string)

    value_1 = bin(value_1)[2:]
    if value[0] != 'p':
        raise Exception(f"{value} is not a valid register_all. >>"+input_string)


    value = value.replace('p','')
    value = int(value)


    # Using Exception Handling
    if value < 0 or value > 31:
        raise Exception("Register value out of bounds. >>"+input_string)
        
    value = bin(value)[2:]

    if instant[0] == '0' and len(instant) > 1 and instant[1] == 'p':
        instant = instant[2:]
        instant = int(instant,16)
        if instant > 4096 or instant < -4096:
            raise Exception("Immediate value out of bounds. >>"+input_string)

        instant = bin(instant)[2:]

    elif instant[0] == '-':
        instant = instant[1:]
        num = 0 - (int(instant))
        if num > 4096 or num < -4096:
            raise Exception("Immediate value out of bounds. >>"+input_string)
        instant = ''.join(reversed([str((num >> i) & 1) for i in range(12)]))

    else:
        instant = int(instant)
        if instant > 4096 or instant < -4096:
            raise Exception("Immediate value out of bounds. >>"+input_string)
        instant = bin(instant)[2:]

    for _ in range(12 - len(instant)):
        instant = '0' + instant

    for _ in range(5 - len(value)):
        value = '0' + value

    for _ in range(5 - len(value_1)):
        value_1 = '0' + value_1


    function_2 = instant[0:7]
    function_3 = instant[7:12]

    out += function_2
    out += value_1
    out += value
    out += function_1
    out += function_3
    out += opcode  
    return out


# new definition with different language(parseU) under RISC V Architechture

def parseU(command, line_number, label_dict):
    try:
        [ins, reg, imm] = command.split()
    except:
        raise Exception("Incorrect command format >>"+command)

    letter = reg[0]

    try:
        reg = int(reg[1:])
    except:
        raise Exception("Incorrect register_all format >>"+command)


    if(ins == 'auipc'):
        opcode = '0010111'

    elif(ins == 'lui'):
        opcode = '0110111'

    if(letter!='p' or reg > 31 or reg < 0):
        raise Exception("Undefined Register >>" +command)

    if(imm[:2]=='0x'):
        try:
            imm = int(imm,0)
        except:
            raise Exception("Invalid instant value >>" +command)

    else:
        try:
            imm = int(imm)
        except:
            raise Exception("Invalid instant value >>" +command)

    # Using Exception Handling
    if(imm < 0 or imm > 1048575):
        raise Exception("Immediate value out of range [0-1048575] >>" + command)

    imm = ''.join(reversed([str((imm >> i) & 1) for i in range(20)]))
    reg = ''.join(reversed([str((reg >> i) & 1) for i in range(5)]))

    return imm+reg+opcode


# Cecking Registers validity

def isValidRegister(reg):
    if reg[0] != 'p':
        return False

    if reg[1:].isnumeric() == False:
        return False

    if int(reg[1:]) < 0 or int(reg[1:]) > 31:
        return False

    return True


# New definition with different language(parseSB) under RISC V Architechture

def parseSB(command, line_number, label_dict):
    components = command.split()

    if(len(components) != 4):
        err = "Error! Branch command expected 3 arguments, got " +  str(len(components)-1) + " instead. >>"+command
        raise Exception(err)
    
    [operation, rs1, rs2, target_register] = command.split()   

    if isValidRegister(rs1) == False:
        raise Exception("Error! Argument 1 is not a valid register_all. >>" + command)

    if isValidRegister(rs2) == False:
        raise Exception("Error! Argument 2 is not a valid register_all. >>"+command)

    if target_register not in label_dict.keys():
        raise Exception("Error! Target register_all not found. >>" + command)

    immediate_field = label_dict[target_register] - line_number

     # Using Exception Handling
    if immediate_field > 4095 or immediate_field < -4096:
        raise Exception("Error! Target label is too far. >>" + command)


#Get the integer based value of registers
    rs1 = int(rs1[1:])
    rs2 = int(rs2[1:])


    rs1 = ('0' * (5 - len(str(bin(rs1))[2:]))) + (str(bin(rs1))[2:])
    rs2 = ('0' * (5 - len(str(bin(rs2))[2:]))) + (str(bin(rs2))[2:])

    immediate_field = ''.join(reversed([str((immediate_field >> i) & 1) for i in range(13)]))

    # at prsent opcode
    opcode = '1100011'

    #Initialising specific functions
    function_1 = '000'*(operation=='beq') + '001'*(operation=='bne') + '100'*(operation=='blt') + '101'*(operation=='bge')
    machine_code = immediate_field[0] + immediate_field[2:8] + rs2 + rs1 + function_1 + immediate_field[8:12] + immediate_field[1] + opcode

    return machine_code


# new definition with different language(parseR) under RISC V Architechture

def parseR(command,inst,labels={}):  #list labels will be initiated
    import re                        # re stands for the module supporting regular languages(both 8 bit and unicode strings)

    p=re.split(r'[,\s]\s*',command)

    if len(p)!=4:
        raise Exception(f'Expected 3 argumets.Got {len(p)-1} instead. >>' + command)

    [ins,ra,rs1,rs2]=p  

    if not isValidRegister(rs1) or not isValidRegister(rs2) or not isValidRegister(ra):
        raise Exception('Invalid Register Operands! >>'+command)

    # at prsent opcode
    opcode='0110011'

#Get the integer based value of registers
    rs1=int(rs1[1:])
    rs2=int(rs2[1:])
    ra=int(ra[1:])

    # Using Exception Handling for checking of rs1 register
    if rs1<0 or rs1>31:
        raise Exception("Register rs1 invalid! >>" + command)

    # Using Exception Handling for checking of rs2 register
    if rs2<0 or rs2>31:
        raise Exception("Register rs2 invalid! >>" + command)

    # Using Exception Handling for checking of ra register
    if ra<0 or ra>31:
        raise Exception("Register ra invalid! >>"+command)

    #Initialising all functions(mostly arithmatic)
    function_1 = '000'*(ins=='sub' or ins=='add' or ins=='mul')+'111'*(ins=='and')+'001'*(ins=='sll')+'010'*(ins=='slt')+'101'*(ins=='sra'or ins=='srl')+'100'*(ins=='xor' or ins=='div')+'110'*(ins=='or' or ins=='rem')
    function_operations = '0000000'*(ins=='add' or ins=='and' or ins=='sll' or ins=='slt' or ins=='srl' or ins=='xor' or ins=='or')+'0100000'*(ins=='sub' or ins=='sra')+'0000001'*(ins=='div'or ins=='rem'or ins=='mul')

    rs1=f'{rs1:05b}'
    rs2=f'{rs2:05b}'
    ra=f'{ra:05b}'

    return function_operations+rs2+rs1+function_1+ra+opcode


# new definition with different language(parseUJ) under RISC V Architechture

def parseUJ(command,inst,labels={}):    #list labels will be initiated
    import re                           # re stands for the module supporting regular languages(both 8 bit and unicode strings)

    p=re.split(r'[,\s]\s*',command)

    if len(p)!=3:
        raise Exception(f"Expexted 2 operands, got{len(p)-1} instead. >>" + command)

    [_,ra,label]=p

    # using not in exception to check the invalidity of register
    if not isValidRegister(ra):
        raise Exception("Invalid Register Operand! >>" + command) 
       
    opcode='1101111'

    # using not in exception to check the invalidity of label
    if label not in labels.keys():
        raise Exception("Label Not Found! >>" + command)

    #Get the integer based value of registers
    ra=int(ra[1:])

    # Using Exception Handling for checking of ra register
    if ra<0 or ra>31:
        raise Exception('Register ra invalid! >>' + command)

    ra=f'{ra:05b}'

    diff=labels[label]-inst

    if diff > 2**20-1 or diff <-2**20:               #Range of Address
        raise Exception('Address Out of Range! Use jalr instead >>' + command)

    diff=''.join([str(diff>>i & 1) for i in range (0,21)])[::-1]
    imm=diff[0]+diff[10:20]+diff[9]+diff[1:9]

    return imm+ra+opcode


# new definition with different language(parseI) under RISC V Architechture

def parseI(command, line_number, table):
    import re                             # re stands for the module supporting regular languages(both 8 bit and unicode strings)
    
    # Initialising All the "I" based instructions
    I = ["addi", "andi", "ori", "lb", "ld", "lh", "lw" , "jalr"]
    
    #Getting the string based values by splitting/slicing
    instant = ''

    try:
        [operation, ra, rs, instant] = command.split()
    except:
        [operation, ra, rs] = command.split()
    
    #Check error code for operation
    if(operation not in I):
        raise Exception("The entered command is not a valid operation")
        
    #Regular Expression based checking
    regex = re.compile(r"p\d+")
    register_all = regex.search(ra)

    #Checking for ra
    if(register_all == None or len(register_all.group()) != len(ra)):
        raise Exception("Enter a valid destination register_all")
        
    #Checking for rs
    if(operation in I[3:]):
        regex = re.compile(r"(\d+\(p\d+\))|(0x(\d+|[A-Fa-f]+)\(p\d+\))")
        register_all = regex.search(rs)

        if(register_all == None or len(register_all.group()) != len(rs)):
            raise Exception("Enter a valid source register_all and its offset")


        # Initialising an bolean function = True    
        bool = True
        rs = ''
    
        for i in register_all.group():        #using for loop for checking of ')'
            if(i == '('):
                bool = False
                continue
    
            if(i == ')'):
                continue
    
            if(bool):
                instant = instant + i
            else:
                rs = rs + i


    #Checking for ra
    else:
        regex = re.compile(r"p\d+")
        register_all = regex.search(rs)

        if(register_all == None or len(register_all.group()) != len(rs)):
            raise Exception("Enter a valid destination register_all")
            
            
    #Get the integer based value of registers
    rs = int(rs[1:])
    ra = int(ra[1:])
    

    # Using Exception Handling for all 3 registers at a time
    if(rs < 0 or rs > 31 or ra < 0 or ra > 31):
        raise Exception("Invalid register_all value!!! They should have been between 0 to 31")

   
    #Encoding to binary for rs register
    rs = str(bin(rs))
    rs = rs[2:]
    rs = '0' * (5 - len(rs)) + rs
    
    #Encoding to binary for ra register
    ra = str(bin(ra))
    ra = ra[2:]
    ra = '0' * (5-len(ra)) + ra
    

    #Encoding and checking for instant
    try:
        int(instant, 0)
    except:
        raise Exception('Enter a valid instant field')
        
    if(instant[0:2] == '0x'):
        #To get the correct size of instant field
        #Sizes smaller than 8 and larger than 8 are all clipped to 8.

        if(len(instant[2:]) <= 8):
            instant = '0x' + '0'*(8 - len(instant[2:])) + instant[2:]

        else:
            instant = '0x' + instant[len(instant)-8:len(instant)]


        instant = int(instant, 0)
        
        if(instant == 4096):
            instant = -2048
        else:
            instant = -(instant & 0x80000000) | (instant & 0x7fffffff)

            
    elif(instant[0:3] == '-0x'):
        if(len(instant[3:]) <= 8):
            instant = '0x' + '0' * (8 - len(instant[3:])) + instant[3:]
        else:
            instant = '0x' + instant[len(instant)-8: len(instant)]
            
        instant = int(instant, 0)
        
        if(instant == 4096):
            instant = -2048
        else:
            instant = (instant & 0x80000000) | -(instant & 0x7fffffff)
            
    else:
        instant = int(instant, 0)
        
    if(instant > 2047 or instant < -2048):
        raise Exception('Immediate value should be in the range [-2048, 2047]')
        
    if(instant < 0):
        instant = -1 * instant
        instant = 4096 - instant


    instant = str(bin(instant))
    instant = instant[2:]
    instant = '0' * (12 - len(instant)) + instant
        
    opcode = ''
    function_1 = ''
    

    # Setting "opcode and function_1" values for each function
    if(operation == 'addi'):
        opcode = '0010011'
        function_1 = '000'

    elif(operation == 'andi'):
        opcode = '0010011'
        function_1 = '111'

    elif(operation == 'ori'):
        opcode = '0010011'
        function_1 = '110'

    elif(operation == 'lb'):
        opcode = '0000011'
        function_1 = '000'

    elif(operation == 'lh'):
        opcode = '0000011'
        function_1 = '001'

    elif(operation == 'lw'):
        opcode = '0000011'
        function_1 = '010'
    
    elif(operation == 'ld'):
        opcode = '0000011'
        function_1 = '011'

    elif(operation == 'jalr'):
        opcode = '1100111'
        function_1 = '000'


    #Collecting the final binary code
    final_value = instant + rs + function_1 + ra + opcode
    return final_value
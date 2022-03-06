import sys
import re               # re stands for the module supporting regular languages(both 8 bit and unicode strings)
from initial import *   # importing from "initial" source

if(len(sys.argv)==3):
    input = sys.argv[1]
    output = sys.argv[2]

elif(len(sys.argv)==2):
    input = sys.argv[1]
    output = input.split('.')[0] + '.mc'

else:
    raise Exception("Invalid arguments")


with open(input, 'r') as f:
    buffer = f.read()

buffer = re.sub(r'#.*\n', '\n', buffer)
buffer = re.sub(r'#[^\n]+', '\n', buffer)
buffer = re.sub(r':', ':\n', buffer)
buffer = re.sub(r'\n\s+', '\n', buffer)
buffer = re.sub(r'^\s+', '', buffer)
buffer = re.sub(r'\s+$', '', buffer)

if(len(buffer)==0):
    raise Exception("No code to process!")

lines = [p.strip() for p in buffer.split("\n")]

data_index = [[i,1] for i, p in enumerate(lines) if p == ".data"]
text_index = [[i,2] for i, p in enumerate(lines) if p == ".text"]

directives = data_index + text_index

#Using Sorting to sort directives and lambda
directives = sorted(directives, key = lambda p:p[0])

# Initialising Array for each type
text = []
data = []
labels = {}

j=0
current_value = 2

for i in range(len(lines)):
    if(j<len(directives) and i==directives[j][0]):
        current_value = directives[j][1]
        j+=1

    elif(current_value==2 and len(lines[i])>0):
        text.append(lines[i])

    elif(len(lines[i])>0):
        data.append(lines[i])


# Initialising Registers

text = "\n".join(text)
text = text.lower()
text = re.sub(r',', ' ', text)
text = re.sub(r'  ', ' ', text)

text = re.sub(r'(?<=[ (])ra(?=[ )\n])', 'x1', text)
text = re.sub(r'(?<=[ (])sp(?=[ )\n])', 'x2', text)
text = re.sub(r'(?<=[ (])gp(?=[ )\n])', 'x3', text)
text = re.sub(r'(?<=[ (])tp(?=[ )\n])', 'x4', text)
text = re.sub(r'(?<=[ (])t0(?=[ )\n])', 'x5', text)
text = re.sub(r'(?<=[ (])t1(?=[ )\n])', 'x6', text)
text = re.sub(r'(?<=[ (])t2(?=[ )\n])', 'x7', text)
text = re.sub(r'(?<=[ (])s0(?=[ )\n])', 'x8', text)
text = re.sub(r'(?<=[ (])s1(?=[ )\n])', 'x9', text)
text = re.sub(r'(?<=[ (])a0(?=[ )\n])', 'x10', text)
text = re.sub(r'(?<=[ (])a1(?=[ )\n])', 'x11', text)
text = re.sub(r'(?<=[ (])a2(?=[ )\n])', 'x12', text)
text = re.sub(r'(?<=[ (])a3(?=[ )\n])', 'x13', text)
text = re.sub(r'(?<=[ (])a4(?=[ )\n])', 'x14', text)
text = re.sub(r'(?<=[ (])a5(?=[ )\n])', 'x15', text)
text = re.sub(r'(?<=[ (])a6(?=[ )\n])', 'x16', text)
text = re.sub(r'(?<=[ (])a7(?=[ )\n])', 'x17', text)
text = re.sub(r'(?<=[ (])s2(?=[ )\n])', 'x18', text)
text = re.sub(r'(?<=[ (])s3(?=[ )\n])', 'x19', text)
text = re.sub(r'(?<=[ (])s4(?=[ )\n])', 'x20', text)
text = re.sub(r'(?<=[ (])s5(?=[ )\n])', 'x21', text)
text = re.sub(r'(?<=[ (])s6(?=[ )\n])', 'x22', text)
text = re.sub(r'(?<=[ (])s7(?=[ )\n])', 'x23', text)
text = re.sub(r'(?<=[ (])s8(?=[ )\n])', 'x24', text)
text = re.sub(r'(?<=[ (])s9(?=[ )\n])', 'x25', text)
text = re.sub(r'(?<=[ (])s10(?=[ )\n])', 'x26', text)
text = re.sub(r'(?<=[ (])s11(?=[ )\n])', 'x27', text)
text = re.sub(r'(?<=[ (])t3(?=[ )\n])', 'x28', text)
text = re.sub(r'(?<=[ (])t4(?=[ )\n])', 'x29', text)
text = re.sub(r'(?<=[ (])t5(?=[ )\n])', 'x30', text)
text = re.sub(r'(?<=[ (])t6(?=[ )\n])', 'x31', text)
text = text.split("\n")



# Processing Data
# Maintain data label locations

dataLocation = {}
dataOut = {}

memory = int("0x10000000",0)

j = 0
while(j<len(data)):
    if(re.match(r'[^\s,]+:', data[j])):
        label = data[j][:-1]
        if label in dataLocation:
            raise Exception("Data Label declared more than once: "+label)
        dataLocation[label] = memory
        j+=1
    
    if(re.match(r'(\.byte|\.half|\.word|\.dword|\.asciiz)', data[j])):   #Inputting all types of DataTypes for registers
        # dataLocation[label] = memory
        datatype = data[j].split()[0]
    
        for value in re.split(r'[, ]', data[j])[1:]:
            if(len(value) == 0):
                continue
        
            if(re.match(r"0x", value)):
                value = int(value,0)
            

            elif(datatype != ".asciiz"):
                value = int(value)
            
            if(datatype == '.byte'):
                dataOut[memory] = value & 255
                value = value>>8
            
                if(value!=0 and value!=-1):
                    raise Exception("Value out of range: "+data[j])
                memory+=1
            

            elif(datatype == '.half'):
                dataOut[memory] = value & 255
                value = value >> 8
                dataOut[memory+1] = value & 255
                value = value>>8
            
                if(value!=0 and value!=-1):
                    raise Exception("Value out of range: "+data[j])
                memory+=2
            

            elif(datatype == '.word'):
                dataOut[memory] = value & 255
                value = value >> 8
                dataOut[memory+1] = value & 255
                value = value >> 8
                dataOut[memory+2] = value & 255
                value = value >> 8
                dataOut[memory+3] = value & 255
                value = value>>8

                if(value!=0 and value!=-1):
                    raise Exception("Value out of range: "+data[j])
                memory+=4
            

            elif(datatype == '.dword'):
                dataOut[memory] = value & 255
                value = value >> 8
                dataOut[memory+1] = value & 255
                value = value >> 8
                dataOut[memory+2] = value & 255
                value = value >> 8
                dataOut[memory+3] = value & 255
                value = value >> 8
                dataOut[memory+4] = value & 255
                value = value >> 8
                dataOut[memory+5] = value & 255
                value = value >> 8
                dataOut[memory+6] = value & 255
                value = value >> 8
                dataOut[memory+7] = value & 255
                value = value>>8
            
                if(value!=0 and value!=-1):
                    raise Exception("Value out of range: "+data[j])
                memory+=8
            

            elif(datatype == '.asciiz'):
                string = re.findall('"([^"]*)"', data[j])
                if(len(string)!=1):
                    raise Exception(".asciiz requires single string: " + data[j])


                for c in string[0]:
                    dataOut[memory] = ord(c)
                    memory += 1
    
                dataOut[memory] = 0
                memory += 1

                break

    else:
        raise Exception("Unsupported directiive " + data[j])
    j+=1



# Process Text
# Replace all commas with spaces
# Replace register labels with correct values
# Replace lw xX label with correct instructions


#ALL Instruction type Formats
R = ['add', 'and', 'or', 'sll', 'slt', 'sra', 'srl', 'sub', 'xor', 'mul', 'div', 'rem']
I = ['addi', 'andi', 'ori', 'lb', 'lh', 'lw', 'jalr']
S = ['sb', 'sw', 'sh']
SB = ['beq', 'bne', 'bge', 'blt']
U = ['auipc', 'lui']
UJ = ['jal']
special = ['lw','lb','lh']


inputNo = 0

for line in text:
    if(re.match(r'[^\s,]+:', line)):
        if line[:-1] in labels:
            raise Exception("Label declared more than once: "+line[:-1])
        labels[line[:-1]] = 4*inputNo
        continue
    inputNo+=1

inputNo = 0
textOut = {}
memory = 0

for line in text:
    if(re.match(r'[^\s,]+:', line)):
        continue

    ins = line.split()[0]

    if(ins in R):
        textOut[memory] = hex(int(parseR(line,memory,labels),2))

    elif(ins in I):
        if(ins not in special or (ins in special and re.match(r'.+\(p\d+\)', line))):
            textOut[memory] = hex(int(parseI(line,memory,labels),2))
        
        else:
            try:
                ins, register, label = line.split()
            except:
                raise Exception("Invalid statement >>" + line)
            
            if(label not in dataLocation.keys()):
                raise Exception("Could not find label >>" + line)
            

            textOut[memory] = hex(int(parseU("lui "+register+" "+hex(dataLocation[label])[:-3], memory, labels),2))
            memory += 4
            textOut[memory] = hex(int(parseI(ins+" "+register+" "+str(int("0x"+hex(dataLocation[label])[7:],0))+"("+register+")", memory, labels),2))


    elif(ins in S):
        textOut[memory] = hex(int(parseS(line,memory,labels),2))
    elif(ins in SB):
        textOut[memory] = hex(int(parseSB(line,memory,labels),2))
    elif(ins in U):
        textOut[memory] = hex(int(parseU(line,memory,labels),2))
    elif(ins in UJ):
        textOut[memory] = hex(int(parseUJ(line,memory,labels),2))
    else:
        raise Exception("Invalid Instruction "+line)
    memory += 4
textOut[memory] = '0x00000000'


output = ''

for k in textOut:
    output+= '0x'+'0'*(10-len(hex(k)))+hex(k)[2:] +" "+'0x'+'0'*(10-len(hex(int(textOut[k],0))))+hex(int(textOut[k],0))[2:]+"\n"
    # output+= '0'*(10-len(hex(int(textOut[k],0))))+hex(int(textOut[k],0))[2:]+"\n"

output+="\n"

for k in dataOut:
    output+= '0x'+'0'*(10-len(hex(k)))+hex(k)[2:]+" "+'0x'+'0'*(4-len(hex(dataOut[k])))+hex(dataOut[k])[2:]+"\n"


with open(output, 'w') as f:
    f.write(output)
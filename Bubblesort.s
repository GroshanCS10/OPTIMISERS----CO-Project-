.data
var1: .word 7, 2, -10, 44, 23, 75, 38, 88, 24, 25, 13

.text
lui x10,0x10000    #base address in x10
addi x11,x0,11     #length in x11
addi x7 x0 1

jal x1,bubblesort
beq x0,x0,finish

bubblesort:
beq x11,x7,exit   #loop counter
    
    addi x8,x0,1
    addi x2,x2,-4
    sw x11,0(x2)
    addi x2,x2,-4
    sw x1,0(x2)
    
    add x31,x0,x10   #copy base address in x31

loop:
bge x8,x11,ff
    lw x30,0(x31)
    lw x29,4(x31)
    bge x29,x30,noswap
sw x29,0(x31)
    sw x30,4(x31)
    noswap:
addi x8,x8,1
        addi x31,x31,4
        jal x0 loop
ff:
addi x11,x11,-1
    jal x1,bubblesort
lw x1,0(x2)
    lw x11,4(x11)
    addi x2,x2,8
    jalr x0 0(x1)
    exit:
    jalr x0 0(x1)
       
       
finish:

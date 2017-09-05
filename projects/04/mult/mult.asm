// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

// Psuedo Code
// Dim a, b, mult, n
// mult = 0
// n=b
// while n > 0
//   mult = mult + a
//   n = n-1
// Loop

@mult
M = 0 //Store and set the multiplier to 0

@R0
D=M
@a
M=D //Store the 'a' variable

@R1
D=M

@R1
D=M
@n
M=D //Store the 'n' variable


(LOOP)

	@END
	D;JEQ //Jump to End if n=0

	@a //Select the 'a' variable
	D=M //Store it in Register D
	@mult //Select the 'mult' variable
	D=D+M //Compute D=mult+a
	M=D

	@n
	D=M-1 //Decrement n by 1
	M=D

	@LOOP
	0;JMP //Goto LOOP

(END)	
	@mult
	D=M
	@R2
	M=D
	@END
	0;JMP //Infinite Loop

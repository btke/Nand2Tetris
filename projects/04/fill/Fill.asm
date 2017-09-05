// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(KEYBOARDLOOP)

@SCREEN
D=A
@addr
M=D  //Set the 'addr' variable to the screen base address

@24576
D=A
@n
M=D //Set the 'n' variable to the last screen address

@KBD
D=M //Get Keyboard Value
@BLACK
D;JGT //If not 0, jump to black
@WHITE
D;JEQ //if 0, jump to white

(BLACK)
@colour
M=-1 //set colour to -1 for black
@SCREENLOOP
0;JMP

(WHITE)
@colour
M=0 //set colour to 0 for white
@SCREENLOOP
0;JMP
	

(SCREENLOOP)
//Screen Fill Code
	@n
	D=M
	@addr
	D=D-M
	@END
	D;JEQ //if i>n goto END
	
	@colour
	D=M	

	@addr
	A=M
	M=D //Set pixel colour
	
	@addr
	M=M+1
	
	@SCREENLOOP
	0;JMP

	
(END)
	@KEYBOARDLOOP
	0;JMP



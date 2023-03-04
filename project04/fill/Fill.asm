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

// @16384 // screen

// @24576 // keyboard

@status
    M=0;
@pointer
    M=0;
@current_screen
    M=0;

(MAIN_LOOP)
    @24576
        D=M
    @FILL_SCREEN
        D; JNE
    @CLEAR_SCREEN
        0; JMP

(FILL_SCREEN)
    @status
        M=-1;

    @SET_SCREEN
        0; JMP

(CLEAR_SCREEN)
    @status
        M=0;

(SET_SCREEN)
    @pointer
        M=0;
    
(LOOP)
    @pointer
        D=M;
        M=M+1;

    @16384
        D=D+A;
    
    @current_screen
        M=D;
    
    @status
        D=M;
    
    @current_screen
        A=M;
        M=D;
        
    @pointer
        D=M;
    
    @8192
        D=D-A;

    @MAIN_LOOP
        D; JEQ

    @LOOP
        0; JMP
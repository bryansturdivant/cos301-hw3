- Bryan Sturdivant
- Cost 301
- HW #3
- 11/5/2025

Manifest:

- README.md: This file: Overview and instructions
- HW02.py: Main python script of the modified HW#2 

Requirements:

- Python

- Running:
    - Windows: python HW02.py
    - Mac: python3 HW02.py

- This will start the program. There is no prompting or additional information provided

- In order to allow multiple lines of input from the user, I have it set up so it loops through the input line by line so it can handle all of the instructions correctly
- cntrl + d: Enter on a new line when you're done with your input 


- Sample Input/Output:
- Sample 1: 

y = 4
y

Functions: ['Main/0]
Constants: [4, 'None']
Locals: ['y']
Globals: ['print']
BEGIN
     LOAD_CONST 0
     STORE_FAST 0
     LOAD_FAST 0
     LOAD_GLOBAL 0
     ROT_TWO
     CALL_FUNCTION 1
     POP_TOP
     LOAD_CONST 1
     RETURN_VALUE
END

- sample 2


y = -60 + 4 * 90
x = 5/2//1
x
y

Functions: ['Main/0]
Constants: [60, 0, 4, 90, 5, 2, 1, 'None']
Locals: ['y', 'x']
Globals: ['print']
BEGIN
     LOAD_CONST 0
     LOAD_CONST 1
     ROT_TWO
     BINARY_SUBTRACT
     LOAD_CONST 2
     LOAD_CONST 3
     BINARY_MULTIPLY
     BINARY_ADD
     STORE_FAST 0
     LOAD_CONST 4
     LOAD_CONST 5
     BINARY_TRUE_DIVIDE
     LOAD_CONST 6
     BINARY_FLOOR_DIVIDE
     STORE_FAST 1
     LOAD_FAST 1
     LOAD_GLOBAL 0
     ROT_TWO
     CALL_FUNCTION 1
     POP_TOP
     LOAD_FAST 0
     LOAD_GLOBAL 0
     ROT_TWO
     CALL_FUNCTION 1
     POP_TOP
     LOAD_CONST 7
     RETURN_VALUE
END





- Modifications from HW #2:
    - Instead of printing the outputs from variables and expressions, its now printing out the JCoCo instructions for any entered input 

- Bugs and Limitations:

    - I believe that everything works as intended without any bugs 

    
- Resources used:

    - Textbook
    - JCoCo documentation 
    - Python documentation for anything I needed a reminder about syntax wise
    - w3schools.com for some help with that loop for multiple lines to be read into the output correctly 
# CO-Project-CSE112
CSE-112 Group Project
This assembler code is written in python and it bridges the gap between high-level programming languages and the machine code understood by computers. They provide a means for programmers to write code at a lower level of abstraction, allowing them to optimize performance and have more control over the hardware. Assemblers are responsible for translating human-readable assembly language code into machine-readable instructions. Assembly language provides a more convenient and readable way for programmers to write code compared to writing directly in machine code.
It takes input from terminal. We type the code in low level language in the terminal followed by enter and control+z to give input.
The code starts by importing the sys module and reading the input from stdin using sys.stdin.read(). The input is then split into lines using the splitlines() method and stored in the infile variable.

The code defines several helper functions, each representing an assembly instruction, such as mul, add, ld, AND, div, Compare, Invert, mov, XOR, OR, sub, st, Rshift, and Lshift. These functions handle different instructions and perform error checking on the input arguments. If any errors are encountered, they raise a SyntaxError with an appropriate error message.

The code defines a dictionary called register that maps register names to their binary representations.

The code initializes variables such as count to keep track of the line number, output to store the resulting binary instructions, labels to store label definitions, and variables to store variable definitions.

The code iterates over each line in the infile and performs the following actions:
        a. If the line starts with a label (ending with a colon), it checks for valid label definitions and adds them to the labels dictionary.
        b. If the line is a variable definition (starts with "var"), it checks for valid variable definitions and adds them to the variables dictionary.
        c. If the line contains an assembly instruction, it splits the line into a list of tokens and checks the instruction type.
        d. Based on the instruction type, the corresponding helper function is called to generate the binary representation of the instruction.
        e. The resulting binary instruction is added to the output list.

After processing all the lines, the code performs additional checks:
        a. It ensures that at least one "hlt" instruction is defined and raises an error if not.
        b. It verifies that there are no duplicate labels and that the last instruction is "hlt". Otherwise, it raises an error.

Finally, the code outputs the resulting binary instructions stored in the output list.

The provided code essentially reads an assembly-like language and converts it into binary instructions. It performs error checking for valid instructions, registers, variables, and labels, and generates the corresponding binary code for each instruction. write this in para instead on points
The code raises SyntaxError exceptions with specific error messages when it encounters invalid instructions, registers, variables, or labels. These exceptions provide concise information about the error, allowing the user to identify and address the problem accurately. The errors include unrecognized or unsupported instructions, invalid register names, invalid variable or label names, duplicate label definitions, and missing "hlt" instruction as the last instruction.

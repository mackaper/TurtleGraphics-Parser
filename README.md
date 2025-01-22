# TurtleGraphics Parser

This repository contains an implementation of a parser for a simple graphics programming language inspired by the Logo language. The program translates commands into Cartesian coordinates and generates line segments representing graphical output. The project includes lexical analysis, recursive descent parsing, and program execution.

## Key Highlights

- **Language Support:** Implements a case-insensitive language with commands for movement, rotation, color changes, and loops.
- **Recursive Descent Parser:** Constructs a syntax tree based on a formal grammar and evaluates commands to generate output.
- **Lexical Analysis:** Processes input into tokens for the parser, identifying syntax errors with precise error reporting.
- **Graphics Execution:** Translates parsed commands into a sequence of line segments with accurate coordinates and colors.
- **Custom Grammar:** Developed a BNF grammar for the language, enabling a structured parsing process.

## Repository Contents

- `src/Lexer.java`: Lexical analyzer that converts input into tokens.
- `src/Parser.java`: Recursive descent parser that generates syntax trees and validates the program.
- `src/Executor.java`: Executes the parsed syntax tree, generating line segments.
- `docs/grammar.bnf`: Formal grammar definition of the language.
- `docs/parsetree.png`: Parse tree for a sample input.
- `docs/sample_output.txt`: Example output of line segments generated from sample input programs.
- `docs/report.md`: Detailed documentation on the parser design, grammar, and testing process.

## Features

- **Error Handling:** Reports syntax errors with precise line numbers and helpful messages.
- **Flexible Input:** Handles case-insensitive commands, optional spaces, and supports comments.
- **Customizable Output:** Generates line segments with configurable precision and outputs in a defined format.
- **Example Programs:** Includes sample input files to demonstrate valid and invalid programs.

## Results

The parser successfully translates graphical programs into line segment definitions, handling loops, color changes, and directional movements. Performance is optimized to handle large inputs efficiently.

---

This project was part of an academic assignment designed to enhance skills in compiler construction, formal grammars, and program parsing.

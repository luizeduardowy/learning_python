# Python Learning Projects

This repository contains small projects and exercises I made while learning Python. Feel free to use them, but please remember to give credit.

## Project structure

```text
.
├── aula46/             # Name and age input, string operations, and basic validation
├── aula50/             # Small input exercises: time-based greetings, names, and parity
├── aula76/             # Word-guessing game
├── aula86/             # Lists and item indexes
├── aula90/             # Interactive list manager
├── aula98/             # CPF input and validation exercise
├── aula113/            # Functions for products and number parity
├── aula118/            # Nested functions and multiplication closures
├── aula125/            # Command-line quiz
├── aula133/            # Finding duplicate values in lists
├── aula161/            # Copying and sorting product dictionaries
├── aula163/            # Function factories and closures
├── collatz_conjecture/ # Collatz (3n + 1) sequence experiment
├── cpf_generator/      # CPF generation and validation exercises
├── exercícios/         # Miscellaneous exercises, including Fibonacci and sorting
├── filter/             # Webcam-to-ASCII streaming prototype using Flask and OpenCV
├── full_guide_py/      # Python syntax and feature notes/examples
├── imc/                # Body Mass Index (BMI) calculator
├── module_test/        # Experiments with Python modules and numeric formatting
├── parity_list/        # Collecting integers and counting even/odd values
├── quadratic_formula/  # Solving quadratic equations
├── rps_test/           # Rock-paper-scissors game
├── turtle_test/        # Drawing experiments with Python Turtle
└── while/              # Exercises using while loops and nested loops
```

The `aula*` folders contain examples associated with individual lessons. The other folders group standalone projects or exercises by topic.

## Setup

The external dependencies are used by the webcam filter in `filter/`. Create and activate a virtual environment, then install them with:

```bash
python -m venv .venv
python -m pip install -r requirements.txt
```

The `.venv/` directory is ignored by Git; only the dependency list is tracked.

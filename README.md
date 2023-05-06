# Leo Program Runner

This Python package provides a way to import and interact with Leo programs. The package dynamically creates a Python class that represents the loaded Leo program, with its associated structs and functions.

## Implementation

The Leo Program Runner works by parsing the source code of the Leo program and dynamically constructing a Python class based on its content. The structs and records defined in the Leo program are represented as member variables of the generated Python class, while the `transition` functions are transformed into Python methods.

When you call a method (i.e., a `transition` function) in the Python class, the Leo Program Runner will automatically convert the provided arguments into the appropriate format for Leo programs and perform the computation.

## Installation

You can install the package using pip:

```bash
pip install git+https://github.com/snowtigersoft/run_leo.git
```

## Usages
Here's an example of how to use the Leo Program Runner:

```python
from run_leo import import_leo_program

# Import the Leo program from a specific directory
leo_program = import_leo_program('./leo_examples/tictactoe')

# Call the available functions in the Leo program
leo_program.call_functions()
```

The import_leo_program() function takes the path to the Leo program's directory as its argument. The returned object will have methods and attributes that correspond to the structs and functions defined in the Leo program.

## Example Programs

The `tests/leo_examples` directory contains example Leo programs from the [AleoHQ/workshop](https://github.com/AleoHQ/workshop) repository. You can experience the effect of running a Leo program through Python by executing the `test_leo_program.py` file.


## Notes
Please note that this package assumes that the Leo program has a main.leo file in the src directory, and the specified path should point to the Leo program's root directory.

If you encounter any issues while using this package, please ensure that your Leo program follows the expected directory structure and file naming conventions.

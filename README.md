# Leo Program Runner

The Leo Program Runner is a Python package that bridges the gap between Leo programs and the Python environment. It allows for seamless interaction with Leo programs and significantly simplifies the development process. By dynamically generating Python classes that serve as representatives of the loaded Leo programs, along with their associated structs and functions, it brings the power of Leo programs to the Python ecosystem.

## How it works

The Leo Program Runner operates by parsing the source code of a Leo program and dynamically constructing a Python class based on its contents. The structs and records defined in the Leo program are represented as member variables of the dynamically-generated Python class, while the `transition` functions are transformed into Python methods.

In the import sections of Leo programs, the naming of structs and records will be slightly altered. For instance, `board.leo/board_state.record` in Leo will be translated into the `board__board_state` attribute of the auto-generated class.

The Leo Program Runner also offers automatic conversion between Python and Leo data types. When you call a method (representing a `transition` function) of the Python class, it takes care of converting the provided arguments into a format suitable for Leo programs, executes the computation, and then converts the results back into a Python-friendly format. This ensures a seamless development experience, making the interaction with a Leo program feel just like working with a Python package.

## Installation

You can easily install the package using pip:

```bash
pip install git+https://github.com/snowtigersoft/run_leo.git
```

## Usage

The Leo Program Runner supports the creation of Aleo accounts. You can create a new account by simply calling `Account.new()`.

```python
from run_leo import Account

acc = Account.new()
# Save to a file
acc.save('/path/to/file')
# Load from a file
acc2 = Account.load('/path/to/file')
```

Here's an example of how you can use the Leo Program Runner:

```python
from run_leo import import_leo_program, Account

# Import the Leo program from a specific directory
leo_program = import_leo_program('./leo_examples/tictactoe')

# set the account use for leo program
acc = Account.new()
leo_program.set_account(acc)

# Call the available functions in the Leo program
leo_program.call_functions()
```

The `import_leo_program()` function requires the path to the Leo program's directory as its argument. The returned object will have methods and attributes that correspond to the structs and functions defined in the Leo program.



## Interactive Example Programs

In the `examples` directory, there is an interactive program `play_tic_tac_toe.py` that lets you experience playing Tic Tac Toe. Players 1 and 2 take turns to place their markers, and the Leo program determines who wins.

You can also find more example Leo programs in the `tests/leo_examples` directory. These examples are taken from the [AleoHQ/workshop](https://github.com/AleoHQ/workshop) repository. If you want to experience running a Leo program through Python, just execute the test_leo_program.py file.

## Important Notes

Please note that this package assumes that there is a `main.leo` file in the `src` directory of the Leo program and that the path provided should point to the Leo program's root directory. If you encounter any issues while using this package, please ensure that your Leo program adheres to the expected directory structure and file naming conventions.
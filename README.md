
# Python Code Obfuscator

This is a Python script that obfuscates Python code by renaming variables and function names to randomized, hard-to-read names while preserving the functionality of the original code. 

## Features

- **Customizable obfuscation**: Specify the length of obfuscated names.
- **Automatic detection**: Detects and skips obfuscation for built-in names, imported modules, and essential functions. (almost always)
- **String safety**: Leaves string literals and comments untouched to avoid breaking code functionality.
- **Output to a new file**: Saves the obfuscated code in a separate file, leaving the original file untouched.

## Requirements

- Python 3.6 or higher.

## Usage

Run the script from the command line and specify the input file, length of obfuscated names, and output file.

### Command-Line Arguments

| Argument | Description                                                   | Example                               |
|----------|---------------------------------------------------------------|---------------------------------------|
| `-i` / `--input` | Input Python file to obfuscate.                              | `-i input.py`                        |
| `-l` / `--length` | Length of the obfuscated names (default: 16, must be > 3).  | `-l 16`                              |
| `-o` / `--output` | Output file to save the obfuscated Python code.            | `-o obfuscated.py`                   |

### Example Usage

```bash
python obfuscator.py -i example.py -l 16 -o obfuscated_example.py
```

This will read the file `example.py`, obfuscate it with randomized names of length 16, and save the result in `obfuscated_example.py`.

## How It Works

1. **Parse the code**: The script uses the `ast` module to parse the input Python file and analyze its structure.
2. **Collect names**: It identifies variable and function names, skipping:
   - Built-in Python names.
   - Imported module names and their functions/classes.
   - Names listed in the `NO_OBFUSCATE` set.
3. **Generate random names**: Uses the `random` module to generate randomized names of the specified length.
4. **Replace names**: Substitutes the original names with the randomized names while ensuring the code remains functional.
5. **Token safety**: Leaves string literals, comments, and other tokens untouched to preserve readability in necessary areas.
6. **Save the output**: Writes the obfuscated code to the specified output file.

## Limitations

- The `NO_OBFUSCATE` set contains names that the script avoids obfuscating. It's there only because I couldn't fix the issues that occur without it. You will need to add keywords depending on your use case
- Length of obfuscated names must be greater than 3 to avoid unexpected issues.

## Example Input and Output

### Input (`example.py`):
```python
def greet(name):
    print(f"Name: , {name}")

greet("Alice")
```

### Command:
```bash
python obfuscator.py -i example.py -l 16 -o obfuscated_example.py
```

### Output (`obfuscated_example.py`):
```python
def xzhlrvioukiqjkyo(ahtjqcvqjdakllay):
    print(f"Name: , {ahtjqcvqjdakllay}")

xzhlrvioukiqjkyo("Alice")
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**Developed by stigsec**  

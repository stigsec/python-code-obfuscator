import random
import string
import ast
import re
import argparse

NO_OBFUSCATE = set([            #this is here because I couldn't fix these
    'os', 'sys', 'random', 'string', 'ast', 're', 'open', 'print', 'exit',      #you could probably get rid of some of them
    'getattr', 'setattr', 'delattr', 'hasattr', 'int', 'str', 'list', 'dict',
    'tuple', 'range', 'len', 'type', 'isinstance', 'dir', 'id', 'input',
    'sum', 'min', 'max', 'map', 'filter', 'sorted', 'enumerate', 'zip', '_',
    'path', '__init__', '__main__'
])

def add_module_functions(module_name, no_obfuscate):
    try:
        module = __import__(module_name)
        for name in dir(module):
            no_obfuscate.add(name)
            if '.' in name:
                submodule = name.split('.')[0]
                no_obfuscate.add(submodule)
    except ImportError:
        pass

def collect_imported_modules(filename):
    with open(filename, 'r') as f:
        source_code = f.read()

    tree = ast.parse(source_code)
    imported_modules = set()

    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                imported_modules.add(alias.name if isinstance(node, ast.Import) else node.module)
                if isinstance(node, ast.ImportFrom):
                    imported_modules.add(alias.name)

    return imported_modules

def generate_random_name(length):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def collect_names(node, name_map, imported_modules, imported_functions_classes, no_obfuscate, length):
    builtins = dir(__builtins__)

    if isinstance(node, ast.FunctionDef):
        if node.name not in builtins and node.name not in imported_functions_classes and node.name not in no_obfuscate:
            name_map[node.name] = generate_random_name(length)

    elif isinstance(node, ast.Name):
        if node.id not in builtins and node.id not in imported_modules and node.id not in imported_functions_classes and node.id not in no_obfuscate:
            if node.id not in name_map:
                name_map[node.id] = generate_random_name(length)

    for child in ast.iter_child_nodes(node):
        collect_names(child, name_map, imported_modules, imported_functions_classes, no_obfuscate, length)

def obfuscate_and_replace(file_path, length, output_file):
    name_map = {}
    imported_modules = collect_imported_modules(file_path)

    for module in imported_modules:
        add_module_functions(module, NO_OBFUSCATE)

    with open(file_path, 'r') as f:
        source_code = f.read()

    tree = ast.parse(source_code)

    imported_functions_classes = {alias.name for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) for alias in node.names}

    collect_names(tree, name_map, imported_modules, imported_functions_classes, NO_OBFUSCATE, length)

    def replace_match(match):
        name = match.group(0)
        return name_map.get(name, name)

    pattern = r'\b(?:' + '|'.join(re.escape(k) for k in name_map.keys()) + r')\b'
    updated_code = re.sub(pattern, replace_match, source_code)

    with open(output_file, 'w') as file:
        file.write(updated_code)
    print(f"File has been obfuscated successfully")

def main():
    parser = argparse.ArgumentParser(description="Python Code Obfuscator", epilog="by stigsec")
    parser.add_argument('-i', '--input', required=True, help="Input Python code")
    parser.add_argument('-l', '--length', type=int, default=16, help="Length of obfuscated names")
    parser.add_argument('-o', '--output', required=True, help="Output file")

    args = parser.parse_args()

    if args.length <= 3:        #if less than 3, weird problems occur
        print("Error: Length must be greater than 3.")
        return

    obfuscate_and_replace(args.input, args.length, args.output)

if __name__ == "__main__":
    main()
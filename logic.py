import re

def is_valid_variable(name, declared_vars):
    return name in declared_vars

def parse_program(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    declared_vars = set()
    declared_procs = {}
    
    program_valid = True
    inside_proc = False
    current_proc = None
    
    for line in lines:
        line = line.strip()
        
        # Ignore empty lines
        if not line:
            continue
        
        # Variable Declaration
        if line.startswith("|") and line.endswith("|"):
            vars_list = line.strip('|').split()
            declared_vars.update(vars_list)
        
        # Procedure Declaration
        elif line.startswith("proc"):
            match = re.match(r'proc\s+([a-z][a-zA-Z0-9]*:?)(?:\s+(.+))?\s*\[', line)
            if match:
                proc_name, params = match.groups()
                declared_procs[proc_name] = set()
                if params:
                    declared_procs[proc_name] = set(params.split())
                inside_proc = True
                current_proc = proc_name
            else:
                print(f"Error: Sintaxis incorrecta en declaración de procedimiento: {line}")
                program_valid = False
        
        # Closing procedure
        elif line == "]" and inside_proc:
            inside_proc = False
            current_proc = None
        
        # Instruction Validation
        elif inside_proc or line.startswith("[") or line.endswith("]"):
            tokens = line.split()
            if tokens[0] in ["move:", "turn:", "face:", "put:", "pick:", "goto:", "jump:"]:
                if not is_valid_variable(tokens[1], declared_vars) and not tokens[1].isdigit():
                    print(f"Error: Uso de variable no declarada en {line}")
                    program_valid = False
            elif tokens[0] in declared_procs:
                params = tokens[1:]
                if set(params) != declared_procs[tokens[0]]:
                    print(f"Error: Llamada incorrecta al procedimiento {tokens[0]} en {line}")
                    program_valid = False
        
        else:
            print(f"Error: Sintaxis inválida en {line}")
            program_valid = False
    
    return program_valid

if __name__ == "__main__":
    filename = "robot_code.txt"  # Reemplaza con el nombre del archivo de entrada
    if parse_program(filename):
        print("Sí")
    else:
        print("No")
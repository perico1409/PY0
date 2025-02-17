import re

def parse_robot_code(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            code = file.read()
    except FileNotFoundError:
        print("Error: File not found.")
        return False
    
    # Definir regex para sintaxis básica
    variable_declaration = re.compile(r'\|[a-z]+(?:\s+[a-z]+)*\|')
    procedure_declaration = re.compile(r'proc\s+[a-zA-Z_:]+(?:\s+[a-zA-Z_:]+)*\s*\[.*?\]', re.DOTALL)
    procedure_call = re.compile(r'[a-zA-Z_:]+(?:\s+[a-zA-Z_:]+)*\.')
    
    # Validar estructura de variables
    if not variable_declaration.search(code):
        print("Error: No valid variable declaration found.")
        return False
    
    # Validar procedimientos
    procedures = procedure_declaration.findall(code)
    if not procedures:
        print("Error: No valid procedures found.")
        return False
    
    # Validar llamadas a procedimientos
    calls = procedure_call.findall(code)
    defined_procs = {p.split()[1] for p in procedures}
    for call in calls:
        proc_name = call.split()[0]
        if proc_name not in defined_procs:
            print(f"Error: Undefined procedure called - {proc_name}")
            return False
    
    print("Syntax is correct.")
    return True
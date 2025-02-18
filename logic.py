def parse_robot_code(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            code = file.read().strip().splitlines()
    except FileNotFoundError:
        print("Error: File not found.")
        return False
    
    variables = set()
    procedures = {}
    procedure_calls = []
    
    # Paso 1: Recorrer cada línea y verificar variables y procedimientos
    for line in code:
        line = line.strip()
        
        # Validar declaración de variables
        if line.startswith('|'):
            # Declarar variables
            line = line[1:-1].strip()  # Eliminar las barras "|"
            vars_in_line = line.split()
            if vars_in_line:
                for var in vars_in_line:
                    if not var.islower():  # Las variables deben estar en minúscula
                        print(f"Error: Variable '{var}' debe estar en minúscula.")
                        return False
                    variables.add(var)
        
        # Validar declaración de procedimientos
        elif line.startswith('proc'):
            # Procesar declaración de procedimiento
            proc_name_end = line.find(':')
            if proc_name_end == -1:
                print(f"Error: El procedimiento no tiene parámetros definidos correctamente en: {line}")
                return False
            proc_name = line[4:proc_name_end].strip()
            if proc_name not in procedures:
                procedures[proc_name] = []  # Crear procedimiento vacío en el diccionario
            # Guardamos la línea del procedimiento para posteriores validaciones.
            procedures[proc_name].append(line)
        
        # Verificar llamadas a procedimientos
        elif '.' in line:
            # Se espera una llamada a un procedimiento
            proc_name = line.split(':')[0].strip()
            if proc_name not in procedures:
                print(f"Error: Procedimiento '{proc_name}' no está definido.")
                return False
            procedure_calls.append(proc_name)
    
    # Paso 2: Verificación de que todas las llamadas a procedimientos son válidas
    for proc in procedure_calls:
        if proc not in procedures:
            print(f"Error: Procedimiento '{proc}' llamado pero no existe.")
            return False
    
    # Paso 3: Verificación de cierre correcto de bloques de procedimiento
    for proc, lines in procedures.items():
        if not any(line.endswith(']') for line in lines):
            print(f"Error: El procedimiento '{proc}' no tiene un bloque correctamente cerrado.")
            return False
    
    print("Syntax is correct.")
    return True
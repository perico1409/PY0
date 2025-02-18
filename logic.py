def analizar_codigo_robot(nombre_archivo):
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            codigo = [linea.strip() for linea in archivo if linea.strip()]
    except FileNotFoundError:
        print("Error: Archivo no encontrado.")
        return False

    variables_globales = set()
    procedimientos = {}
    variables_locales = {}
    comandos_validos = {
        'move', 'turn', 'face', 'put', 'pick', 'jump', 'goTo', 'nop',
        'if', 'while', 'repeatTimes', 'canMove', 'canPick', 'canPut'
    }

    def limpiar_linea(linea):
        if '#' in linea:
            linea = linea[:linea.index('#')]
        return linea.strip()

    en_procedimiento = False
    proc_actual = None
    contenido_actual = []

    for linea in codigo:
        linea = limpiar_linea(linea)
        if not linea:
            continue
        if linea.startswith('|'):
            if not linea.endswith('|'):
                print(f"Error: Bloque de declaración de variables no está cerrado correctamente: {linea}")
                return False
            vars_en_linea = linea[1:-1].strip().split()
            for var in vars_en_linea:
                var = var.replace(',', '').strip() 
                if not var.islower() or not var.isalnum():
                    print(f"Error: Variable '{var}' debe estar en minúsculas y ser alfanumérica.")
                    return False
                variables_globales.add(var)

        elif linea.startswith('proc '):
            nombre_completo = linea[5:].split('[')[0].strip() 
            if nombre_completo[0].isupper():
                print(f"Error: El nombre del procedimiento '{nombre_completo}' no debe comenzar con mayúscula.")
                return False

            proc_actual = nombre_completo
            en_procedimiento = True
            contenido_actual = []

            print(f"Debug: Procedimiento encontrado - {nombre_completo}")
        elif en_procedimiento and linea.startswith('|'):
            if not linea.endswith('|'):
                print(f"Error: Bloque de declaración de variables locales no está cerrado correctamente: {linea}")
                return False
            vars_locales = linea[1:-1].split(',') 
            variables_locales[proc_actual] = {v.strip() for v in vars_locales}
        elif linea.endswith(']'):
            if en_procedimiento:
                contenido_actual.append(linea)
                procedimientos[proc_actual] = contenido_actual
                en_procedimiento = False
                proc_actual = None
                contenido_actual = []

        elif en_procedimiento:
            contenido_actual.append(linea)
    for linea in codigo:
        linea = limpiar_linea(linea)
        if not linea:
            continue

        if ':=' in linea:
            if not linea.endswith('.'):
                print(f"Error: Falta el punto al final de la asignación: {linea}")
                return False

    print("La sintaxis es correcta.")
    return True

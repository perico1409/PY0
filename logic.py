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
        # Eliminar comentarios
        if '#' in linea:
            linea = linea[:linea.index('#')]
        return linea.strip()

    def validar_nombre_proc(nombre):
        # Acepta nombres de procedimientos con parámetros, incluyendo 'and' o cualquier identificador
        partes = nombre.split()
        for parte in partes:
            # Verificar que cada parte sea alfanumérica o ':' o 'and' como un separador
            if not (parte.isalnum() or parte == ':' or parte == 'and' or parte.isalpha()):
                return False
        return True

    # Primera pasada: recolectar variables y procedimientos
    en_procedimiento = False
    proc_actual = None
    contenido_actual = []

    for linea in codigo:
        linea = limpiar_linea(linea)
        if not linea:
            continue

        # Procesar variables globales
        if linea.startswith('|'):
            if not linea.endswith('|'):
                print(f"Error: Bloque de declaración de variables no está cerrado correctamente: {linea}")
                return False
            vars_en_linea = linea[1:-1].strip().split()
            for var in vars_en_linea:
                # Eliminar comas y espacios adicionales de las variables
                var = var.replace(',', '').strip()  # Eliminar comas
                if not var.islower() or not var.isalnum():
                    print(f"Error: Variable '{var}' debe estar en minúsculas y ser alfanumérica.")
                    return False
                variables_globales.add(var)

        # Procesar procedimientos
        elif linea.startswith('proc '):
            if en_procedimiento:
                procedimientos[proc_actual] = contenido_actual
            
            en_procedimiento = True
            nombre_completo = linea[5:].split('[')[0].strip()
            proc_actual = nombre_completo
            contenido_actual = []
            
            if '[' in linea and ']' in linea and linea.index('[') > linea.index(']'):
                print(f"Error: Formato inválido de procedimiento: {linea}")
                return False

        # Procesar variables locales en procedimientos
        elif en_procedimiento and linea.startswith('|'):
            if not linea.endswith('|'):
                print(f"Error: Bloque de declaración de variables locales no está cerrado correctamente: {linea}")
                return False
            vars_locales = linea[1:-1].split(',')
            variables_locales[proc_actual] = {v.strip() for v in vars_locales}

        # Fin de procedimiento
        elif linea.endswith(']'):
            if en_procedimiento:
                contenido_actual.append(linea)
                procedimientos[proc_actual] = contenido_actual
                en_procedimiento = False
                proc_actual = None
                contenido_actual = []

        # Contenido de procedimiento
        elif en_procedimiento:
            contenido_actual.append(linea)

    # Segunda pasada: validar instrucciones
    en_bloque_principal = False
    
    for linea in codigo:
        linea = limpiar_linea(linea)
        if not linea:
            continue

        print(f"Verificando línea: {linea}")  # Mensaje de depuración para ver qué se está procesando

        if linea == '[':
            en_bloque_principal = True
        elif linea == ']':
            en_bloque_principal = False
        elif en_bloque_principal:
            # Verificar que las asignaciones terminen con un punto
            if ':=' in linea:
                if not linea.endswith('.'):
                    print(f"Error: Falta el punto al final de la asignación: {linea}")  # Mensaje de depuración
                    return False

            # Validar llamadas a procedimientos y comandos
            if ':' in linea and not linea.startswith('|'):
                partes = linea.split(':')
                comando = partes[0].strip()
                
                # Verificar si es un comando válido o una llamada a procedimiento
                encontrado = False
                for proc in procedimientos:
                    nombre_base_proc = proc.split(':')[0].strip()
                    if comando == nombre_base_proc:
                        encontrado = True
                        break
                
                if not encontrado and comando not in comandos_validos:
                    print(f"Error: Comando o procedimiento inválido: {comando}")
                    return False

    print("La sintaxis es correcta.")
    return True

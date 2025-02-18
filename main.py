import logic as lg
import os

# Definir el directorio donde están los archivos
data_dir = os.path.dirname(os.path.abspath(__file__))  # Usamos __file__ para obtener la ruta absoluta

if __name__ == "__main__":
    # Obtener el nombre del archivo desde el usuario
    filename = input("Digite el nombre del archivo (sin .txt):") + ".txt"

    # Concatenar la ruta completa del archivo
    full_path = os.path.join(data_dir, filename)

    # Verificar si el archivo existe y luego procesarlo
    if os.path.isfile(full_path):
        if lg.analizar_codigo_robot(full_path):
            print("Sí cumple")
        else:
            print("No cumple")
    else:
        print(f"Error: El archivo {filename} no existe.")
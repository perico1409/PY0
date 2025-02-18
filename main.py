import logic as lg
import os

data_dir = os.path.dirname(os.path.abspath(__file__)) 

if __name__ == "__main__":
    filename = input("Digite el nombre del archivo (sin .txt):") + ".txt"
    full_path = os.path.join(data_dir, filename)
    if os.path.isfile(full_path):
        if lg.analizar_codigo_robot(full_path):
            print("Sí cumple")
        else:
            print("No cumple")
    else:
        print(f"Error: El archivo {filename} no existe.")
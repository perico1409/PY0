import logic as lg
import os

data_dir = os.path.dirname(os.path.realpath('__file__')) + '/PY0/'


if __name__ == "__main__":
    
    filename = input("digite el nombre del archivo:") + ".txt" 
    if lg.parse_robot_code(filename):
        print("Sí cumple")
    else:
        print("No cumple")
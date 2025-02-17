import logic as lg




if __name__ == "__main__":
    
    filename = input("digite el nombre del archivo:") + ".txt" 
    if lg.parse_program(filename):
        print("Sí")
    else:
        print("No")
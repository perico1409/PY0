import logic as lg

if __name__ == "__main__":
    filename = "robot_code.txt"  
    if lg.parse_program(filename):
        print("Sí")
    else:
        print("No")
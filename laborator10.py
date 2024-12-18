import sys
import os

valid = False

def citire_consola():
    print("\naici fac citirea din consola")

def citire_fisier(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError("File does not exist!")
    
    if not os.path.isfile(file_path):
        raise FileNotFoundError("File does not exist!")

    try:
        with open(file_path, 'r') as file:
            text = file.read()
            print(f"\nTextul citit din fisier: {text}\n")
    except Exception as e:
        print(e)

    return text

while not valid: 
    option = input(f"\nCum doriti sa inserati textul? [Consola/Fisier]\n")

    if option.lower() == "consola":
        citire_consola()
        valid = True
        text = input("\nIntroduceti textul: ")
        print(f"\nTextul este: {text}\n")

    elif option.lower() == "fisier":
        valid = True
        file_path = input("\nIntroduceti calea catre fisier: ")
        print(f"\nCalea primita: {file_path}\n")
        citire_fisier(file_path)

    else: 
        print("\noptiune invalida!")
        valid = False
        continue
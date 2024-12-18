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
        citire_fisier(file_path)
        print(f"\nCalea primita: {file_path}\n")

    else: 
        print("\noptiune invalida!")
        valid = False
        continue
import sys
import os
from langdetect import detect, detect_langs

valid = False

def detectare_limba(text):
    try:
        lang = detect(text)
        prob = detect_langs(text)

        print(f"Textul este scris in limba: {lang}")
        print(f"Probabilitati detaliate: {prob}")

    except Exception as e:
        print(f"Eroare la detectarea limbii: {e}")

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
        detectare_limba(text)

    elif option.lower() == "fisier":
        valid = True
        file_path = input("\nIntroduceti calea catre fisier: ")
        print(f"\nCalea primita: {file_path}\n")
        text = citire_fisier(file_path)
        detectare_limba(text)

    else: 
        print("\noptiune invalida!")
        valid = False
        continue
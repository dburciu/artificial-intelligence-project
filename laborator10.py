import os
from langdetect import detect, detect_langs
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
from collections import Counter

valid = False

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')

# Generez dinamic o mapare intre codurile date de langdetec si cele suportate de nltk
# stopwords.fileids() va returna lista cu limbile suportate de nltk
# lang[:2] preia primele 2 caractere pentru a putea compune coduri pentru fiecare limba -> ro ~ romanian

lang_to_nltk = {lang[:2]: lang for lang in stopwords.fileids()}

def detectare_limba(text):
    try:
        lang = detect(text)
        prob = detect_langs(text)

        print(f"Textul este scris in limba: {lang}")
        print(f"Probabilitati detaliate: {prob}")

    except Exception as e:
        print(f"Eroare la detectarea limbii: {e}")
    
    return lang

def informatii_stilometrice(text, lang):

    lang_nltk = lang_to_nltk.get(lang, "english")
    print(f"\n\n\nLimba este: {lang_nltk}")

    # lungimea in caractere

    char_len = len(text)

    # lungimea in cuvinte

    words = word_tokenize(text)

    # lungime cuvinte

    words_len = len(words)

    # frecventa cuvintelor

    words_freq = Counter(words)

    # Analizam care sunt cele mai semnificative cuvinte din text

    stop_words = set(stopwords.words(lang_nltk))

    important_words = [
        word.lower() for word in words if word.lower() not in stop_words and word.isalpha()
    ]

    important_words_freq = Counter(important_words)

    # Numarul de propozitii

    nb_of_phrases = len(re.split(r'[.!?]', text)) - 1

    # Media cuvintelor per propozitie

    words_mean = words_len / nb_of_phrases if nb_of_phrases > 0 else 0

    print(f"\nLungimea textului in cuvinte: {words}")
    print(f"\nLungimea textului in caractere: {char_len}")
    print(f"\nCele mai frecvente cuvinte(toate): ")

    for w, frq in words_freq.most_common(10):
        print(f"  {w}: {frq}")
    
    print(f"\nCele mai frecvente cuvinte(importante): ")

    for w, frq in important_words_freq.most_common(10):
        print(f"  {w}: {frq}")

    print(f"\nNumarul de propozitii: {nb_of_phrases}")
    print(f"\nMedia cuvintelor per propozitie: {words_mean:.2f}\n")
    

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
        valid = True
        text = input("\nIntroduceti textul: ")
        print(f"\nTextul este: {text}\n")
        lang = detectare_limba(text)
        informatii_stilometrice(text, lang)

    elif option.lower() == "fisier":
        valid = True
        file_path = input("\nIntroduceti calea catre fisier: ")
        print(f"\nCalea primita: {file_path}\n")
        text = citire_fisier(file_path)
        lang = detectare_limba(text)
        informatii_stilometrice(text, lang)

    else: 
        print("\noptiune invalida!")
        valid = False
        continue
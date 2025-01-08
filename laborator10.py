import os
from langdetect import detect, detect_langs
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
from collections import Counter
import matplotlib.pyplot as plt

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

    # Lungimea textului in caractere

    plt.figure(figsize=(5, 5))
    plt.bar(['Lungimea în caractere'], [char_len], color='blue')
    plt.title('Lungimea textului în caractere')
    plt.ylabel('Număr de caractere')
    plt.tight_layout()
    plt.show()

    # Lungimea textului in cuvinte

    plt.figure(figsize=(5, 5))
    plt.bar(['Lungimea în cuvinte'], [words_len], color='cyan')
    plt.title('Lungimea textului în cuvinte')
    plt.ylabel('Număr de cuvinte')
    plt.tight_layout()
    plt.show()

    # Frecventa cuvintelor (toate)

    most_common_words = words_freq.most_common(10)
    words_labels, words_values = zip(*most_common_words)

    plt.figure(figsize=(10, 5))
    plt.bar(words_labels, words_values, color='skyblue')
    plt.title('Cele mai frecvente cuvinte (toate)')
    plt.ylabel('Frecvența')
    plt.xlabel('Cuvinte')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Frecventa cuvintelor (cele mai importante)

    most_common_important_words = important_words_freq.most_common(10)
    important_words_labels, important_words_values = zip(*most_common_important_words)

    plt.figure(figsize=(10, 5))
    plt.bar(important_words_labels, important_words_values, color='orange')
    plt.title('Cele mai frecvente cuvinte (importante)')
    plt.ylabel('Frecvența')
    plt.xlabel('Cuvinte')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Distributia numarului de cuvinte per propozitie

    plt.figure(figsize=(5, 5))
    plt.bar(['Media cuvintelor/propozitie'], [words_mean], color='green')
    plt.title('Media cuvintelor per propoziție')
    plt.ylabel('Numărul mediu de cuvinte')
    plt.tight_layout()
    plt.show()

    # Numarul total de propozitii

    plt.figure(figsize=(5, 5))
    plt.bar(['Numărul de propoziții'], [nb_of_phrases], color='purple')
    plt.title('Numărul total de propoziții')
    plt.ylabel('Număr')
    plt.tight_layout()
    plt.show()


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

## punctul 4

from nltk.corpus import wordnet
import random
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import nltk

nltk.download('wordnet')
nltk.download('omw-1.4')


def get_synonyms(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name().replace('_', ' '))
    return list(set(synonyms))


def get_hypernyms(word):
    hypernyms = []
    for syn in wordnet.synsets(word):
        for hyper in syn.hypernyms():
            for lemma in hyper.lemmas():
                hypernyms.append(lemma.name().replace('_', ' '))
    return list(set(hypernyms))


# antonime NEGATE
def get_antonyms(word):
    antonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            if lemma.antonyms():
                antonyms.append('not ' + lemma.antonyms()[0].name().replace('_', ' '))
    return antonyms


def replace_words(text):
    words = word_tokenize(text)
    new_words = words[:]
    stop_words = set(stopwords.words('english'))

    # filtrez cuvintele relevante (fără stopwords și doar cuvinte alfabetice)
    filtered_words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]

    # aleg 20% din cuvinte filtrate pentru a le schimba
    num_to_replace = int(len(words) * 0.2)
    important_words = random.sample(filtered_words, num_to_replace)

    for i, word in enumerate(words):
        if word.lower() in important_words and word.isalpha():
            synonyms = get_synonyms(word)
            hypernyms = get_hypernyms(word)
            antonyms = get_antonyms(word)
            replacements = synonyms + hypernyms + antonyms

            if replacements:
                new_words[i] = random.choice(replacements)

    return ' '.join(new_words)


test_text1 = "The cat has a lot of personality. She is fluffy and full of energy."
print("Text original:", test_text1)
alternative_text1 = replace_words(test_text1)
print("Text alternativ:", alternative_text1)

test_text2 = "I can not imagine my life without her. "
print("Text original:", test_text2)
alternative_text2 = replace_words(test_text2)
print("Text alternativ:", alternative_text2)

test_text3 = "This is one of the reasons I would not let go of her even for all the money in the world."
print("Text original:", test_text3)
alternative_text3 = replace_words(test_text3)
print("Text alternativ:", alternative_text3)

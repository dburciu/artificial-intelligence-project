import pandas as pd  # Pentru "pd"
import random         # Pentru "random"
from collections import Counter
import spacy

# Funcție pentru a extrage toate cuvintele dintr-o coloană
def extrage_cuvinte_din_camp(file_path, camp_index):
    df = pd.read_excel(file_path)
    # Verificăm dacă indexul există
    if camp_index >= len(df.columns):
        print(f"Eroare: Câmpul {camp_index} nu există în fișier.")
        return []

    # Selectăm coloana specificată
    camp = df.iloc[:, camp_index].dropna()

    # Tokenizare simplă pe baza spațiilor și semnelor de punctuație
    cuvinte = []
    for valoare in camp:
        if isinstance(valoare, str):  # Verificăm dacă este un text
            cuvinte.extend(valoare.split())

    return cuvinte

# Funcție pentru a genera propoziții variate folosind cuvintele extrase
def genereaza_propozitii(cuvinte, numar_propozitii=5):
    nlp = spacy.load("en_core_web_sm")  # Încărcăm modelul de limbă
    text_combined = " ".join(cuvinte)
    doc = nlp(text_combined)

    # Creăm propoziții variate
    sentences = []
    for _ in range(numar_propozitii):
        # Alegem aleatoriu cuvinte din textul procesat pentru subiect, verb și complement
        subject = random.choice([token.text for token in doc if token.pos_ == "NOUN"])
        verb = random.choice([token.text for token in doc if token.pos_ == "VERB"])
        complement = random.choice([token.text for token in doc if token.pos_ in {"NOUN", "PROPN"}])
        adverb = random.choice([token.text for token in doc if token.pos_ == "ADV"] + [None])
        adjective = random.choice([token.text for token in doc if token.pos_ == "ADJ"] + [None])

        # Propoziții scurte: subiect + verb + complement
        if random.random() < 0.5:  # 50% șanse de propoziție scurtă
            propozitie = f"{subject.capitalize()} {verb} {complement}."
        else:
            # Propoziții mai lungi: adăugăm și adverbe sau adjective
            if adverb and adjective:
                propozitie = f"{subject.capitalize()} {verb} {complement} {adverb} și {adjective}."
            elif adverb:
                propozitie = f"{subject.capitalize()} {verb} {complement} {adverb}."
            elif adjective:
                propozitie = f"{subject.capitalize()} {verb} {complement} {adjective}."
            else:
                propozitie = f"{subject.capitalize()} {verb} {complement}."

        sentences.append(propozitie)
    
    return sentences

if __name__ == "__main__":
    file_path = "Data cat personality and predation Cordonnier et al.xlsx"
    camp_index = 28  # Indexul câmpului din care vrem să extragem date
    cuvinte = extrage_cuvinte_din_camp(file_path, camp_index)

    if cuvinte:
        # Analizăm frecvența cuvintelor
        frecventa_cuvintelor = Counter(cuvinte)
        print("Cele mai frecvente cuvinte:", frecventa_cuvintelor.most_common(10))

        # Generăm propoziții variate folosind cuvintele extrase
        propozitii = genereaza_propozitii(cuvinte, numar_propozitii=10)
        print("\nPropoziții generate:")
        for p in propozitii:
            print(p)

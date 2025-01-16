import pandas as pd
from deep_translator import GoogleTranslator
import warnings
import random
from faker import Faker

# Ignorarea tuturor warning-urilor
warnings.filterwarnings("ignore")


# Funcție pentru a traduce o celulă
def translate_cell(cell, source_lang='fr', target_lang='ro'):
    if isinstance(cell, str):
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        return translator.translate(cell)
    else:
        return cell


# Funcția de traducere a titlurilor coloanelor
def traduce_titluri(df, source_lang='fr', target_lang='ro'):
    translated_columns = {}
    for col in df.columns:
        if col != "Plus":
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            translated_columns[col] = translator.translate(col)
        else:
            translated_columns[col] = col  # Păstrează "Plus" netradus
    return df.rename(columns=translated_columns)


# Funcție pentru a verifica dacă documentul este deja tradus
def document_deja_tradus(df, source_lang='fr', target_lang='ro'):
    for col in df.columns:
        if col != "Plus":  # Exclude coloana "Plus" de la verificare
            translated_title = GoogleTranslator(source=source_lang, target=target_lang).translate(col)
            if translated_title == col:
                return True
    return False


# Funcție pentru a verifica duplicatele (ignora coloana "Plus")
def verifica_duplicate(df):
    df_comparable = df.drop(columns=["Plus"], errors="ignore")
    duplicate_mask = df_comparable.duplicated(keep=False)
    duplicate_rows = df[duplicate_mask]

    if not duplicate_rows.empty:
        print("\nRânduri duplicate:")
        print(duplicate_rows)


# Funcție pentru a verifica linii identice (ignorând prima coloană, a doua coloană și coloana "Plus")
def verifica_identice(df):
    df_comparable = df.drop(columns=[df.columns[0], df.columns[1], "Plus"], errors="ignore")
    duplicate_mask = df_comparable.duplicated(keep=False)
    duplicate_rows = df[duplicate_mask]

    if not duplicate_rows.empty:
        print("\nRânduri identice (ignorând prima coloană, a doua coloană și coloana 'Plus'):")
        print(duplicate_rows)


# Funcție pentru a genera și adăuga linii noi
def adauga_intrari_noi(file_path):
    fake = Faker()
    df = pd.read_excel(file_path)

    # Întreabă utilizatorul dacă dorește să adăuge intrări noi
    raspuns = input("Doriți să adăugați intrări noi? (da/nu): ").strip().lower()
    if raspuns != 'da':
        print("Nu se vor adăuga intrări noi.")
        return

    # Solicită numărul de intrări de adăugat
    try:
        nr_intrari = int(input("Introduceți numărul de intrări noi de adăugat: ").strip())
    except ValueError:
        print("Valoare invalidă. Operațiunea a fost anulată.")
        return

    # Generare de noi intrări conform specificațiilor
    for _ in range(nr_intrari):
        new_row = {}
        for col_index in range(len(df.columns)):
            new_row[df.columns[col_index]] = generate_value_by_position(col_index, fake)
        print(f"Intrare adăugată:\n{new_row}")  # Afișăm intrarea adăugată în terminal
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Salvează DataFrame-ul actualizat
    try:
        df.to_excel(file_path, index=False)
        print(f"{nr_intrari} intrări noi au fost adăugate cu succes.")
    except Exception as e:
        print(f"Eroare la salvarea fișierului: {e}")


# Funcție de generare a valorilor pentru fiecare coloană în funcție de specificații
def generate_value_by_position(col_index, fake):
    # Definirea generatorilor pentru fiecare coloană, în funcție de index
    column_generators = {
        0: lambda: random.randint(4000, 10000),
        1: lambda: fake.date_time_this_decade().strftime('%d/%m/%Y %I:%M:%S %p'),
        2: lambda: random.choice(['M', 'F']),
        3: lambda: random.choice(['Moinsde1', '1a2', '2a10', 'Plusde10']),
        4: lambda: random.choice(
            ['BEN', 'SBI', 'BRI', 'CHA', 'EUR', 'MCO', 'PER', 'RAG', 'SPH', 'ORI', 'TUV', 'Autre', 'NSP']),
        5: lambda: random.randint(1, 5),
        6: lambda: random.choice(['ASB', 'AAB', 'ML', 'MI']),
        7: lambda: random.choice(['U', 'PU', 'R']),
        8: lambda: random.randint(1, 5),
        9: lambda: random.randint(1, 4),
        10: lambda: random.randint(1, 5),
        11: lambda: random.randint(1, 5),
        12: lambda: random.randint(1, 5),
        13: lambda: random.randint(1, 5),
        14: lambda: random.randint(1, 5),
        15: lambda: random.randint(1, 5),
        16: lambda: random.randint(1, 5),
        17: lambda: random.randint(1, 5),
        18: lambda: random.randint(1, 5),
        19: lambda: random.randint(1, 5),
        20: lambda: random.randint(1, 5),
        21: lambda: random.randint(1, 5),
        22: lambda: random.randint(1, 5),
        23: lambda: random.randint(1, 5),
        24: lambda: random.randint(1, 5),
        25: lambda: random.choice(['1', '2', '3', 'NSP']),
        26: lambda: random.randint(1, 5),
        27: lambda: random.randint(1, 5),
    }

    # Verificăm dacă indexul coloanei este definit în generatori
    if col_index in column_generators:
        # print(f"Generează valoare pentru coloana {col_index}")  # Afișează în terminal
        return column_generators[col_index]()  # Returnează valoarea generată
    else:
        print(f"Coloana {col_index} nu este definită în generatori!")
        return None  # Returnează None dacă coloana nu există în dict


# Funcție principală pentru a modifica traducerea
def modifica_traducerea(file_path, source_lang='fr', target_lang='ro'):
    df = pd.read_excel(file_path)

    # Verifică dacă documentul este deja tradus
    is_translated = document_deja_tradus(df, source_lang, target_lang)

    if is_translated:
        print("Documentul este deja în limba dorită. Nu este necesară traducerea.")
        print("Documentul este deja tradus. Continuăm cu verificările suplimentare...\n")
    else:
        # Traducerea conținutului coloanei "Plus"
        df['Plus'] = df['Plus'].apply(lambda x: translate_cell(x, source_lang, target_lang))

    # Traducerea titlurilor de coloane
    df = traduce_titluri(df, source_lang, target_lang)

    # Verificarea duplicatelor
    verifica_duplicate(df)

    # Verificarea identicelor
    verifica_identice(df)

    # Salvează DataFrame-ul tradus în fișierul Excel
    df.to_excel(file_path, index=False)


if __name__ == "__main__":
    file_path = "Data cat personality and predation Cordonnier et al.xlsx"
    modifica_traducerea(file_path, source_lang='fr', target_lang='ro')
    adauga_intrari_noi(file_path)

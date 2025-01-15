import pandas as pd
from deep_translator import GoogleTranslator
import warnings

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
            # Dacă găsim un titlu deja tradus corect, considerăm că documentul este deja tradus
            if translated_title == col:
                return True
    return False

# Funcție pentru a verifica duplicatele (ignora coloana "Plus")
def verifica_duplicate(df):
    # Excludem coloana "Plus" din verificare
    df_comparable = df.drop(columns=["Plus"], errors="ignore")

    # Verificarea rândurilor identice pe baza tuturor câmpurilor
    duplicate_mask = df_comparable.duplicated(keep=False)
    duplicate_rows = df[duplicate_mask]

    if not duplicate_rows.empty:
        print("\nRânduri duplicate:")
        print(duplicate_rows)

# Funcție pentru a verifica linii identice (ignorând prima coloană, a doua coloană și coloana "Plus")
def verifica_identice(df):
    # Excludem prima coloană, a doua coloană și coloana "Plus"
    df_comparable = df.drop(columns=[df.columns[0], df.columns[1], "Plus"], errors="ignore")

    # Verificăm duplicatele doar pe baza coloanelor rămase
    duplicate_mask = df_comparable.duplicated(keep=False)
    duplicate_rows = df[duplicate_mask]

    if not duplicate_rows.empty:
        print("\nRânduri identice (ignorând prima coloană, a doua coloană și coloana 'Plus'):")
        print(duplicate_rows)

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

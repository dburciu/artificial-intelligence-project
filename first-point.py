import pandas as pd

def verifica_datele(file_path):
    df = pd.read_excel(file_path)

    # Verificarea valorilor lipsă
    missing_values = df.isnull().sum()
    if missing_values.any():
        print("Valori lipsă pe coloană:")
        print(missing_values[missing_values > 0])

    # Verificarea coloanelor duplicate
    duplicate_columns = df.columns[df.columns.duplicated()]
    if len(duplicate_columns) > 0:
        print("\nColoane duplicate:")
        print(duplicate_columns)

    # Verificarea rândurilor duplicate pe baza Row.names
    if 'Row.names' in df.columns:
        duplicate_row_names = df['Row.names'][df['Row.names'].duplicated()]
        if len(duplicate_row_names) > 0:
            print("\nRânduri duplicate 'Row.names':")
            print(duplicate_row_names.values)  # Afișează doar numerele rândurilor duplicate

    # Verificarea rândurilor identice după toate câmpurile (fără Horodateur și Row.names)
    fields_to_exclude = ['Horodateur', 'Row.names']
    df_comparable = df.drop(columns=fields_to_exclude, errors='ignore')  # Creează un dataframe fără aceste coloane

    # Identificarea rândurilor duplicate
    duplicate_mask = df_comparable.duplicated(keep=False)  # Flag pentru toate rândurile duplicate (inclusiv primul din grup)
    duplicate_rows_all_fields = df[duplicate_mask]  # Selectarea rândurilor duplicate

    if not duplicate_rows_all_fields.empty:
        print("\nRânduri identice (după toate câmpurile, fără 'Horodateur' și 'Row.names'):")
        
        # Gruparea și afișarea rândurilor care sunt duplicate între ele
        grouped_duplicates = df_comparable[duplicate_mask].groupby(list(df_comparable.columns), group_keys=False).apply(
            lambda x: list(x.index)
        )
        
        for group in grouped_duplicates:
            print(f"Rândurile identice: {group}")

    # Verificarea rândurilor identice după toate câmpurile (fără Horodateur, Row.names și Plus)
    fields_to_exclude.append('Plus')  # Adaugă 'Plus' la excluderi
    df_comparable = df.drop(columns=fields_to_exclude, errors='ignore')  # Creează un dataframe fără aceste coloane

    # Identificarea rândurilor duplicate
    duplicate_mask = df_comparable.duplicated(keep=False)  # Flag pentru toate rândurile duplicate (inclusiv primul din grup)
    duplicate_rows_all_fields = df[duplicate_mask]  # Selectarea rândurilor duplicate

    if not duplicate_rows_all_fields.empty:
        print("\nRânduri identice (după toate câmpurile, fără 'Horodateur', 'Row.names' și 'Plus'):")
        
        # Gruparea și afișarea rândurilor care sunt duplicate între ele
        grouped_duplicates = df_comparable[duplicate_mask].groupby(list(df_comparable.columns), group_keys=False).apply(
            lambda x: list(x.index)
        )
        
        for group in grouped_duplicates:
            print(f"Rândurile identice: {group}")

    # Salvarea erorilor într-un fișier de log doar dacă există erori
    with open('error_log.txt', 'w', encoding='utf-8') as f:
        if missing_values.any():
            f.write("Valori lipsă pe coloane:\n")
            f.write(str(missing_values[missing_values > 0]) + '\n\n')
        
        if len(duplicate_columns) > 0:
            f.write("Coloane duplicate:\n")
            f.write(str(duplicate_columns) + '\n\n')
        
        if 'Row.names' in df.columns and len(duplicate_row_names) > 0:
            f.write("Rânduri duplicate 'Row.names':\n")
            f.write(str(duplicate_row_names.values) + '\n\n')
        
        if not duplicate_rows_all_fields.empty:
            f.write("Rânduri identice (căutare fără câmpurile 'Horodateur' și 'Row.names'):\n")
            for group in grouped_duplicates:
                f.write(f"Rândurile identice: {group}\n")
        
        # Adăugăm și log pentru rândurile identice fără 'Horodateur', 'Row.names' și 'Plus'
        if not duplicate_rows_all_fields.empty:
            f.write("Rânduri identice (căutare fără câmpurile 'Horodateur', 'Row.names' și 'Plus'):\n")
            for group in grouped_duplicates:
                f.write(f"Rândurile identice: {group}\n")

if __name__ == "__main__":
    file_path = "Data cat personality and predation Cordonnier et al.xlsx"
    verifica_datele(file_path)

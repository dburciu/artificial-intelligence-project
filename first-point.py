import pandas as pd

def verifica_datele(file_path):
    df = pd.read_excel(file_path)

    # Verificarea valorilor lipsa
    missing_values = df.isnull().sum()
    if missing_values.any():
        print("Valori lipsa pe coloana:")
        print(missing_values[missing_values > 0])

    # Verificarea coloanelor duplicate
    duplicate_columns = df.columns[df.columns.duplicated()]
    if len(duplicate_columns) > 0:
        print("\nColoane duplicate:")
        print(duplicate_columns)

    # Verificarea randurilor duplicate pe baza Row.names
    if 'Row.names' in df.columns:
        duplicate_row_names = df['Row.names'][df['Row.names'].duplicated()]
        if len(duplicate_row_names) > 0:
            print("\nRanduri duplicate 'Row.names':")
            print(duplicate_row_names.values)  # Afiseaza doar numerele randurilor duplicate

    # Verificarea randurilor identice dupa toate campurile (fara Horodateur si Row.names)
    fields_to_exclude = ['Horodateur', 'Row.names']
    df_comparable = df.drop(columns=fields_to_exclude, errors='ignore')  # Creeaza un dataframe fara aceste coloane

    # Identificarea randurilor duplicate
    duplicate_mask = df_comparable.duplicated(keep=False)  # Flag pentru toate randurile duplicate (inclusiv primul din grup)
    duplicate_rows_all_fields = df[duplicate_mask]  # Selectarea randurilor duplicate

    if not duplicate_rows_all_fields.empty:
        print("\nRanduri identice (dupa toate campurile, fara 'Horodateur' si 'Row.names'):")
        
        # Gruparea si afisarea randurilor care sunt duplicate intre ele
        grouped_duplicates = df_comparable[duplicate_mask].groupby(list(df_comparable.columns)).apply(lambda x: list(df.loc[x.index, 'Row.names']))
        
        for group in grouped_duplicates:
            print(f"Randurile identice: {group}")

    # Verificarea randurilor identice dupa toate campurile (fara Horodateur, Row.names si Plus)
    fields_to_exclude.append('Plus')  # Adauga 'Plus' la excluderi
    df_comparable = df.drop(columns=fields_to_exclude, errors='ignore')  # Creeaza un dataframe fara aceste coloane

    # Identificarea randurilor duplicate
    duplicate_mask = df_comparable.duplicated(keep=False)  # Flag pentru toate randurile duplicate (inclusiv primul din grup)
    duplicate_rows_all_fields = df[duplicate_mask]  # Selectarea randurilor duplicate

    if not duplicate_rows_all_fields.empty:
        print("\nRanduri identice (dupa toate campurile, fara 'Horodateur', 'Row.names' si 'Plus'):")
        
        # Gruparea si afisarea randurilor care sunt duplicate intre ele
        grouped_duplicates = df_comparable[duplicate_mask].groupby(list(df_comparable.columns)).apply(lambda x: list(df.loc[x.index, 'Row.names']))
        
        for group in grouped_duplicates:
            print(f"Randurile identice: {group}")

    # Salvarea erorilor intr-un fisier de log doar daca exista erori
    with open('error_log.txt', 'w', encoding='utf-8') as f:
        if missing_values.any():
            f.write("Valori lipsa pe coloane:\n")
            f.write(str(missing_values[missing_values > 0]) + '\n\n')
        
        if len(duplicate_columns) > 0:
            f.write("Coloane duplicate:\n")
            f.write(str(duplicate_columns) + '\n\n')
        
        if 'Row.names' in df.columns and len(duplicate_row_names) > 0:
            f.write("Randuri duplicate 'Row.names':\n")
            f.write(str(duplicate_row_names.values) + '\n\n')
        
        if not duplicate_rows_all_fields.empty:
            f.write("Randuri identice (search fara campurile 'Horodateur' si 'Row.names'):\n")
            for group in grouped_duplicates:
                f.write(f"Randurile identice: {group}\n")
        
        # Adaugam si log pentru randurile identice fara 'Horodateur', 'Row.names' si 'Plus'
        if not duplicate_rows_all_fields.empty:
            f.write("Randuri identice (search fara campurile 'Horodateur', 'Row.names' si 'Plus'):\n")
            for group in grouped_duplicates:
                f.write(f"Randurile identice: {group}\n")

if __name__ == "__main__":
    file_path = "Data cat personality and predation Cordonnier et al.xlsx"
    verifica_datele(file_path)

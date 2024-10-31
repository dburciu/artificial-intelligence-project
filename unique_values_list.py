import pandas as pd

file_path = 'Data cat personality and predation Cordonnier et al.xlsx'
df = pd.read_excel(file_path)

columns = df.columns

results = {}

# Iterează prin fiecare coloană
for column in columns:
    unique_values = df[column].value_counts()
    results[column] = {
        'total_values': unique_values.sum(),
        'frequencies': unique_values.reset_index()  # Resetăm indexul pentru a afișa numele complet
    }

print("FRECVENTA LA NIVEL DE CLASA")

for column, data in results.items():
    print(f"\nAtribut: {column}")
    print(f"Numărul total de valori distincte: {data['total_values']}")
    print("Frecvența valorilor:")
    freq_df = data['frequencies']
    freq_df.columns = ['Valoare', 'Frecvență']  
    print(freq_df)

print("-------------------")
print("FRECVENTA LA NIVELUL INTREGULUI FISIER")

for column in df.columns:
    if column != 'Plus':
        unique_values = df[column].value_counts()
        total_values = unique_values.sum()  # Numărul total de valori din fisier

        print(f"\nAtribut: {column}")
        print(f"Numărul total de valori distincte: {len(unique_values)}")
        print(f"Numărul total de valori: {total_values}")
        print("Frecvența valorilor:")
        
        for value, frequency in unique_values.items():
            print(f"{value}: {frequency}")
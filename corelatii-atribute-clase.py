import pandas as pd
import os

# Specifică corect calea fișierului Excel
file_path = "Data cat personality and predation Cordonnier et al.xlsx"

# Citește fișierul Excel și gestionează posibilele excepții
try:
    df = pd.read_excel(file_path, sheet_name=0)  # Presupunând că primul sheet (index 0) trebuie citit
    print("Coloanele din DataFrame:", df.columns)  # Afișează coloanele disponibile
except FileNotFoundError:
    print(f"Fișierul nu a fost găsit: {file_path}")
    exit()
except ValueError as e:
    print(f"Eroare la citirea fișierului Excel: {e}")
    exit()

# Verifică dacă coloana 'Race' există
if 'Race' not in df.columns:
    print("Coloana 'Race' nu există în DataFrame.")
    exit()

# Șterge coloanele specificate, gestionând erorile dacă nu există
df = df.drop(columns=['Row.names', 'Horodateur', 'Logement', 'Zone', 'Ext', 'Obs', 'PredOiseau', 'PredMamm', 'Plus'], errors='ignore')

# Asigură-te că directorul de ieșire există
output_directory = 'auto'
os.makedirs(output_directory, exist_ok=True)

output_file = os.path.join(output_directory, 'analyse_cats_data.txt')

def display_class_instances(df, file):
    race_counts = df['Race'].value_counts()  # Numără instanțele pentru fiecare clasă
    file.write("Numărul de instanțe pentru fiecare clasă (Race):\n")
    file.write(str(race_counts))
    file.write("\n\n")

def display_distinct_values(df, file):
    for column in df.columns:
        file.write(f"Atrribut: {column}\n")
        file.write("Valori distincte: " + str(df[column].unique()) + "\n")
        file.write("Numărul global de valori:\n")
        file.write(str(df[column].value_counts()) + "\n")
        file.write("\nNumărul de valori pe 'Race':\n")
        file.write(str(df.groupby('Race')[column].value_counts()) + "\n")
        file.write("\n" + "-" * 50 + "\n\n")

def display_correlations(df, file):
    numeric_df = df.select_dtypes(include=['int64', 'float64'])
    
    # Calculează matricea de corelație
    correlations = numeric_df.corr()

    # Verifică dacă 'Race' este în DataFrame-ul numeric
    if 'Race' in correlations.columns:
        # Obține corelația tuturor atributelor cu 'Race'
        race_correlations = correlations['Race'].drop('Race')

        # Sortează atributele în funcție de corelația lor absolută cu 'Race'
        sorted_attributes = race_correlations.abs().sort_values(ascending=False).index
        
        # Creează o matrice de corelație sortată pe baza atributelor sortate
        sorted_correlations = correlations.loc[sorted_attributes, sorted_attributes]
        
        file.write("Matricea de corelație (ordonată după influența asupra 'Race'):\n")
        file.write(str(sorted_correlations))
        file.write("\n\n")
    else:
        file.write("Nu au fost găsite atribute numerice pentru a corela cu 'Race'.\n\n")

with open(output_file, 'w', encoding='utf-8') as file:
    display_class_instances(df, file)
    display_distinct_values(df, file)
    display_correlations(df, file)

print(f"Analiza a fost scrisă în {output_file}")

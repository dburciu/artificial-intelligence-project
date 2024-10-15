import pandas as pd

# Citirea fișierului Excel
df = pd.read_excel("Data cat personality and predation Cordonnier et al.xlsx")

# Verificarea valorilor lipsă
missing_values = df.isnull().sum()
print("Valori lipsă pe coloană:")
print(missing_values)

# Verificarea rândurilor duplicate
duplicate_rows = df[df.duplicated()]
print("\nRânduri duplicate:")
print(duplicate_rows)

# Verificarea valorilor suplimentare
if 'ID' in df.columns:
    invalid_values = df[df['ID'] <= 0]
    print("\nValori ID invalide (negative sau zero):")
    print(invalid_values)

accepted_values = ['A', 'B', 'C']
if 'Category' in df.columns:
    extra_values = df[~df['Category'].isin(accepted_values)]
    print("\nValori suplimentare în coloană 'Category':")
    print(extra_values)

# Salvează erorile într-un fișier de log
with open('error_log.txt', 'w', encoding='utf-8') as f:
    f.write("Valori lipsă pe coloană:\n")
    f.write(str(missing_values) + '\n\n')
    f.write("Rânduri duplicate:\n")
    f.write(str(duplicate_rows) + '\n\n')
    if 'ID' in df.columns:
        f.write("Valori ID invalide (negative sau zero):\n")
        f.write(str(invalid_values) + '\n\n')
    if 'Category' in df.columns:
        f.write("Valori suplimentare în coloană 'Category':\n")
        f.write(str(extra_values) + '\n\n')

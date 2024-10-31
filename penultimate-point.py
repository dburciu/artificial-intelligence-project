import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def verifica_corelatii(file_path):
    # Citirea setului de date
    df = pd.read_excel(file_path)

    # Excluderea coloanei "Plus"
    df = df.drop(columns=['Plus'], errors='ignore')  # Ignoră dacă "Plus" nu există

    # Calcularea matricei de corelație
    correlation_matrix = df.corr()

    # Afișarea matricei de corelație folosind heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True, cbar_kws={"shrink": .8})
    plt.title("Matricea de Corelație (fără 'Plus')")
    plt.show()

    return correlation_matrix

if __name__ == "__main__":
    file_path = 'Data_cat_numerice.xlsx'  # Fișierul cu date numerice
    corelatii = verifica_corelatii(file_path)
    print("Matricea de corelație:\n", corelatii)

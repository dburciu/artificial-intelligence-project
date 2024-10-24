import pandas as pd

def transf_in_nums(file_path, output_path):
    # Citirea setului de date
    df = pd.read_excel(file_path)

    # Coloane non-numerice
    non_numeric_columns = df.select_dtypes(exclude=['number'])

    for column in non_numeric_columns:
        if column != "Plus":
            df[column] = df[column].astype('category').cat.codes  # Transformarea în coduri numerice

    # Salvarea DataFrame-ului într-un fișier Excel
    df.to_excel(output_path, index=False)
    
    return df

if __name__ == "__main__":
    input_file_path = 'Data cat personality and predation Cordonnier et al.xlsx'
    output_file_path = 'Data_cat_numerice.xlsx'  # Numele fișierului de ieșire
    transformed_df = transf_in_nums(input_file_path, output_file_path)
    print(transformed_df)  # Afișarea DataFrame-ului convertit

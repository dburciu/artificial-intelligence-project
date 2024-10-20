import pandas as pd

def transf_in_nums():

    df = pd.read_excel('Data cat personality and predation Cordonnier et al.xlsx')

    # Non-numeric columns
    non_numeric_columns = df.select_dtypes(exclude=['number'])

    for column in non_numeric_columns:
        if (column != "Plus"):
            df[column] = df[column].astype('category').cat.codes


if __name__ == "__main__":
    print(df)

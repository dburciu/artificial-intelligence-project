import pandas as pd

df = pd.read_excel('cat_personality_data.xlsx')

# Non-numeric columns
non_numeric_columns = df.select_dtypes(exclude=['number'])

for column in non_numeric_columns:
    df[column] = df[column].astype('category').cat.codes

print(df)

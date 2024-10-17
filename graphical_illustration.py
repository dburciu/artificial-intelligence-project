import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from deep_translator import GoogleTranslator

data = pd.read_excel('Data cat personality and predation Cordonnier et al.xlsx')


for col in data.columns:
    if col != 'Race' and col != 'Row.names' and col != 'Plus':

        if data[col].dtype == 'object' or data[col].dtype == 'category':
            plt.figure(figsize=(10, 6))
            sns.countplot(data=data, x='Race', hue=col)
            plt.title(f'Countplot: Race vs {GoogleTranslator(source='auto', target='en').translate(col)}')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

        elif pd.api.types.is_numeric_dtype(data[col]):
            plt.figure(figsize=(10, 6))
            sns.boxplot(data=data, x='Race', y=col)
            plt.title(f'Boxplot: Race vs {GoogleTranslator(source='auto', target='en').translate(col)}')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

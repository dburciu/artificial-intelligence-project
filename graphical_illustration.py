import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from deep_translator import GoogleTranslator

data = pd.read_excel('Data cat personality and predation Cordonnier et al.xlsx')

race_dict = {
    "BEN": "Bengal",
    "SBI": "Birman",
    "BRI": "British Shorthair",
    "CHA": "Chartreux",
    "EUR": "European",
    "MCO": "Maine coon",
    "PER": "Persian",
    "RAG": "Ragdoll",
    "SPH": "Sphynx",
    "SAV": "Savannah",  # nu exista mentionata SVA
    "ORI": "Sphynx",
    "TUV": "Turkish angora",
    "Autre": "No Breed/ Other",
    "NSP": "Unkown"
}

data['Race'] = data['Race'].map(race_dict)

for col in data.columns:
    if col != 'Race' and col != 'Row.names' and col != 'Plus':

        if data[col].dtype == 'object' or data[col].dtype == 'category':
            plt.figure(figsize=(10, 6))
            sns.countplot(data=data, x='Race', hue=col)
            plt.title(f"Countplot: Race vs {GoogleTranslator(source='auto', target='en').translate(col)}")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

        elif pd.api.types.is_numeric_dtype(data[col]):
            plt.figure(figsize=(10, 6))
            sns.boxplot(data=data, x='Race', y=col)
            plt.title(f"Boxplot: Race vs {GoogleTranslator(source='auto', target='en').translate(col)}")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

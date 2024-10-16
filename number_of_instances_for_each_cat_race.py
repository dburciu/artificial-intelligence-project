import pandas as pd

data = pd.read_excel('Data cat personality and predation Cordonnier et al.xlsx')

print("Numărul de instanțe pentru fiecare rasă de pisici:")
class_counts = data['Race'].value_counts()
for cat_breed, count in class_counts.items():
    print(f"Rasa '{cat_breed}': {count} instanțe")

import pandas as pd

def unique_val():

    data = pd.read_excel('Data cat personality and predation Cordonnier et al.xlsx')

    # Get a list of all columns to identify class columns
    attributes = data.columns.tolist()

    # Non-numeric columns
    classes = data.select_dtypes(include=['object']).columns.tolist()

    for column in attributes:
        print(f"\nProcessing column: {column}")
    
        unique_values = data[column].value_counts()
    
        print(f"Total unique values in {column}: {len(unique_values)}")
        # print(unique_values)

        for class_column in classes:
            if class_column != column:
                grouped = data.groupby(class_column)[column].value_counts()
                print("---")
                print(grouped)

if __name__ == "__main__":
    print(unique_val());
import csv
import pandas as pd

def read_csv(filepath):
    blanks = 0
    conteo = 0
    data = []
    
    with open(filepath, mode='r') as file:
        csv_reader = csv.reader(file, delimiter=';')

        for row in csv_reader:
            if all(cell.strip() == "" for cell in row):
                blanks += 1
            conteo += 1

            if blanks == 2:
                data.append(row)

        columns = data[3]
        data = data[4:]
        
    df = pd.DataFrame(data, columns=columns)
    df = df.replace(',', '.', regex=True)
        
    return df
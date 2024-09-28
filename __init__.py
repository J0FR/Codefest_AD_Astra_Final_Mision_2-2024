
import csv

def read_csv():
    filepath = "Data/SPG_001.csv"
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

        data = data[4:]
        
                

    print(float[:5])  
    print(conteo)
    return data

read_csv()
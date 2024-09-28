from csv_reader import read_csv
import pandas as pd

def main():

    file_path = input("Escribe el path del archivo: ")
    csv = read_csv(file_path)

    data, columns = csv
    df = pd.DataFrame(data, columns=columns)
    df = df.replace(',', '.', regex=True)
    print(df)
    print(df.iloc[:, -2:])
    for col in df.columns:
    if 'Magnitude [dBm]' in col:
        # Convertir la columna a tipo float
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Crear una nueva columna para la amplitud correspondiente
        new_col_name = col.replace('Magnitude', 'Amplitud')
        df[new_col_name] = 10 ** (df[col] / 20)


if __name__ == "__main__":
    main()
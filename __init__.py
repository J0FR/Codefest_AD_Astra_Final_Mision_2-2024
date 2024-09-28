from csv_reader import read_csv
import pandas as pd

def main():

    file_path = input("Escribe el path del archivo: ")
    csv = read_csv(file_path)

    data, columns = csv
    df = pd.DataFrame(data, columns=columns)
    print(df)


if __name__ == "__main__":
    main()
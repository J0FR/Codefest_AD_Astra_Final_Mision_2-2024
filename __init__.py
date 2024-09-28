from csv_reader import read_csv

def main():

    file_path = input("Escribe el path del archivo: ")
    csv = read_csv(file_path)

if __name__ == "__main__":
    main()
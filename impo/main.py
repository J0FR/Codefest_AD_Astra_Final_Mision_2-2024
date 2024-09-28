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
    df = df.replace(r'^\s*$', 0, regex=True)  # Reemplazar valores vacíos o no válidos con 0
    return df

# Leer el archivo CSV
df = read_csv('./Data/SPG_001.csv')

# Seleccionar solo las columnas de Magnitudes (ignorando la primera columna que es la frecuencia)
magnitude_columns = df.columns[1:]

# Tomar 50 columnas aleatorias de las columnas de magnitud
random_columns = df[magnitude_columns].sample(n=50, axis=1, random_state=42)  # random_state es para reproducibilidad

# Convertir las columnas seleccionadas a tipo float (reemplazar errores con 0 si es necesario)
random_columns = random_columns.apply(pd.to_numeric, errors='coerce').fillna(0)

# Calcular el promedio de magnitudes por fila solo con las 50 columnas aleatorias
df['Average Magnitude [dBm]'] = random_columns.mean(axis=1)

# Mostrar el DataFrame con las columnas seleccionadas y el nuevo promedio
print(df[['Frequency [Hz]', 'Average Magnitude [dBm]']])

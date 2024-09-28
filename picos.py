import pandas as pd
import matplotlib.pyplot as plt
import random

# Función para leer el archivo CSV
def read_csv(filepath):
    blanks = 0
    conteo = 0
    data = []
    
    with open(filepath, mode='r') as file:
        csv_reader = pd.read_csv(file, delimiter=';')

        columns = csv_reader.columns
        data = csv_reader.to_numpy()

    df = pd.DataFrame(data, columns=columns)
    df = df.replace(',', '.', regex=True)
    df = df.apply(pd.to_numeric, errors='coerce')  # Convertir todo a float
    
    return df

# Leer el archivo CSV
df = read_csv('./Data/SPG_001.csv')

# Limpiar nombres de las columnas
df.columns = df.columns.str.strip()

# Verificar las columnas para seleccionar una aleatoria
magnitude_columns = [col for col in df.columns if 'Magnitude [dBm]' in col]

# Seleccionar una columna aleatoria
columna_aleatoria = random.choice(magnitude_columns)

# Graficar la columna seleccionada con Frecuencia en el eje X
plt.figure(figsize=(10, 6))
plt.plot(df['Frequency [Hz]'], df[columna_aleatoria], label=f'Frecuencia vs {columna_aleatoria}')
plt.title(f'Frecuencia vs {columna_aleatoria}')
plt.xlabel('Frecuencia [Hz]')
plt.ylabel(columna_aleatoria)
plt.legend()
plt.grid(True)
plt.show()

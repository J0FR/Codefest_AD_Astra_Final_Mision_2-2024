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

# Calcular el promedio general de todas las filas de 'Average Magnitude [dBm]'
overall_average = df['Average Magnitude [dBm]'].mean()

# Aplicar la condición de dejar a 0 los valores por debajo del promedio general
df['Filtered Average Magnitude [dBm]'] = df['Average Magnitude [dBm]'].apply(lambda x: x if x >= overall_average else 0)

# Mostrar el DataFrame con las columnas seleccionadas, el nuevo promedio y el promedio filtrado
print(df[['Frequency [Hz]', 'Average Magnitude [dBm]', 'Filtered Average Magnitude [dBm]']])

print(df)

max = -9999999
values = []
for index, value in df['Filtered Average Magnitude [dBm]'].items():
    if value > max and value != 0:
        max = value
    if value == 0 and max != -9999999:
        values.append((index, max))
        max = -9999999
print(values)

df['Frequency [Hz]'] = pd.to_numeric(df['Frequency [Hz]'], errors='coerce')
df['Average Magnitude [dBm]'] = pd.to_numeric(df['Average Magnitude [dBm]'], errors='coerce')


one = None
two = None
for index, value in values:
    if (df["Frequency [Hz]"][index] >= 430 and df["Frequency [Hz]"][index] <= 440) and (two is None or df["Frequency [Hz]"][two] < df["Frequency [Hz]"][index]):
        two = index - 1
    elif one is None or df["Frequency [Hz]"][index] > df["Frequency [Hz]"][one]:
        one = index - 1
       
       
import pandas as pd
import matplotlib.pyplot as plt 
datos_one_mag = []
datos_one_frec = []
if one is not None:
    min_one = None
    max_one = None
    one_step = one
    while 0 < one_step:
        one_step -= 1
    min_one = one_step
    while df["Filtered Average Magnitude [dBm]"][one_step] != 0:
        one_step += 1
        datos_one_mag.append(df["Filtered Average Magnitude [dBm]"][one_step])
        datos_one_frec.append(df["Frequency [Hz]"][one_step])
    max_one = one_step
    
datos_two_mag = []
datos_two_frec = []
if two is not None:
    min_two = None
    max_two = None
    two_step = two
    while 0 < two_step:
        two_step -= 1
    min_two = two_step
    while df["Filtered Average Magnitude [dBm]"][two_step] != 0:
        two_step += 1
        datos_two_mag.append(df["Filtered Average Magnitude [dBm]"][two_step])
        datos_two_frec.append(df["Frequency [Hz]"][two_step])
    max_two = two_step
    
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Supongamos que tenemos los datos 'datos_one_mag', 'datos_one_frec', 'datos_two_mag' y 'datos_two_frec'
# de las islas correspondientes al 'one' y 'two' calculados previamente.

# Función para crear un histograma basado en magnitud y frecuencia
def crear_histograma(frecuencia, magnitud, titulo):
    plt.figure(figsize=(10, 6))
    plt.bar(frecuencia, magnitud, width=500000, edgecolor='black')  # La barra se muestra por frecuencia
    plt.title(f'Histograma de {titulo}')
    plt.xlabel('Frecuencia [Hz]')
    plt.ylabel('Magnitud [dBm]')
    plt.show()

# Histograma para la primera isla (one)
if datos_one_mag and datos_one_frec:
    crear_histograma(datos_one_frec, datos_one_mag, "Primera Isla (One)")

# Histograma para la segunda isla (two)
if datos_two_mag and datos_two_frec:
    crear_histograma(datos_two_frec, datos_two_mag, "Segunda Isla (Two)")


import numpy as np

# 1. Frecuencia central: La frecuencia en la cual la señal tiene su mayor amplitud.
def calcular_frecuencia_central(df):
    max_index = df['Filtered Average Magnitude [dBm]'].idxmax()  # Índice de la magnitud máxima
    return df['Frequency [Hz]'][max_index]  # Frecuencia correspondiente

# 2. Ancho de banda (BW): Diferencia entre la frecuencia mínima y máxima dentro del rango de la señal.
def calcular_ancho_de_banda(df):
    freqs_con_magnitud = df[df['Filtered Average Magnitude [dBm]'] != 0]['Frequency [Hz]']
    return freqs_con_magnitud.max() - freqs_con_magnitud.min()

# 3. Amplitud/Potencia: Máxima potencia de la señal (en dBm).
def calcular_amplitud(df):
    return df['Filtered Average Magnitude [dBm]'].max()

# 4. Nivel de ruido: Promedio de las magnitudes que están por debajo de un umbral bajo (considerado como ruido).
def calcular_nivel_ruido(df, umbral_ruido=-100):
    ruido = df[df['Filtered Average Magnitude [dBm]'] < umbral_ruido]['Filtered Average Magnitude [dBm]']
    return ruido.mean() if not ruido.empty else None

# 5. Relación señal-ruido (SNR): La diferencia entre la amplitud máxima y el nivel de ruido.
def calcular_snr(df, umbral_ruido=-100):
    amplitud_max = calcular_amplitud(df)
    nivel_ruido = calcular_nivel_ruido(df, umbral_ruido)
    return amplitud_max - nivel_ruido if nivel_ruido is not None else None

# 6. Picos espectrales: Puntos donde la amplitud es máxima dentro del ancho de banda.
def encontrar_picos(df):
    return df[df['Filtered Average Magnitude [dBm]'] > 0][['Frequency [Hz]', 'Filtered Average Magnitude [dBm]']]

# 7. Frecuencias espurias: Señales indeseadas que están lejos de la señal principal.
def encontrar_frecuencias_espurias(df, umbral=-80):
    espurias = df[df['Filtered Average Magnitude [dBm]'] < umbral]
    return espurias[['Frequency [Hz]', 'Filtered Average Magnitude [dBm]']]

# 8. Drift de frecuencia: Cambios en la frecuencia central de la señal a lo largo del tiempo.
def calcular_drift_frecuencia(frecuencia_inicial, frecuencia_final):
    return frecuencia_final - frecuencia_inicial

# 9. Tiempo de ocupación: Tiempo durante el cual la señal está presente (puedes definir los datos temporales si están disponibles).
def calcular_tiempo_ocupacion(tiempos):
    return tiempos.max() - tiempos.min()

# 10. Crest factor: Relación entre el pico de la señal y su valor RMS (Root Mean Square).
def calcular_crest_factor(df):
    pico = calcular_amplitud(df)
    rms = np.sqrt(np.mean(np.square(df['Filtered Average Magnitude [dBm]'])))
    return pico / rms if rms != 0 else None


# Datos de prueba
data = {
    'Frequency [Hz]': np.linspace(0, 1000000, 100),
    'Filtered Average Magnitude [dBm]': np.random.uniform(-120, 0, 100)
}
df = pd.DataFrame(data)

# Histograma de prueba
datos_one_mag = df['Filtered Average Magnitude [dBm]'][:50]
datos_one_frec = df['Frequency [Hz]'][:50]

datos_two_mag = df['Filtered Average Magnitude [dBm]'][50:]
datos_two_frec = df['Frequency [Hz]'][50:]

# Prueba de creación de histogramas
if datos_one_mag.any() and datos_one_frec.any():
    crear_histograma(datos_one_frec, datos_one_mag, "Primera Isla (One)")

if datos_two_mag.any() and datos_two_frec.any():
    crear_histograma(datos_two_frec, datos_two_mag, "Segunda Isla (Two)")

# 1. Prueba de frecuencia central
frecuencia_central = calcular_frecuencia_central(df)
print("Frecuencia central:", frecuencia_central)

# 2. Prueba de ancho de banda
ancho_banda = calcular_ancho_de_banda(df)
print("Ancho de banda:", ancho_banda)

# 3. Prueba de amplitud
amplitud = calcular_amplitud(df)
print("Amplitud máxima:", amplitud)

# 4. Prueba de nivel de ruido
nivel_ruido = calcular_nivel_ruido(df, umbral_ruido=-100)
print("Nivel de ruido:", nivel_ruido)

# 5. Prueba de relación señal-ruido (SNR)
snr = calcular_snr(df, umbral_ruido=-100)
print("Relación señal-ruido (SNR):", snr)

# 6. Prueba de picos espectrales
picos = encontrar_picos(df)
print("Picos espectrales:\n", picos)

# 7. Prueba de frecuencias espurias
frecuencias_espurias = encontrar_frecuencias_espurias(df, umbral=-80)
print("Frecuencias espurias:\n", frecuencias_espurias)

# 8. Prueba de drift de frecuencia
frecuencia_inicial = 500000
frecuencia_final = 600000
drift = calcular_drift_frecuencia(frecuencia_inicial, frecuencia_final)
print("Drift de frecuencia:", drift)

# 9. Prueba de tiempo de ocupación
tiempos = pd.Series(np.linspace(0, 10, 100))  # Simulando tiempos de 0 a 10 segundos
tiempo_ocupacion = calcular_tiempo_ocupacion(tiempos)
print("Tiempo de ocupación:", tiempo_ocupacion)

# 10. Prueba de crest factor
crest_factor = calcular_crest_factor(df)
print("Crest factor:", crest_factor)
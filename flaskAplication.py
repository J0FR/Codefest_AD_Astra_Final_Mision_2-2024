from flask import Flask, request, redirect, url_for, render_template
import os
import pandas as pd
import csv
import numpy as np
from flask import Flask, request, render_template
import os
import csv
import pandas as pd

from impo import main3

app = Flask(__name__)

# Configuración para la subida de archivos
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No hay archivo en la solicitud.'
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No seleccionaste ningún archivo.'
    
    if file and allowed_file(file.filename):
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)  # Guarda el archivo en el servidor
        
        df = read_csv(file_path)
        results = process_data(df)
        return render_template('results.html', results=results)

    return 'Archivo no permitido. Asegúrate de subir un archivo .csv.'

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

def process_data(df):
    magnitude_columns = df.columns[1:]
    random_columns = df[magnitude_columns].sample(n=50, axis=1, random_state=42)
    random_columns = random_columns.apply(pd.to_numeric, errors='coerce').fillna(0)
    
    df['Average Magnitude [dBm]'] = random_columns.mean(axis=1)
    overall_average = df['Average Magnitude [dBm]'].mean()
    df['Filtered Average Magnitude [dBm]'] = df['Average Magnitude [dBm]'].apply(lambda x: x if x >= overall_average else 0)

    # Obtén los valores y frecuencias
    max = -9999999
    values = []
    for index, value in df['Filtered Average Magnitude [dBm]'].items():
        if value > max and value != 0:
            max = value
        if value == 0 and max != -9999999:
            values.append((index, max))
            max = -9999999

    

    datos_one_mag = df['Filtered Average Magnitude [dBm]'][:50]
    datos_one_frec = df['Frequency [Hz]'][:50]
    datos_two_mag = df['Filtered Average Magnitude [dBm]'][50:]
    datos_two_frec = df['Frequency [Hz]'][50:]

    # Calcular métricas
    frecuencia_central = calcular_frecuencia_central(df)
    ancho_banda = calcular_ancho_de_banda(df)
    amplitud = calcular_amplitud(df)
    nivel_ruido = calcular_nivel_ruido(df, umbral_ruido=-100)
    snr = calcular_snr(df, umbral_ruido=-100)
    picos = encontrar_picos(df)
    frecuencias_espurias = encontrar_frecuencias_espurias(df, umbral=-80)

    # Crear histogramas
    main3.crear_histograma(datos_one_frec, datos_one_mag, "Primera Isla (One)", 'histograma_one.png')
    main3.crear_histograma(datos_two_frec, datos_two_mag, "Segunda Isla (Two)", 'histograma_two.png')

    # Calcular drift y tiempo de ocupación
    frecuencia_inicial = 500000  # Debes definir un valor adecuado
    frecuencia_final = 600000     # Debes definir un valor adecuado
    drift = calcular_drift_frecuencia(frecuencia_inicial, frecuencia_final)

    tiempos = pd.Series(np.linspace(0, 10, 100))  # Simulando tiempos de 0 a 10 segundos
    tiempo_ocupacion = calcular_tiempo_ocupacion(tiempos)

    # Calcular crest factor
    crest_factor = calcular_crest_factor(df)

    return {
        'average_magnitude': df['Average Magnitude [dBm]'].tolist(),
        'filtered_average_magnitude': df['Filtered Average Magnitude [dBm]'].tolist(),
        'frecuencia_central': frecuencia_central,
        'ancho_banda': ancho_banda,
        'amplitud': amplitud,
        'nivel_ruido': nivel_ruido,
        'snr': snr,
        'picos': picos.to_dict(orient='records'),  # Convertir a diccionario
        'frecuencias_espurias': frecuencias_espurias.to_dict(orient='records'),  # Convertir a diccionario
        'drift': drift,
        'tiempo_ocupacion': tiempo_ocupacion,
        'crest_factor': crest_factor,
        'histograma_one': 'histograma_one.png',
        'histograma_two': 'histograma_two.png'
    }

# 1. Frecuencia central
def calcular_frecuencia_central(df):
    max_index = df['Filtered Average Magnitude [dBm]'].idxmax()  # Índice de la magnitud máxima
    return df['Frequency [Hz]'][max_index]  # Frecuencia correspondiente

# 2. Ancho de banda (BW)
def calcular_ancho_de_banda(df):
    freqs_con_magnitud = df[df['Filtered Average Magnitude [dBm]'] != 0]['Frequency [Hz]']
    return freqs_con_magnitud.max() - freqs_con_magnitud.min()

# 3. Amplitud/Potencia
def calcular_amplitud(df):
    return df['Filtered Average Magnitude [dBm]'].max()

# 4. Nivel de ruido
def calcular_nivel_ruido(df, umbral_ruido=-100):
    ruido = df[df['Filtered Average Magnitude [dBm]'] < umbral_ruido]['Filtered Average Magnitude [dBm]']
    return ruido.mean() if not ruido.empty else None

# 5. Relación señal-ruido (SNR)
def calcular_snr(df, umbral_ruido=-100):
    amplitud_max = calcular_amplitud(df)
    nivel_ruido = calcular_nivel_ruido(df, umbral_ruido)
    return amplitud_max - nivel_ruido if nivel_ruido is not None else None

# 6. Picos espectrales
def encontrar_picos(df):
    return df[df['Filtered Average Magnitude [dBm]'] > 0][['Frequency [Hz]', 'Filtered Average Magnitude [dBm]']]

# 7. Frecuencias espurias
def encontrar_frecuencias_espurias(df, umbral=-80):
    espurias = df[df['Filtered Average Magnitude [dBm]'] < umbral]
    return espurias[['Frequency [Hz]', 'Filtered Average Magnitude [dBm]']]

# 8. Drift de frecuencia
def calcular_drift_frecuencia(frecuencia_inicial, frecuencia_final):
    return frecuencia_final - frecuencia_inicial

# 9. Tiempo de ocupación
def calcular_tiempo_ocupacion(tiempos):
    return tiempos.max() - tiempos.min()

# 10. Crest factor
def calcular_crest_factor(df):
    pico = calcular_amplitud(df)
    rms = np.sqrt(np.mean(np.square(df['Filtered Average Magnitude [dBm]'])))
    return pico / rms if rms != 0 else None

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)  # Crea el directorio de subidas si no existe
    app.run(debug=True)


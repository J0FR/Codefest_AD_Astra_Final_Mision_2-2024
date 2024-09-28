import csv
import numpy as np
import matplotlib.pyplot as plt

class AdaptiveNoiseCanceller:
    def __init__(self, signal, noise, mu=0.01, filter_order=10):
        """
        Inicializa el cancelador adaptativo de ruido.
        :param signal: Señal original contaminada con interferencia.
        :param noise: Señal de ruido conocida (entrada de referencia del inhibidor).
        :param mu: Tasa de aprendizaje para el filtro LMS.
        :param filter_order: Orden del filtro adaptativo (número de coeficientes).
        """
        self.signal = signal
        self.noise = noise
        self.mu = mu
        self.filter_order = filter_order
        self.weights = np.zeros(filter_order)  # Coeficientes iniciales del filtro adaptativo

    def lms_filter(self):
        """
        Aplica el filtro LMS para cancelar la interferencia en la señal.
        :return: Señal procesada (señal con la interferencia cancelada).
        """
        N = len(self.signal)
        output = np.zeros(N)  # Señal filtrada
        error = np.zeros(N)   # Error entre la señal deseada y la estimación

        for n in range(self.filter_order, N):
            # Segmento de la señal de ruido de acuerdo con el orden del filtro
            x_noise = self.noise[n:n-self.filter_order:-1]
            
            # Estimación de la interferencia usando los pesos actuales del filtro
            estimated_noise = np.dot(self.weights, x_noise)
            
            # Error entre la señal deseada y la estimación del ruido
            error[n] = self.signal[n] - estimated_noise
            
            # Actualización de los pesos del filtro (algoritmo LMS)
            self.weights += 2 * self.mu * error[n] * x_noise

            # Señal de salida filtrada
            output[n] = error[n]

        return output

def generate_signals():
    # Frecuencia de la señal y ruido
    fs = 1000  # Frecuencia de muestreo
    t = np.linspace(0, 1, fs)  # Intervalo de tiempo de 1 segundo

    # Señal original (señal sinusoidal entre 400 y 450 MHz)
    signal = np.sin(2 * np.pi * 430 * t)

    # Interferencia (inhibidor) que afecta desde 30 MHz hasta 6 GHz
    noise = np.sin(2 * np.pi * 50 * t) + 0.5 * np.sin(2 * np.pi * 1500 * t)

    # Señal mezclada con interferencia
    noisy_signal = signal + noise

    return signal, noise, noisy_signal, t

def save_to_csv(filepath, time, signal, noisy_signal, filtered_signal):
    """
    Guarda las señales generadas en un archivo CSV.
    :param filepath: Ruta donde se guarda el CSV.
    :param time: Array de tiempo.
    :param signal: Señal original.
    :param noisy_signal: Señal con interferencia.
    :param filtered_signal: Señal filtrada.
    """
    with open(filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time (s)', 'Original Signal', 'Noisy Signal', 'Filtered Signal'])
        for i in range(len(time)):
            writer.writerow([time[i], signal[i], noisy_signal[i], filtered_signal[i]])

def plot_signals(time, signal, noisy_signal, filtered_signal):
    """
    Plotea las señales en el dominio del tiempo.
    """
    plt.figure(figsize=(10, 6))

    # Señal original
    plt.subplot(3, 1, 1)
    plt.plot(time, signal)
    plt.title('Señal Original')

    # Señal con ruido
    plt.subplot(3, 1, 2)
    plt.plot(time, noisy_signal)
    plt.title('Señal con Interferencia')

    # Señal después de la cancelación de interferencia
    plt.subplot(3, 1, 3)
    plt.plot(time, filtered_signal)
    plt.title('Señal después de Cancelación de Interferencia')

    plt.tight_layout()
    plt.show()

def plot_fourier(signal, fs, title):
    """
    Aplica la Transformada de Fourier a una señal y plotea su espectro de frecuencias.
    :param signal: Señal en el dominio del tiempo.
    :param fs: Frecuencia de muestreo.
    :param title: Título del gráfico.
    """
    N = len(signal)
    freqs = np.fft.fftfreq(N, 1/fs)
    fft_signal = np.fft.fft(signal)
    
    # Graficar solo las frecuencias positivas
    plt.figure(figsize=(8, 4))
    plt.plot(freqs[:N//2], np.abs(fft_signal[:N//2]))  # Magnitud del espectro
    plt.title(f"Espectro de Frecuencias - {title}")
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("Magnitud")
    plt.grid(True)
    plt.show()

# Ejemplo de uso
if __name__ == "__main__":
    # Generar señales para la prueba
    signal, noise, noisy_signal, time = generate_signals()
    fs = 1000  # Frecuencia de muestreo

    # Crear una instancia del cancelador adaptativo
    canceller = AdaptiveNoiseCanceller(noisy_signal, noise)

    # Aplicar el filtro LMS
    filtered_signal = canceller.lms_filter()

    # Guardar las señales en un archivo CSV
    save_to_csv('data/processed_signal_data.csv', time, signal, noisy_signal, filtered_signal)

    # Ploteo de las señales en el dominio del tiempo
    plot_signals(time, signal, noisy_signal, filtered_signal)

    # Aplicar y plotear la Transformada de Fourier para cada señal
    plot_fourier(signal, fs, "Señal Original")
    plot_fourier(noisy_signal, fs, "Señal con Interferencia")
    plot_fourier(filtered_signal, fs, "Señal Filtrada")


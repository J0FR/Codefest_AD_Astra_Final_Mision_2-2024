import numpy as np
 
def generate_signals():
    # Frecuencia de la señal y ruido
    fs = 1000  # Frecuencia de muestreo
    t = np.linspace(0, 1, fs)  

 
    signal = np.sin(2 * np.pi * 430 * t)

  
    noise = np.sin(2 * np.pi * 50 * t) + 0.5 * np.sin(2 * np.pi * 1500 * t)

   
    noisy_signal = signal + noise

    return signal, noise, noisy_signal

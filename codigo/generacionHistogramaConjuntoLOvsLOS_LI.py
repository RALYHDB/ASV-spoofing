import os
import torch
import torchaudio
import numpy as np
import matplotlib.pyplot as plt
from speechbrain.inference import EncoderClassifier
from sklearn.metrics.pairwise import cosine_similarity

def calculate_eer(fpr, fnr, thresholds):
    """
    Calcular el EER (Equal Error Rate) y el umbral correspondiente.

    Parámetros:
    - fpr (list): Lista de tasas de falsos positivos.
    - fnr (list): Lista de tasas de falsos negativos.
    - thresholds (list): Lista de umbrales correspondientes a las tasas FPR y FNR.

    Retorna:
    - eer (float): Equal Error Rate.
    - eer_threshold (float): Umbral correspondiente al EER.
    """
    differences = np.abs(np.array(fpr) - np.array(fnr))
    min_index = np.argmin(differences)
    eer = (fpr[min_index] + fnr[min_index]) / 2
    eer_threshold = thresholds[min_index]
    return eer, eer_threshold

def plot_fpr_fnr(target_scores, impostor_scores, model_name, output_dir):
    """
    Generar y guardar la gráfica de FPR y FNR en función del umbral, incluyendo el EER.
    
    Parámetros:
    - target_scores (numpy.ndarray): Puntuaciones de los locutores objetivos.
    - impostor_scores (numpy.ndarray): Puntuaciones de los locutores impostores.
    - model_name (str): Nombre del modelo ASV para el título de la gráfica.
    - output_dir (str): Directorio donde se guardará la gráfica generada.
    """
    thresholds = np.linspace(min(min(target_scores), min(impostor_scores)), max(max(target_scores), max(impostor_scores)), 1000)
    fpr = []
    fnr = []

    for threshold in thresholds:
        fpr.append(np.mean(impostor_scores >= threshold))
        fnr.append(np.mean(target_scores < threshold))

    # Calcular el EER y el umbral correspondiente
    eer, eer_threshold = calculate_eer(fpr, fnr, thresholds)

    plt.figure(figsize=(10, 6))

    plt.plot(thresholds, fpr, label='FPR (False Positive Rate)', color='red')
    plt.plot(thresholds, fnr, label='FNR (False Negative Rate)', color='blue')
    plt.axvline(eer_threshold, color='green', linestyle='--', label=f'EER = {eer:.2f} en Umbral {eer_threshold:.2f}')

    plt.title(f'FPR y FNR en función del umbral para {model_name}')
    plt.xlabel('Umbral')
    plt.ylabel('Tasa')
    plt.legend()
    plt.grid(True)

    output_path = os.path.join(output_dir, f"fpr_fnr_LOS_LibriTTS_agregado_{model_name}.png")
    plt.savefig(output_path, dpi=300)  # Guardar con dpi=300 para alta calidad
    plt.close()
    print(f"Gráfica de FPR y FNR guardada en: {output_path}")

def cargar_y_combinar_puntuaciones(paths):
    puntuaciones = []
    for path in paths:
        puntuaciones.append(np.load(path))
        print(f"Puntuaciones cargadas desde {path}")
    return np.concatenate(puntuaciones)


# Función para crear el histograma conjunto
def crear_histograma_conjunto():
    # Rutas de los archivos de puntuaciones guardadas
        #######################################################################################################################################################
# Rutas de los archivos de puntuaciones guardadas
    puntuaciones_objetivos_paths = [
        "puntuaciones/puntuaciones_LOs_femeninos_resnet.npy",
        "puntuaciones/puntuaciones_LOs_masculinos_resnet.npy"
    ]
    puntuaciones_synthesized_paths = [
        "puntuaciones/puntuaciones_LOCs_femeninos_LibriTTS_resnet.npy",
        "puntuaciones/puntuaciones_LOCs_masculinos_LibriTTS_resnet.npy"
    ]

    # Cargar y combinar las puntuaciones de los locutores objetivos
    puntuaciones_objetivos = cargar_y_combinar_puntuaciones(puntuaciones_objetivos_paths)

    # Cargar y combinar las puntuaciones de los locutores sintetizados
    puntuaciones_synthesized = cargar_y_combinar_puntuaciones(puntuaciones_synthesized_paths)


    # Cargar las puntuaciones de los locutores objetivos
   # puntuaciones_objetivos = np.load(puntuaciones_objetivos_path)
    #print(f"Puntuaciones de locutores objetivos cargadas desde {puntuaciones_objetivos_path}")

    # Cargar las puntuaciones de los locutores sintetizados
    #puntuaciones_synthesized = np.load(puntuaciones_synthesized_path)
    #print(f"Puntuaciones de locutores sintetizados cargadas desde {puntuaciones_synthesized_path}")
    #######################################################################################################################################################
    plot_fpr_fnr(puntuaciones_objetivos, puntuaciones_synthesized, "resnet", 'F:/ASV_SpeechBrain/speechbrain/histogramas')
    # Crear un histograma conjunto de las puntuaciones
    plt.figure(figsize=(10, 6))

    # Histograma para las puntuaciones de los locutores objetivos
    plt.hist(puntuaciones_objetivos, bins=30, density=True, histtype='step', linewidth=1.5, color='b', label='Locutor Objetivo')

    # Histograma para las puntuaciones de los locutores sintetizados
    plt.hist(puntuaciones_synthesized, bins=30, density=True, histtype='step', linewidth=1.5, color='r', label='Locutor Objetivo Sintetizado')

    # Configuración del gráfico
    #######################################################################################################################################################
    plt.title('Histograma de puntuaciones (LO vs LOS).resnet')
    plt.xlabel('Puntuación')
    plt.ylabel('Densidad de Frecuencia')
    plt.legend()
    plt.grid(True)

    # Guardar el histograma en la carpeta de histogramas
    histogramas_dir = 'F:/ASV_SpeechBrain/speechbrain/histogramas'
    os.makedirs(histogramas_dir, exist_ok=True)
    #######################################################################################################################################################
    histograma_path = os.path.join(histogramas_dir, 'histograma_conjunto_LOS_LibriTTS_agregado_resnet.png')
    plt.savefig(histograma_path, dpi=300, bbox_inches='tight')
    print(f"Histograma guardado en {histograma_path}")

    # Mostrar el histograma
    plt.show()

# Llamar a la función para crear y mostrar el histograma conjunto
crear_histograma_conjunto()

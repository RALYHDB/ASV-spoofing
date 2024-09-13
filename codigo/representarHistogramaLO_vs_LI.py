import os
import numpy as np
import matplotlib.pyplot as plt

def load_scores(output_dir, speaker_ids, model_short):
    """
    Cargar y concatenar las puntuaciones de similitud coseno para los locutores especificados y el modelo ASV.
    
    Parámetros:
    - output_dir (str): Directorio donde se guardaron las puntuaciones.
    - speaker_ids (list): Lista de IDs de locutores.
    - model_short (str): Nombre corto del modelo ASV.

    Retorna:
    - scores (numpy.ndarray): Puntuaciones concatenadas para todos los locutores.
    """
    scores = []
    for speaker_id in speaker_ids:
        score_file = os.path.join(output_dir, f"puntuaciones_LO_{speaker_id}_{model_short}.npy")
        if os.path.exists(score_file):
            speaker_scores = np.load(score_file)
            scores.append(speaker_scores)
        else:
            print(f"Archivo no encontrado: {score_file}")
    
    if scores:
        return np.concatenate(scores)
    else:
        return np.array([])

def load_impostor_scores(output_dir, model_short):
    """
    Cargar las puntuaciones de similitud coseno para los locutores impostores y el modelo ASV.
    
    Parámetros:
    - output_dir (str): Directorio donde se guardaron las puntuaciones.
    - model_short (str): Nombre corto del modelo ASV.

    Retorna:
    - scores (numpy.ndarray): Puntuaciones para los locutores impostores.
    """
    score_file = os.path.join(output_dir, f"puntuaciones_impostores_femeninos_y_masculinos_{model_short}.npy")
    if os.path.exists(score_file):
        return np.load(score_file)
    else:
        print(f"Archivo no encontrado: {score_file}")
        return np.array([])

def plot_histogram(target_scores, impostor_scores, model_name, output_dir):
    """
    Generar y guardar el histograma de puntuaciones en forma de escalones para locutores objetivos e impostores.
    
    Parámetros:
    - target_scores (numpy.ndarray): Puntuaciones de los locutores objetivos a representar en el histograma.
    - impostor_scores (numpy.ndarray): Puntuaciones de los locutores impostores a representar en el histograma.
    - model_name (str): Nombre del modelo ASV para el título del histograma.
    - output_dir (str): Directorio donde se guardará la gráfica generada.
    """
    # Calcular las frecuencias y los bins para locutores objetivos
    target_frequencies, target_bins = np.histogram(target_scores, bins=50, density=True)
    # Calcular las frecuencias y los bins para locutores impostores
    impostor_frequencies, impostor_bins = np.histogram(impostor_scores, bins=50, density=True)

    # Crear la figura del histograma en forma de escalones
    plt.figure(figsize=(10, 6))

    # Graficar locutores objetivos
    plt.step(target_bins[:-1], target_frequencies, where='mid', color='blue', alpha=0.75, label='Locutores Objetivos')
    plt.fill_between(target_bins[:-1], target_frequencies, step='mid', alpha=0.2, color='blue')

    # Graficar locutores impostores
    plt.step(impostor_bins[:-1], impostor_frequencies, where='mid', color='red', alpha=0.75, label='Locutores Impostores')
    plt.fill_between(impostor_bins[:-1], impostor_frequencies, step='mid', alpha=0.2, color='red')

    # Título y etiquetas del histograma
    plt.title(f'Histograma de Puntuaciones de Similitud Coseno para {model_name}')
    plt.xlabel('Puntuación de Similitud Coseno')
    plt.ylabel('Densidad de Frecuencia')
    plt.legend()
    plt.grid(True)

    # Guardar la figura en alta calidad
    output_path = os.path.join(output_dir, f"histograma_FM_{model_name}.png")
    plt.savefig(output_path, dpi=300)  # Guardar con dpi=300 para alta calidad
    plt.close()
    print(f"Gráfica guardada en: {output_path}")

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

    output_path = os.path.join(output_dir, f"fpr_fnr_FM_{model_name}.png")
    plt.savefig(output_path, dpi=300)  # Guardar con dpi=300 para alta calidad
    plt.close()
    print(f"Gráfica de FPR y FNR guardada en: {output_path}")

if __name__ == "__main__":
    output_dir = "puntuaciones"
    save_dir = "graficas"
    os.makedirs(save_dir, exist_ok=True)
    
    #speaker_ids = [5181, 5198, 5328, 978, 3962, 3433, 6539, 2309, 4442, 7423]
    speaker_ids = [2834, 614, 585, 483, 5949, 215, 6127, 1384, 3867, 4779,5181, 5198, 5328, 978, 3962, 3433, 6539, 2309, 4442, 7423]
    models = [
        ("xvector", "XVector"),
        ("ecapa", "ECAPA-TDNN"),
        ("resnet", "ResNet")
    ]
    
    for model_short, model_name in models:
        target_scores = load_scores(output_dir, speaker_ids, model_short)
        impostor_scores = load_impostor_scores(output_dir, model_short)
        
        if target_scores.size > 0 or impostor_scores.size > 0:
            plot_histogram(target_scores, impostor_scores, model_name, save_dir)
            plot_fpr_fnr(target_scores, impostor_scores, model_name, save_dir)
        else:
            print(f"No se encontraron puntuaciones para el modelo {model_name}")

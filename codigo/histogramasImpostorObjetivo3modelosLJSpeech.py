import numpy as np
import os
import matplotlib.pyplot as plt

def plot_histogram_continuous(impostor_scores, real_scores, model_name):
    plt.figure(figsize=(8, 6))

    # Calcular histograma continuo para locutores impostores
    impostor_density, impostor_bins, _ = plt.hist(impostor_scores, bins=100, density=True, color='r', alpha=0.5, label='Impostores', histtype='step')

    # Calcular histograma continuo para locutores reales
    real_density, real_bins, _ = plt.hist(real_scores, bins=100, density=True, color='b', alpha=0.5, label='objetivo', histtype='step')

    plt.title(f'Puntuaciones para {model_name}')
    plt.xlabel('Puntuación')
    plt.ylabel('Densidad')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'densidad_puntuaciones_continua_{model_name.lower()}.png')
    plt.show()

def plot_combined_histogram_continuous(impostor_scores, real_scores, model_names):
    plt.figure(figsize=(12, 8))

    colors = ['r', 'g', 'b', 'm', 'c', 'y']
    line_styles = ['-', '--', '-.', ':']

    for i, (model_name, impostor_score, real_score) in enumerate(zip(model_names, impostor_scores, real_scores)):
        # Flatten arrays if necessary
        if impostor_score.ndim > 1:
            impostor_score = impostor_score.flatten()
        if real_score.ndim > 1:
            real_score = real_score.flatten()

        # Calculate combined histogram for impostor scores
        impostor_density, impostor_bins = np.histogram(impostor_score, bins=100, density=True)
        impostor_bins = (impostor_bins[:-1] + impostor_bins[1:]) / 2  # Use bin centers as x values
        color = colors[i % len(colors)]
        plt.plot(impostor_bins, impostor_density, color=color, alpha=0.8, linestyle='-', label=f'Impostores ({model_name})')

        # Calculate combined histogram for real scores
        real_density, real_bins = np.histogram(real_score, bins=100, density=True)
        real_bins = (real_bins[:-1] + real_bins[1:]) / 2  # Use bin centers as x values
        color = colors[(i + 1) % len(colors)]  # Use a different color for real scores
        plt.plot(real_bins, real_density, color=color, alpha=0.8, linestyle='--', label=f'objetivo ({model_name})')

    plt.title('Puntuaciones para Locutor Impostor y Locutor Objetivo')
    plt.xlabel('Puntuación')
    plt.ylabel('Densidad')
    plt.legend()
    plt.grid(True)
    plt.savefig('densidad_puntuaciones_continua_modelos_combinados.png')
    plt.show()

# Cargar puntuaciones para cada modelo
models = ["ResNet", "eCapa", "xvector"]
impostor_scores = []
real_scores = []

for model_name in models:
    impostor_score_file = f"puntuaciones_impostores_Voxceleb_{model_name.lower()}.npy"
    impostor_score_path = os.path.abspath(impostor_score_file)
    if not os.path.exists(impostor_score_path):
        raise FileNotFoundError(f'El archivo {impostor_score_file} no existe.')
    impostor_scores.append(np.load(impostor_score_path))

    real_score_file = f"PuntuacionesClonacionYreal/puntuaciones_reales_{model_name.lower()}.npy"
    real_score_path = os.path.abspath(real_score_file)
    if not os.path.exists(real_score_path):
        raise FileNotFoundError(f'El archivo {real_score_file} no existe.')
    real_scores.append(np.load(real_score_path))

# Graficar histogramas continuos por separado para cada modelo
for model_name, impostor_score, real_score in zip(models, impostor_scores, real_scores):
    plot_histogram_continuous(impostor_score, real_score, model_name)

# Graficar histogramas continuos combinados para todos los modelos
plot_combined_histogram_continuous(impostor_scores, real_scores, models)

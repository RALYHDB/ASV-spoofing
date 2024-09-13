import os
import torch
import torchaudio
import numpy as np
from speechbrain.inference import EncoderClassifier
from sklearn.metrics.pairwise import cosine_similarity

def calculate_cosine_scores(audio_dir, start_idx, num_files, prototype_path, output_dir, model_name, model_short):
    """
    Calcula las puntuaciones de similitud coseno entre los embeddings de los archivos de audio del locutor objetivo
    y el embedding prototipo, y guarda las puntuaciones en un archivo .npy.

    Parámetros:
    - audio_dir (str): Directorio que contiene los archivos de audio.
    - start_idx (int): Índice de inicio para los archivos de audio a procesar.
    - num_files (int): Número máximo de archivos a procesar.
    - prototype_path (str): Ruta del archivo donde se encuentra el embedding prototipo.
    - output_dir (str): Directorio donde se guardarán las puntuaciones.
    - model_name (str): Nombre del modelo ASV a usar.
    - model_short (str): Nombre corto del modelo para los archivos de salida.

    Retorna:
    - cosine_scores (numpy.ndarray): Puntuaciones de similitud coseno calculadas.
    """
    
    # Inicializar el clasificador con el modelo especificado
    classifier = EncoderClassifier.from_hparams(source=model_name)
    print(f"Clasificador {model_name} inicializado correctamente")
    
    # Cargar el embedding prototipo desde el archivo
    embedding_prototipo = np.load(prototype_path)
    print(f"Embedding prototipo cargado desde {prototype_path}")

    # Obtener la lista de archivos de audio de los locutores objetivo
    audio_files = [os.path.join(audio_dir, f) for f in os.listdir(audio_dir) if f.endswith('.wav')]
    
    # Limitar a los archivos desde 'start_idx' hasta 'start_idx + num_files'
    audio_files_to_process = audio_files[start_idx:start_idx + num_files]
    
    # Lista para almacenar los embeddings de los locutores objetivo
    embeddings = []
    
    # Iterar sobre los archivos de audio y calcular los embeddings
    for audio_file in audio_files_to_process:
        try:
            signal, fs = torchaudio.load(audio_file)
            embedding = classifier.encode_batch(signal)
            embeddings.append(embedding.squeeze().detach().numpy())  # Convertir a numpy y eliminar dimensiones innecesarias
        except Exception as e:
            print(f"Error al procesar {audio_file}: {str(e)}")
    
    # Convertir la lista de embeddings a un array de NumPy
    embeddings_np = np.array(embeddings)
    
    # Asegurarse de que los embeddings sean 2D
    embeddings_np = embeddings_np.reshape(embeddings_np.shape[0], -1)
    
    # Calcular la distancia coseno entre el embedding prototipo y cada uno de los nuevos embeddings
    cosine_scores = cosine_similarity(embedding_prototipo, embeddings_np)
    
    # Aplanar las puntuaciones de comparación
    cosine_scores = cosine_scores.flatten()

    # Guardar las puntuaciones en un archivo .npy
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        ##################################################################################################################################################
    output_file_path = os.path.join(output_dir, f"puntuaciones_LOS_LibriTTS_5181{model_short}.npy")
    np.save(output_file_path, cosine_scores)
    print(f"Puntuaciones de similitud coseno guardadas en {output_file_path}")

    return cosine_scores

if __name__ == "__main__":
            ##################################################################################################################################################
    audio_dir = 'F:\ASV_SpeechBrain\speechbrain\clonacion_LibriTTS\clonacion_M_5181'
    #audio_dir = 'F:\ASV_SpeechBrain\speechbrain\LJSpeech'
    start_idx = 0
    num_files = 100 
    output_dir = "puntuaciones"
    
    models = [
        ("speechbrain/spkrec-ecapa-voxceleb", "ecapa"),
        ("speechbrain/spkrec-xvect-voxceleb", "xvector"),
        ("speechbrain/spkrec-resnet-voxceleb", "resnet")
    ]
    
    for model_name, model_short in models:
                ##################################################################################################################################################
        prototype_path = f"prototipos de embeddings/embedding_prototipo_M_5181_{model_short}.npy"
        cosine_scores = calculate_cosine_scores(audio_dir, start_idx, num_files, prototype_path, output_dir, model_name, model_short)
        print(f"Puntuaciones de similitud coseno calculadas para {model_name}: {cosine_scores}")

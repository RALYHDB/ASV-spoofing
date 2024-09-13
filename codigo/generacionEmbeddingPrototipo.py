import os
import torch
import torchaudio
import numpy as np
from speechbrain.inference import EncoderClassifier

def calculate_prototype_embedding(audio_dir, num_files, save_dir, save_filename, model_name):
    """
    Calcula el embedding prototipo de un conjunto de archivos de audio y lo guarda en un archivo.
    
    Parámetros:
    - audio_dir (str): Directorio que contiene los archivos de audio.
    - num_files (int): Número máximo de archivos a procesar.
    - save_dir (str): Directorio donde se guardará el embedding prototipo.
    - save_filename (str): Nombre del archivo donde se guardará el embedding prototipo.
    - model_name (str): Nombre del modelo ASV a usar.
    
    Retorna:
    - embedding_prototipo (numpy.ndarray): El embedding prototipo calculado.
    """
    
    # Inicializar el clasificador con el modelo especificado
    classifier = EncoderClassifier.from_hparams(source=model_name)
    print(f"Clasificador {model_name} inicializado correctamente")
    
    # Obtener la lista de archivos de audio de los locutores objetivo
    audio_files = [os.path.join(audio_dir, f) for f in os.listdir(audio_dir) if f.endswith('.wav')]
    
    # Limitar a los primeros 'num_files' archivos (o menos si hay menos de 'num_files')
    audio_files = audio_files[:num_files]
    
    # Lista para almacenar los embeddings de los locutores objetivo
    embeddings = []
    
    # Iterar sobre los archivos de audio y calcular los embeddings
    for audio_file in audio_files:
        try:
            signal, fs = torchaudio.load(audio_file)
            embedding = classifier.encode_batch(signal)
            embeddings.append(embedding.squeeze().detach().numpy())  # Convertir a numpy y eliminar dimensiones innecesarias
        except Exception as e:
            print(f"Error al procesar {audio_file}: {str(e)}")
    
    # Convertir la lista de embeddings a un array de NumPy y luego a un tensor de PyTorch
    embeddings_np = np.array(embeddings)
    embeddings_tensor = torch.tensor(embeddings_np)
    
    # Calcular la media de los embeddings para obtener el embedding prototipo
    embedding_prototipo = torch.mean(embeddings_tensor, dim=0).numpy()
    
    # Asegurarse de que embedding_prototipo sea 2D
    embedding_prototipo = embedding_prototipo.reshape(1, -1)
    
    # Crear el directorio de guardado si no existe
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # Guardar el embedding prototipo en un archivo
    save_path = os.path.join(save_dir, save_filename)
    np.save(save_path, embedding_prototipo)
    print(f"Embedding prototipo guardado en {save_path}")
    
    return embedding_prototipo

if __name__ == "__main__":
##################################################################################################################################################
    #audio_dir = 'F:/ASV_SpeechBrain/speechbrain/LibriTTS/train-other-500/4779/4779_audios'
    audio_dir ='F:\ASV_SpeechBrain\speechbrain\LJSpeech'
    num_files = 100
    save_dir = "prototipos de embeddings"
    
    models = [
        ("speechbrain/spkrec-ecapa-voxceleb", "ecapa"),
        ("speechbrain/spkrec-xvect-voxceleb", "xvector"),
        ("speechbrain/spkrec-resnet-voxceleb", "resnet")
    ]
    
    for model_name, model_short in models:
##################################################################################################################################################
        save_filename = f"embedding_prototipo_LJSpeech_100sentencias_{model_short}.npy"
        embedding_prototipo = calculate_prototype_embedding(audio_dir, num_files, save_dir, save_filename, model_name)
        print(f"Embedding prototipo calculado para {model_name}: {embedding_prototipo}")

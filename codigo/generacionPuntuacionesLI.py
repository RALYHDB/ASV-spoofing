import os
import torch
import torchaudio
import numpy as np
from speechbrain.inference import EncoderClassifier
from sklearn.metrics.pairwise import cosine_similarity

def calculate_embeddings(audio_dir, num_files):
    """
    Cargar y calcular los embeddings de los archivos de audio.
    
    Parámetros:
    - audio_dir (str): Directorio que contiene los archivos de audio.
    - num_files (int): Número máximo de archivos a procesar.
    
    Retorna:
    - embeddings (list): Lista de embeddings calculados.
    """
    ##################################################################################################################################
    classifier = EncoderClassifier.from_hparams(source="speechbrain/spkrec-resnet-voxceleb")
    audio_files = [os.path.join(root, file)
                   for root, _, files in os.walk(audio_dir)
                   for file in files if file.endswith('.wav')]

    # Limitar a los primeros 'num_files' archivos
    audio_files = audio_files[:num_files]

    embeddings = []
    for audio_file in audio_files:
        try:
            signal, fs = torchaudio.load(audio_file)
            embedding = classifier.encode_batch(signal)
            embeddings.append(embedding.squeeze().detach().numpy())  # Convertir a numpy y eliminar dimensiones innecesarias
        except Exception as e:
            print(f"Error al procesar {audio_file}: {str(e)}")
    return embeddings

def load_prototype_embeddings(prototype_dir, speaker_ids):
    """
    Cargar los embeddings prototipo.
    
    Parámetros:
    - prototype_dir (str): Directorio que contiene los embeddings prototipo.
    - speaker_ids (list): Lista de IDs de locutores.
    
    Retorna:
    - prototype_embeddings (list): Lista de embeddings prototipo cargados.
    """
    # Lista de IDs que pertenecen al conjunto de archivos 'embedding_prototipo_F_{speaker_id}_xvector.npy'
    ids_f = [2834, 614, 585, 483, 5949, 215, 6127, 1384, 3867, 4779]
    
    prototype_embeddings = []
    for speaker_id in speaker_ids:
        if speaker_id in ids_f:
     ##################################################################################################################################           
            prototype_path = os.path.join(prototype_dir, f"embedding_prototipo_F_{speaker_id}_resnet.npy")
        else:
            prototype_path = os.path.join(prototype_dir, f"embedding_prototipo_M_{speaker_id}_resnet.npy")
        
        if os.path.exists(prototype_path):
            prototype_embedding = np.load(prototype_path)
            prototype_embeddings.append(prototype_embedding)
        else:
            print(f"Archivo no encontrado: {prototype_path}")
    
    return prototype_embeddings
def compare_embeddings_with_prototypes(embeddings, prototype_embeddings):
    """
    Comparar los embeddings con los embeddings prototipo usando la similitud coseno.
    
    Parámetros:
    - embeddings (list): Lista de embeddings a comparar.
    - prototype_embeddings (list): Lista de embeddings prototipo.
    
    Retorna:
    - cosine_scores (numpy.ndarray): Puntuaciones de similitud coseno.
    """
    cosine_scores = []
    for embedding in embeddings:
        for prototype_embedding in prototype_embeddings:
            score = cosine_similarity(embedding.reshape(1, -1), prototype_embedding.reshape(1, -1))
            cosine_scores.append(score.item())
    return np.array(cosine_scores)

def main():
    impostor_ids_masculinos = ['id00043', 'id00149', 'id00332', 'id00385', 'id00650', 'id00673', 'id00680', 'id00755', 'id00806', 'id00829','id00015', 'id00029', 'id00060', 'id00062', 'id00168', 'id00184', 'id00185', 'id00191', 'id00255','id00258']
    general_dir = 'F:/ASV_SpeechBrain/speechbrain/vox2_aac/voxceleb2/wav'
    num_files = 500
    target_speaker_ids = [2834, 614, 585, 483, 5949, 215, 6127, 1384, 3867, 4779,5181, 5198, 5328, 978, 3962, 3433, 6539, 2309, 4442, 7423]
    prototype_dir = 'prototipos de embeddings'
    
    # Cargar embeddings prototipo
    prototype_embeddings = load_prototype_embeddings(prototype_dir, target_speaker_ids)
    
    all_cosine_scores = []
    for impostor_id in impostor_ids_masculinos:
        audio_dir = os.path.join(general_dir, impostor_id)
        
        # Calcular embeddings para los archivos de audio
        embeddings = calculate_embeddings(audio_dir, num_files)
        
        # Comparar embeddings con los embeddings prototipo
        cosine_scores = compare_embeddings_with_prototypes(embeddings, prototype_embeddings)
        
        all_cosine_scores.extend(cosine_scores)
        #print(all_cosine_scores)
    
    # Guardar las puntuaciones de similitud coseno
    output_dir = "puntuaciones"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    ########################################################################################################################################
    output_file_path = os.path.join(output_dir, "puntuaciones_impostores_femeninos_y_masculinos_resnet.npy")
    np.save(output_file_path, np.array(all_cosine_scores))
    print(f"Puntuaciones de similitud coseno guardadas en {output_file_path}")

if __name__ == "__main__":
    main()

import os
import random
import torchaudio
from speechbrain.inference.TTS import MSTacotron2
from speechbrain.inference.vocoders import HIFIGAN
import nltk
from nltk.corpus import brown

def generate_long_text(num_sentences=1000):
    """
    Genera un texto largo a partir de las primeras 'num_sentences' oraciones del corpus Brown.
    
    Argumentos:
    - num_sentences (int): Número de oraciones a incluir en el texto. Por defecto, 1000.
    
    Retorna:
    - str: Texto largo generado.
    """
    nltk.download('brown')
    sentences = brown.sents()[:num_sentences]
    long_text = ' '.join([' '.join(sentence) for sentence in sentences])
    return long_text

def collect_wav_files(root_folder):
    """
    Recoge todos los archivos .wav de las subcarpetas de la carpeta raíz.
    
    Argumentos:
    - root_folder (str): Ruta a la carpeta raíz.
    
    Retorna:
    - list: Lista de rutas de archivos .wav.
    """
    wav_files = []
    for subdir, _, files in os.walk(root_folder):
        for file in files:
            if file.endswith('.wav'):
                wav_files.append(os.path.join(subdir, file))
    return wav_files

def split_sentences(long_text, target_length=12):
    """
    Divide el texto largo en oraciones más cortas de aproximadamente 'target_length' palabras.
    
    Argumentos:
    - long_text (str): Texto largo a dividir.
    - target_length (int): Número aproximado de palabras por oración. Por defecto, 12.
    
    Retorna:
    - list: Lista de oraciones más cortas.
    """
    words = long_text.split()
    short_sentences = []
    
    for i in range(0, len(words), target_length):
        short_sentences.append(' '.join(words[i:i + target_length]))
    
    return short_sentences

def find_largest_file(files):
    """
    Encuentra el archivo de mayor tamaño en una lista de archivos.
    
    Argumentos:
    - files (list): Lista de rutas de archivos.
    
    Retorna:
    - str: Ruta del archivo de mayor tamaño.
    """
    largest_file = max(files, key=os.path.getsize)
    return largest_file

def clone_voice_for_speaker(speaker_id, audio_folder, output_base_folder):
    """
    Clona la voz del locutor especificado y guarda los archivos de audio resultantes.
    
    Argumentos:
    - speaker_id (int): ID del locutor a clonar.
    - audio_folder (str): Ruta a la carpeta de audios de referencia.
    - output_base_folder (str): Ruta base a la carpeta de salida.
    """
    # Generar texto largo con 1000 oraciones
    long_text = generate_long_text(num_sentences=1000)

    # Dividir el texto en oraciones más cortas de aproximadamente 12 palabras cada una
    short_sentences = split_sentences(long_text, target_length=12)

    # Seleccionar las primeras 1000 frases cortas
    phrases = short_sentences[:1000]

    # Inicializar TTS (mstacotron2) y Vocoder (HiFIGAN)
    ms_tacotron2 = MSTacotron2.from_hparams(source="speechbrain/tts-mstacotron2-libritts", savedir="pretrained_models/tts-mstacotron2-libritts")
    hifi_gan = HIFIGAN.from_hparams(source="speechbrain/tts-hifigan-libritts-22050Hz", savedir="pretrained_models/tts-hifigan-libritts-22050Hz")

    # Recoger archivos de audio de referencia del locutor
    audio_files = collect_wav_files(audio_folder)

    # Encontrar el archivo de mayor tamaño
    reference_speech = find_largest_file(audio_files)

    # Crear carpeta de salida si no existe
    output_folder = os.path.join(output_base_folder, f"clonacion_F_{speaker_id}")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Clonar voz para cada frase y guardar el resultado
    for i, phrase in enumerate(phrases):
        mel_outputs, mel_lengths, alignments = ms_tacotron2.clone_voice(phrase, reference_speech)
        waveforms = hifi_gan.decode_batch(mel_outputs)
        output_path = os.path.join(output_folder, f"{i+1}.wav")
        torchaudio.save(output_path, waveforms.squeeze(1).cpu(), 22050)
        print(f"Guardado: {output_path}")

# IDs de los locutores a clonar y sus respectivas rutas de audios de referencia
speaker_data = {
    
    4779:"F:/ASV_SpeechBrain/speechbrain/LibriTTS/train-other-500/4779/4779_audios"
}

# Ruta base a la carpeta de salida
output_base_folder = "clonacion_LibriTTS"

# Clonar voces para todos los locutores especificados
for speaker_id, audio_folder in speaker_data.items():
    clone_voice_for_speaker(speaker_id, audio_folder, output_base_folder)

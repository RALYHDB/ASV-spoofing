import os
import torchaudio
from speechbrain.inference import FastSpeech2
from speechbrain.inference.vocoders import DiffWaveVocoder
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
    # Descarga el corpus Brown (si no está descargado)
    nltk.download('brown')
    
    # Selecciona las primeras 'num_sentences' oraciones del corpus Brown
    sentences = brown.sents()[:num_sentences]
    
    # Convierte las oraciones en una sola cadena de texto
    long_text = ' '.join([' '.join(sentence) for sentence in sentences])
    
    return long_text

# Intialize TTS (FastSpeech2) and Vocoder (DiffWave)
fastspeech2 = FastSpeech2.from_hparams(source="speechbrain/tts-fastspeech2-ljspeech", savedir="pretrained_models/tts-fastspeech2-ljspeech")
diffwave = DiffWaveVocoder.from_hparams(source="speechbrain/tts-diffwave-ljspeech", savedir="pretrained_models/tts-diffwave-ljspeech")

long_text=generate_long_text(num_sentences=1000)
# Extract 1000 short phrases from the text
phrases = [sentence.strip() for sentence in long_text.split('.') if len(sentence.split()) > 3][:1000]

# Create directory for saving the audio files
output_dir = "AudiosClonadosLJSpeech_1000_muestras"
os.makedirs(output_dir, exist_ok=True)

# Generate audio files for each phrase
for i, input_text in enumerate(phrases):
    # Running the TTS
    mel_output, durations, pitch, energy = fastspeech2.encode_text(
      [input_text],
      pace=1.0,        # scale up/down the speed
      pitch_rate=1.0,  # scale up/down the pitch
      energy_rate=1.0, # scale up/down the energy
    )

    # Running Vocoder (spectrogram-to-waveform)
    waveforms = diffwave.decode_batch(
        mel_output,
        hop_len=256,  # upsample factor, should be the same as "hop_len" during the extraction of mel-spectrogram
        fast_sampling=True,  # fast sampling is highly recommanded
        fast_sampling_noise_schedule=[0.0001, 0.001, 0.01, 0.05, 0.2, 0.5],  # customized noise schedule 
    )

    # Save the waveform
    filename = os.path.join(output_dir, f'vozClonada_LJSpeech_{i+1}.wav')
    torchaudio.save(filename, waveforms.squeeze(1), 22050)
    print(f'Saved {filename}')
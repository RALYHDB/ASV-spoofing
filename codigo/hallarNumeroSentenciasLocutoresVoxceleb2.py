import os

def count_audio_files(base_path):
    locutor_counts = {}

    # Recorrer todas las carpetas de locutores (idxxxxx)
    for locutor in os.listdir(base_path):
        locutor_path = os.path.join(base_path, locutor)
        
        if os.path.isdir(locutor_path):
            # Contador para los archivos .wav del locutor actual
            wav_count = 0
            
            # Recorrer recursivamente todas las subcarpetas y contar archivos .wav
            for root, dirs, files in os.walk(locutor_path):
                for file in files:
                    if file.lower().endswith('.wav'):
                        wav_count += 1
            
            # Guardar el conteo en el diccionario solo si se encontraron archivos .wav
            if wav_count > 0:
                locutor_counts[locutor] = wav_count

    # Ordenar los locutores por el número de archivos .wav (en orden descendente)
    sorted_locutor_counts = sorted(locutor_counts.items(), key=lambda x: x[1], reverse=True)

    return sorted_locutor_counts

# Ruta base de la base de datos
base_path = r'F:\ASV_SpeechBrain\speechbrain\vox2_aac\voxceleb2\wav'

# Contabilizar archivos de audio y obtener la lista ordenada
sorted_locutor_counts = count_audio_files(base_path)

# Guardar resultados en un archivo de texto
output_file = 'locutores_con_mas_audios.txt'

with open(output_file, 'w', encoding='utf-8') as f:
    for locutor, count in sorted_locutor_counts:
        f.write(f'{locutor}: {count} archivos de audio\n')

print(f'Se han guardado los resultados en "{output_file}".')

# Imprimir la lista de locutores con el mayor número de archivos de audio en la consola
for locutor, count in sorted_locutor_counts:
    print(f'{locutor}: {count} archivos de audio')

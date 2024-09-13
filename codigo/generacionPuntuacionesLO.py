import numpy as np
import os
import matplotlib.pyplot as plt

# Definir las listas de IDs y modelos
ids = [2834, 614, 585, 483, 5949, 215, 6127, 1384, 3867, 4779]
modelos = ['ecapa', 'xvector', 'resnet']

# Definir la carpeta de origen y destino
carpeta_origen = 'puntuaciones'
carpeta_destino = 'puntuaciones'

# Crear un diccionario para almacenar las puntuaciones concatenadas
puntuaciones_concatenadas = {modelo: [] for modelo in modelos}

# Leer y concatenar las puntuaciones
for modelo in modelos:
    for id in ids:
        nombre_archivo = f'puntuaciones_LO_{id}_{modelo}.npy'
        ruta_archivo = os.path.join(carpeta_origen, nombre_archivo)
        if os.path.exists(ruta_archivo):
            puntuaciones = np.load(ruta_archivo)
            puntuaciones_concatenadas[modelo].append(puntuaciones)
        else:
            print(f'Archivo no encontrado: {ruta_archivo}')

# Guardar las puntuaciones concatenadas
for modelo in modelos:
    concatenacion = np.concatenate(puntuaciones_concatenadas[modelo])
    nombre_archivo_destino = f'puntuaciones_LOs_femeninos_{modelo}.npy'
    ruta_archivo_destino = os.path.join(carpeta_destino, nombre_archivo_destino)
    np.save(ruta_archivo_destino, concatenacion)
    print(f'Guardado: {ruta_archivo_destino}')


# Procesar las puntuaciones concatenadas y mostrar histogramas
for modelo in modelos:
    # Concatenar las puntuaciones
    concatenacion = np.concatenate(puntuaciones_concatenadas[modelo])
    
    # Mostrar histograma
    plt.figure(figsize=(10, 6))
    plt.hist(concatenacion, bins=30,histtype='step', linewidth=1.5,density=True, edgecolor='black')
    plt.title(f'Histograma de Puntuaciones para {modelo}')
    plt.xlabel('Valor de la puntuación')
    plt.ylabel('Densidad de Frecuencia')
    
    # Mostrar el histograma en pantalla
    plt.show()
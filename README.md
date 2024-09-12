# Verificación Automática del Locutor y Ataques de Spoofing

Este repositorio contiene el código y los recursos asociados a mi Trabajo Fin de Grado (TFG), en el que evalúo el rendimiento de diferentes sistemas de verificación automática del locutor (ASV) frente a ataques de suplantación de identidad utilizando tecnologías de síntesis de voz (TTS).

### Explicación de cada sección:

1. **Título del Proyecto**: Evaluación sobre la aplicabilidad de los actuales conversores y sintetizadores de voz para la generación de voz falsificada.
2. **Descripción del Proyecto**: Explica brevemente en qué consiste el proyecto, su relevancia, y lo que otros pueden encontrar en el repositorio.
3. **Estructura del Repositorio**: Describe cómo están organizados los archivos y carpetas.
4. **Instalación y Requisitos**: Instrucciones para instalar dependencias y clonar el repositorio.
5. **Uso**: Explica cómo ejecutar el código, entrenar modelos, realizar experimentos y cualquier otro paso necesario.
6. **Resultados**: Resumen de los principales hallazgos o gráficos generados en los experimentos.
7. **Contribuciones**: Si aceptas contribuciones de otros, explica cómo hacerlo.
8. **Licencia**: Especifica la licencia bajo la cual publicas el código, si aplica.
9. **Contacto**: Proporciona información de contacto en caso de que alguien quiera hacer preguntas o colaborar.

## Descripción del Proyecto

En este proyecto, se analiza la vulnerabilidad de los sistemas de verificación de locutores basados en redes neuronales ante ataques de **spoofing** generados mediante síntesis de voz. Los sistemas de ASV evaluados incluyen modelos basados en:
- **TDNN**
- **ResNet**
- **ECAPA-TDNN**

Los sistemas de TTS utilizados incluyen:
- **FastSpeech**
- **Tacotron**

Y los **vocoders**:
- **DiffWave**
- **HiFi-GAN**

El objetivo es determinar el rendimiento de los sistemas de ASV frente a estos ataques utilizando la métrica de la Tasa de Error Equivalente (**EER**).

## Estructura del Repositorio

Este repositorio está organizado en las siguientes carpetas y archivos:

- `/MiTFG`
  - `/codigo`        # Contiene los scripts para los experimentos
  - `/documentos`    # Archivos PDF y recursos relacionados con el TFG
  - `/resultados`    # Resultados experimentales, gráficos, tablas, etc.
- `README.md`        # Este archivo
- `requirements.txt` # Archivo con las dependencias necesarias

## Instalación y Requisitos

### Requisitos previos

Para ejecutar este proyecto, necesitarás tener instaladas las siguientes dependencias:

- **Python 3.10.9** o superior.
- Las bibliotecas necesarias se encuentran en el archivo `requirements.txt`.

### Instalación de dependencias

1. Clona este repositorio a tu máquina local utilizando el siguiente comando:

    ```bash
    git clone https://github.com/tu_usuario/nombre_del_repositorio.git
    cd nombre_del_repositorio
    ```

2. Instala las dependencias ejecutando:

    ```bash
    pip install -r requirements.txt
    ```

Esto instalará todas las bibliotecas necesarias para ejecutar los experimentos.

## Uso

1. Asegúrate de tener todas las dependencias instaladas según los pasos anteriores.
2. Navega a la carpeta `/codigo` donde se encuentran los scripts de los experimentos.
3. Ejecuta los scripts según el experimento que desees realizar.

### Ejecución de los Scripts

Para ejecutar un experimento de verificación del locutor con ataques de **spoofing**, por ejemplo:

	```bash
	python codigo/nombre_del_script.py
	```
## Resultados

En la carpeta `/resultados`, encontrarás:

- **Histogramas** de puntuaciones de locutores objetivos, impostores y locutores sintetizados.
- **Curvas DET (Detection Error Tradeoff)**, que comparan el rendimiento de los sistemas de ASV frente a los ataques de spoofing.

Cada experimento generará gráficos y tablas que muestran los datos obtenidos y te permitirán analizar el rendimiento de los modelos evaluados.

| Sistema          | Base de Datos              | EER [%] |
|------------------|----------------------------|---------|
| x-vector         | VoxCeleb 2, LibriTTS        | 2.43    |
| ECAPA-TDNN       | VoxCeleb 2, LibriTTS        | 0.27    |
| ResNet           | VoxCeleb 2, LibriTTS        | 0.06    |


## Contribuciones

Las contribuciones son bienvenidas. Si deseas colaborar, sigue los siguientes pasos:

1. **Fork** este repositorio.
2. Crea una nueva rama para tus cambios (`git checkout -b mi-nueva-rama`).
3. Realiza los cambios necesarios y haz un commit (`git commit -am 'Añadir nueva característica'`).
4. Envía un pull request.

Agradezco cualquier sugerencia, mejora o aporte.

## Contacto

Si tienes alguna duda o sugerencia respecto al proyecto, puedes contactarme a través de:

- **Email:** franlopezh1b@gmail.com
- **LinkedIn:** [tu_perfil_linkedin](https://www.linkedin.com/in/tu_perfil)
"# Evaluaci-n-sobre-la-aplicabilidad-de-sintetizadores-de-voz-para-la-generaci-n-de-voz-falsificada" 

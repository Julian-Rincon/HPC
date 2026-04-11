# Taller 3: Procesamiento de Video

Conversión de un video a color a escala de grises con dos enfoques: secuencial y paralelo.

## Contenido

- `video_processor_Secuencial.py`: procesamiento secuencial
- `video_processor_Paralelo.py`: procesamiento paralelo
- `comparacion_resultados.py`: análisis comparativo a partir de los tiempos generados
- `20 PLANTILLAS de MEMES para videos.mp4`: video base
- `video_result_secuencial.mp4` y `video_result_paralelo.mp4`: resultados de ejemplo

## Requisitos

- Python 3.9+
- `opencv-python`
- `numpy`
- `matplotlib`

```bash
pip install opencv-python numpy matplotlib
```

## Ejecución

```bash
python "taller-3-procesamiento-video/video_processor_Secuencial.py"
python "taller-3-procesamiento-video/video_processor_Paralelo.py"
python "taller-3-procesamiento-video/comparacion_resultados.py"
```

También puedes pasar un video distinto como argumento:

```bash
python "taller-3-procesamiento-video/video_processor_Paralelo.py" "ruta/a/video.mp4"
```

## Archivos generados

Al ejecutar los scripts se crean:

- `frames_video_original/`
- `frames_video_result_secuencial/`
- `frames_video_result_paralelo/`
- `tiempos_secuencial.txt`
- `tiempos_paralelo.txt`

## Hallazgos

- La extracción y reconstrucción del video son etapas similares en ambos enfoques.
- La mejora principal aparece en el procesamiento de frames.
- El enfoque paralelo combina concurrencia y operaciones vectorizadas para reducir drásticamente el tiempo total.

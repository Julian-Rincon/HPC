# Taller 2: Detección de Bordes con Sobel

Implementación del operador Sobel en CPU con dos variantes: secuencial y paralela usando `multiprocessing`.

## Contenido

- `CPU-Secuencial.py`: versión secuencial
- `CPU-Paralelo.py`: versión paralela multicore
- `Comparador Secuencial vs Paralelo.py`: comparador de rendimiento
- `images.jpg`: imagen base de prueba
- `Resultados/`: salidas de ejemplo

## Requisitos

- Python 3.8+
- `numpy`
- `Pillow`

```bash
pip install numpy Pillow
```

## Ejecución

Desde la raíz del repositorio:

```bash
python "taller-2-deteccion-bordes-sobel/CPU-Secuencial.py"
python "taller-2-deteccion-bordes-sobel/CPU-Paralelo.py"
python "taller-2-deteccion-bordes-sobel/Comparador Secuencial vs Paralelo.py"
```

También puedes indicar una imagen personalizada:

```bash
python "taller-2-deteccion-bordes-sobel/CPU-Paralelo.py" "ruta/a/imagen.jpg"
```

## Resultados generados

Los scripts guardan las salidas en `Resultados/`:

- `resultado_gris_secuencial.png`
- `resultado_bordes_secuencial.png`
- `resultado_gris_paralelo.png`
- `resultado_bordes_paralelo.png`

## Hallazgos

- El paralelismo mejora el rendimiento cuando el tamaño de imagen justifica el overhead.
- Para imágenes pequeñas, la versión secuencial puede ser más rápida.

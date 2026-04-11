# HPC

Repositorio principal del curso de Computación de Alto Rendimiento. La rama `main` centraliza las entregas de los talleres en una sola estructura, con código, evidencias y documentación organizados por actividad.

## Integrantes

- Julian Rincón
- Paula Caballero

## Estructura del repositorio

```text
HPC/
├── taller-1-tsp-fuerza-bruta/
├── taller-2-deteccion-bordes-sobel/
├── taller-3-procesamiento-video/
└── taller-4-tsp-distribuido/
```

## Talleres incluidos

### 1. TSP por fuerza bruta

Ruta: `taller-1-tsp-fuerza-bruta/`

- Implementación secuencial y paralela del problema del viajante
- Archivo principal: `tsp_bruteforce.py`
- Documento de apoyo: `HPC_Tsp.pdf`

### 2. Detección de bordes con Sobel

Ruta: `taller-2-deteccion-bordes-sobel/`

- Comparación entre versión secuencial y paralela en CPU
- Scripts principales:
  - `CPU-Secuencial.py`
  - `CPU-Paralelo.py`
  - `Comparador Secuencial vs Paralelo.py`
- Evidencias generadas en `Resultados/`

### 3. Procesamiento de video a escala de grises

Ruta: `taller-3-procesamiento-video/`

- Conversión de video color a escala de grises
- Comparación entre procesamiento secuencial y paralelo
- Scripts principales:
  - `video_processor_Secuencial.py`
  - `video_processor_Paralelo.py`
  - `comparacion_resultados.py`

### 4. TSP distribuido con Docker Swarm

Ruta: `taller-4-tsp-distribuido/`

- Solución distribuida cliente-servidor para TSP
- API Flask desplegable con Docker
- Cliente Python para evaluar rutas por fuerza bruta
- Código base en `tsp_solution/`

## Requisitos generales

- Python 3.9 o superior
- `pip`
- Dependencias específicas por taller indicadas en cada carpeta
- Docker Desktop con Swarm habilitado para el Taller 4

## Ejecución rápida

```bash
git clone git@github.com:Julian-Rincon/HPC.git
cd HPC
```

Después, entra al taller que quieras ejecutar y sigue su `README.md`.

## Notas de organización

- La documentación ya no está separada por ramas.
- Cada taller tiene su propia carpeta y su propio `README.md`.
- La rama `main` queda como punto de entrada único del proyecto.

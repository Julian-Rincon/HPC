# Taller 1: TSP por Fuerza Bruta

Implementación didáctica del problema del viajante con dos enfoques: secuencial y paralelo mediante `multiprocessing`.

## Contenido

- `tsp_bruteforce.py`: script principal del taller
- `HPC_Tsp.pdf`: documento de apoyo y contexto académico

## Objetivo

- Evaluar todas las permutaciones posibles del TSP
- Comparar tiempos de ejecución entre el enfoque secuencial y el paralelo
- Medir speedup, eficiencia y consumo de recursos

## Requisitos

- Python 3.8+
- `psutil`

```bash
pip install psutil
```

## Ejecución

Desde la raíz del repositorio:

```bash
python taller-1-tsp-fuerza-bruta/tsp_bruteforce.py
```

## Observaciones

- La solución exacta por fuerza bruta crece factorialmente.
- La versión paralela mejora el tiempo de ejecución, pero también introduce overhead.
- Para cantidades altas de ciudades, el consumo de memoria puede crecer de forma importante.

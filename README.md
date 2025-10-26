# HPC — Taller: TSP por Fuerza Bruta (secuencial y paralelo)

## Descripción del Proyecto

Este repositorio contiene una implementación en Python de una solución por fuerza bruta
para el Problema del Viajante (TSP). El código compara dos enfoques:

- Un algoritmo secuencial que evalúa todas las permutaciones (fuerza bruta).
- Una versión paralela que distribuye la evaluación de rutas entre procesos usando
  el módulo `multiprocessing`.

El propósito principal es educativo: demostrar el coste exponencial del TSP, comparar
tiempos de ejecución secuenciales vs. paralelos y mostrar métricas de rendimiento y uso
de recursos. El archivo principal es `tsp_bruteforce.py`.

## Requisitos del Sistema

Recomendado (mínimos para pruebas locales pequeñas):

- CPU: procesador multi-core (2+ núcleos) — el script aprovecha procesos múltiples.
- RAM: 8 GB o más (el enfoque paralelo puede consumir mucha memoria si se generan
  todas las permutaciones en memoria).

Software y versiones probadas:

- Python 3.8+ (recomendado 3.10/3.11)
- Windows, macOS o Linux (el script usa `multiprocessing` y `psutil` — multiplataforma)

# HPC — Proyecto: TSP por Fuerza Bruta (secuencial y paralelo)

Este documento está organizado para cubrir punto por punto la petición original.

1) Descripción del Proyecto
----------------------------

Este repositorio contiene `tsp_bruteforce.py`, una implementación didáctica en Python
del Problema del Viajante (TSP) usando fuerza bruta. Incluye dos modos de ejecución:

- Secuencial: prueba cada permutación (fijando la ciudad 0 como inicio).
- Paralelo: divide el conjunto de permutaciones entre procesos usando
  `multiprocessing.Pool`.

Objetivos:

- Demostrar el crecimiento factorial del espacio de búsqueda.
- Comparar tiempos secuenciales vs. paralelos y medir speedup/eficiencia.
- Mostrar métricas de uso de memoria y CPU (usa `psutil`).

2) Requisitos del Sistema
-------------------------

- Hardware recomendado:
  - CPU multi-core (4+ núcleos recomendados; el usuario obtuvo 10 físicos / 16 lógicos).
  - RAM: 8 GB mínimo; 16+ GB recomendado para experimentar con n≈10–12.

- Software y versiones (ejemplo probado por el usuario):
  - Sistema operativo: Windows 10/11 (también funciona en Linux/macOS).
  - Python: 3.8+ (el usuario usó 3.13.7 — CPython).

- Librerías Python necesarias:
  - `psutil` (monitor de recursos)

Instalación rápida (PowerShell / pwsh):

```powershell
pip install psutil
```

3) Instalación
---------------

Comandos para clonar e instalar dependencias:

```powershell
git clone https://github.com/Julian-Rincon/HPC.git
cd HPC
pip install psutil
```

Instrucciones de ejecución (ejemplo):

```powershell
python tsp_bruteforce.py
# o en Windows con py launcher:
py -3 tsp_bruteforce.py
```

4) Estructura del Código
------------------------

Archivo principal: `tsp_bruteforce.py` — contiene todas las funciones; se explica a
continuación cada componente, su propósito, entradas/salidas y complejidad.

- `mostrar_informacion_sistema()`
  - Propósito: imprimir información hardware/OS/Python usando `platform` y `psutil`.
  - Entrada: ninguna. Salida: impresión por stdout.
  - Complejidad: O(1).

- `calcular_distancia(ciudad1, ciudad2)`
  - Propósito: distancia euclidiana entre dos coordenadas (x,y).
  - Entrada: dos tuplas float. Salida: float.
  - Complejidad: O(1).

- `calcular_distancia_ruta(ciudades, ruta)`
  - Propósito: calcular distancia total de una ruta circular (incluye regreso).
  - Validaciones: detección de rutas con índices fuera de rango, elementos repetidos,
    distancias NaN/Inf/negativas. Además, realiza un análisis estadístico simple
    y cálculos adicionales si detecta segmentos atípicos.
  - Entrada: `ciudades: List[Tuple[float,float]]`, `ruta: List[int]`.
  - Salida: float (distancia total).
  - Complejidad: O(n) para una ruta de n ciudades.

- `tsp_secuencial(ciudades)`
  - Propósito: evaluar todas las permutaciones (fijando la ciudad 0) y devolver la
    mejor ruta encontrada junto con métricas.
  - Entrada: lista de coordenadas. Salida: `(mejor_ruta, distancia_minima, metricas)`.
  - Complejidad temporal: O((n-1)!). Complejidad espacial adicional: O(1) aparte de
    la entrada y el iterador de permutaciones.

- `evaluar_grupo_rutas(args)`
  - Propósito: worker para evaluar un subconjunto de rutas (usado por `Pool.map`).
  - Entrada: tupla `(ciudades, rutas_del_grupo)`.
  - Salida: `(mejor_ruta_local, distancia_minima_local, rutas_evaluadas)`.

- `tsp_paralelo(ciudades, num_procesos=None)`
  - Propósito: genera todas las permutaciones, las reparte en `num_procesos` grupos
    y usa `multiprocessing.Pool` para evaluar cada grupo en paralelo.
  - Observación crítica: en la implementación actual se materializan todas las
    permutaciones en memoria (lista) antes de dividirlas — esto implica O((n-1)!)
    memoria, y puede causar `MemoryError` para n moderados.
  - Complejidad temporal: O((n-1)!) en trabajo total; tiempo de pared puede reducirse
    aproximadamente por factor de `num_procesos` menos overhead.

- `main()`
  - Propósito: orquestar la ejecución de ambos métodos, medir tiempos y memoria,
    presentar métricas y comparar resultados.

Flujo de ejecución (resumido / pseudocódigo):

```
mostrar_informacion_sistema()
definir ciudades
ejecutar tsp_secuencial -> medir tiempo, memoria
ejecutar tsp_paralelo  -> medir tiempo, memoria
calcular speedup, eficiencia y mostrar comparación
```

Pseudocódigo (secuencial):

```
fijar ciudad 0
para cada permutacion de (1..n-1):
    ruta = [0] + permutacion
    distancia = calcular_distancia_ruta(ciudades, ruta)
    si distancia < mejor:
        guardar mejor
```

Pseudocódigo (paralelo — actual):

```
generar lista completa de rutas (materializa todas)
dividir la lista en k trozos (k=num_procesos)
pool.map(evaluar_grupo_rutas, grupos)
reducir resultados para obtener la mejor ruta global
```

5) Características Técnicas
--------------------------

- Algoritmos implementados: Fuerza bruta (brute force) — evaluación completa de
  permutaciones.
- Patrones: maestro/worker (pool de procesos) en la versión paralela.
- Optimizaciones aplicadas:
  - Fijar la ciudad 0 para evitar rotaciones equivalentes (reduce factor n!).
  - Validaciones exhaustivas en `calcular_distancia_ruta`.
- Manejo de errores:
  - `ValueError` para rutas inválidas o resultados numéricos no válidos.
  - Uso de `psutil` para monitorización; no hay manejo explícito de `MemoryError`
    dentro del script — se recomienda limitar `num_procesos` o cambiar la estrategia.

6) Problemas Conocidos y Soluciones
----------------------------------

- Problema: consumo de memoria en `tsp_paralelo` porque materializa todas las
  permutaciones.
  - Solución: implementar streaming/chunks para no almacenar todo en memoria. Uso de
    `itertools.permutations` con `itertools.islice` y envío de bloques al pool.

- Problema: overhead de paralelización para problemas pequeños (n pequeño).
  - Solución: ejecutar paralelo sólo si `n` es lo suficientemente grande y medir
    previamente el tiempo secuencial para decidir.

- Errores comunes y troubleshooting rápido:
  - `MemoryError`: reducir `num_procesos`, disminuir n, o usar versión por chunks.
  - Resultados diferentes entre ejecuciones: revisar tolerancias numéricas y la
    implementación (ambos modos deberían producir la misma distancia óptima).

7) Limitaciones conocidas
-------------------------

- Escalabilidad: fuerza bruta es factorial — impracticable para n>12 en CPUs
  convencionales si se busca la solución exacta.
- La versión paralela actual no escala en memoria: puede fallar antes de aprovechar
  todos los núcleos si la RAM es insuficiente.


9) Ejemplo de salida (salida real)
---------------------------------------------

Se Muestra la salida real obtenida en su máquina; se incluye a
continuación (exacta).
```
================================================================================
INFORMACIÓN DEL SISTEMA
================================================================================
📌 PROCESADOR:
   Procesador: Intel64 Family 6 Model 186 Stepping 2, GenuineIntel
   Arquitectura: AMD64
   Núcleos físicos: 10
   Núcleos lógicos (threads): 16
   Frecuencia actual: 2400.00 MHz
   Frecuencia máxima: 2400.00 MHz
📌 MEMORIA RAM:
   Total: 31.65 GB
   Disponible: 4.46 GB
   En uso: 27.19 GB
   Porcentaje usado: 85.9%
📌 SISTEMA OPERATIVO:
   Sistema: Windows
   Versión: 10.0.26200
   Release: 11
📌 ENTORNO DE PYTHON:
   Versión de Python: 3.13.7
   Implementación: CPython
================================================================================
================================================================================
PROBLEMA DEL VIAJERO - MÉTODO FUERZA BRUTA
COMPARACIÓN: SECUENCIAL vs PARALELO
================================================================================
Número de ciudades: 10
Rutas totales a evaluar: 362,880
Coordenadas de ciudades:
   Ciudad 0: (0, 0)
   Ciudad 1: (2, 8)
   Ciudad 2: (5, 3)
   Ciudad 3: (8, 6)
   Ciudad 4: (9, 2)
   Ciudad 5: (3, 9)
   Ciudad 6: (4, 1)
   Ciudad 7: (7, 7)
   Ciudad 8: (1, 4)
   Ciudad 9: (6, 5)
--------------------------------------------------------------------------------
 EJECUTANDO ALGORITMO SECUENCIAL (FUERZA BRUTA)
--------------------------------------------------------------------------------
   Evaluando rutas secuencialmente (fuerza bruta)...
 Mejor ruta encontrada: [0, 8, 1, 5, 7, 3, 4, 9, 2, 6]
 Distancia mínima: 32.5078 unidades
 Tiempo de ejecución: 9.903752 segundos
 Rutas evaluadas: 362,880
 Procesos utilizados: 1
 Uso de memoria: 0.3751 GB
--------------------------------------------------------------------------------
 EJECUTANDO ALGORITMO PARALELO (FUERZA BRUTA DISTRIBUIDA)
--------------------------------------------------------------------------------
   Generando todas las permutaciones para dividir entre 16 procesos...
   Distribuyendo 362880 rutas entre 16 procesos...
   Cada proceso evaluará aproximadamente 22680 rutas...
 Mejor ruta encontrada: [0, 8, 1, 5, 7, 3, 4, 9, 2, 6]
 Distancia mínima: 32.5078 unidades
 Tiempo de ejecución: 3.632346 segundos
 Rutas evaluadas: 362,880
 Procesos utilizados: 16
 Rutas por proceso: ~22,680
 Uso de memoria: 0.0665 GB
================================================================================
ANÁLISIS COMPARATIVO DE RENDIMIENTO
================================================================================
MÉTRICAS DE ACELERACIÓN:
   Speedup (aceleración): 2.73x
   Eficiencia paralela: 17.04%
   Mejora de tiempo: 63.32%
   Tiempo ahorrado: 6.271406 segundos
COMPARACIÓN DE TIEMPOS:
   Tiempo secuencial: 9.903752 segundos
   Tiempo paralelo: 3.632346 segundos
   Diferencia: 6.271406 segundos
COMPARACIÓN DE RECURSOS:
   Procesos secuencial: 1
   Procesos paralelo: 16
   Núcleos utilizados: 16 de 16
VERIFICACIÓN DE RESULTADOS:
   ✓ Ambos algoritmos encontraron la misma solución óptima
   ✓ Distancia: 32.5078 unidades
CONCLUSIÓN:
   El algoritmo paralelo fue 2.73 veces más rápido
   Se logró aprovechar 17.0% de la capacidad de paralelización
================================================================================
```

Interpretación corta: la versión paralela reduce significativamente el tiempo en
este ejemplo (≈2.7x), pero la eficiencia por núcleo es baja (~17%) porque existe
overhead en la creación/gestión de procesos y reparto de trabajo. Para problemas
más grandes conviene evitar materializar permutaciones y/o usar heurísticas.


---

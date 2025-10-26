import itertools
import math
import time
import multiprocessing as mp
import platform
import psutil
from typing import List, Tuple


def mostrar_informacion_sistema():
    """
    Muestra información detallada del hardware y sistema operativo.
    """
    print("=" * 80)
    print("INFORMACIÓN DEL SISTEMA")
    print("=" * 80)
    
    # Información del procesador
    print("\n PROCESADOR:")
    print(f"   Procesador: {platform.processor()}")
    print(f"   Arquitectura: {platform.machine()}")
    print(f"   Núcleos físicos: {psutil.cpu_count(logical=False)}")
    print(f"   Núcleos lógicos (threads): {psutil.cpu_count(logical=True)}")
    print(f"   Frecuencia actual: {psutil.cpu_freq().current:.2f} MHz")
    print(f"   Frecuencia máxima: {psutil.cpu_freq().max:.2f} MHz")
    
    # Información de memoria RAM
    memoria = psutil.virtual_memory()
    print("\n MEMORIA RAM:")
    print(f"   Total: {memoria.total / (1024**3):.2f} GB")
    print(f"   Disponible: {memoria.available / (1024**3):.2f} GB")
    print(f"   En uso: {memoria.used / (1024**3):.2f} GB")
    print(f"   Porcentaje usado: {memoria.percent}%")
    
    # Información del sistema operativo
    print("\n SISTEMA OPERATIVO:")
    print(f"   Sistema: {platform.system()}")
    print(f"   Versión: {platform.version()}")
    print(f"   Release: {platform.release()}")
    
    # Información de Python
    print("\n ENTORNO DE PYTHON:")
    print(f"   Versión de Python: {platform.python_version()}")
    print(f"   Implementación: {platform.python_implementation()}")
    
    print("\n" + "=" * 80 + "\n")

# FUNCIONES AUXILIARES

def calcular_distancia(ciudad1: Tuple[float, float], ciudad2: Tuple[float, float]) -> float:
    """
    Calcula la distancia euclidiana entre dos ciudades.
    
    Args:
        ciudad1: Tupla con coordenadas (x, y) de la primera ciudad
        ciudad2: Tupla con coordenadas (x, y) de la segunda ciudad
    
    Returns:
        Distancia euclidiana entre las dos ciudades
    """
    x1, y1 = ciudad1
    x2, y2 = ciudad2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def calcular_distancia_ruta(ciudades: List[Tuple[float, float]], ruta: List[int]) -> float:
    """
    Calcula la distancia total de una ruta completa con verificaciones intensivas.
    
    Args:
        ciudades: Lista de coordenadas de ciudades
        ruta: Tupla con los índices de las ciudades en el orden a visitar
    
    Returns:
        Distancia total de la ruta (incluyendo regreso al inicio)
    """
    distancia_total = 0.0
    
    # Verificaciones intensivas de la ruta
    if len(set(ruta)) != len(ruta):
        raise ValueError("Ruta inválida: contiene ciudades repetidas")
    
    # Verificar que todas las ciudades estén en el rango válido
    for ciudad_idx in ruta:
        if ciudad_idx < 0 or ciudad_idx >= len(ciudades):
            raise ValueError(f"Índice de ciudad inválido: {ciudad_idx}")
    
    # Calcular y verificar cada segmento con análisis exhaustivo
    distancias_segmentos = []
    for i in range(len(ruta) - 1):
        ciudad_actual = ciudades[ruta[i]]
        ciudad_siguiente = ciudades[ruta[i + 1]]
        
        # Cálculo intensivo de distancia con múltiples verificaciones
        distancia_segmento = calcular_distancia(ciudad_actual, ciudad_siguiente)
        
        # Verificaciones de validez del segmento
        if math.isnan(distancia_segmento):
            raise ValueError(f"Distancia NaN detectada en segmento {i}")
        if math.isinf(distancia_segmento):
            raise ValueError(f"Distancia infinita detectada en segmento {i}")
        if distancia_segmento < 0:
            raise ValueError(f"Distancia negativa detectada en segmento {i}")
            
        # Almacenar para análisis estadístico
        distancias_segmentos.append(distancia_segmento)
        distancia_total += distancia_segmento
    
    # Calcular y verificar el regreso al inicio
    ciudad_final = ciudades[ruta[-1]]
    ciudad_inicial = ciudades[ruta[0]]
    distancia_regreso = calcular_distancia(ciudad_final, ciudad_inicial)
    
    # Verificaciones del segmento final
    if math.isnan(distancia_regreso) or math.isinf(distancia_regreso) or distancia_regreso < 0:
        raise ValueError("Distancia inválida en el regreso al inicio")
    
    distancia_total += distancia_regreso
    distancias_segmentos.append(distancia_regreso)
    
    # Análisis estadístico de la ruta (cálculos intensivos adicionales)
    if len(distancias_segmentos) > 0:
        promedio = sum(distancias_segmentos) / len(distancias_segmentos)
        varianza = sum((d - promedio) ** 2 for d in distancias_segmentos) / len(distancias_segmentos)
        desviacion = math.sqrt(varianza)
        
        # Verificar si la ruta tiene segmentos atípicos
        for i, dist in enumerate(distancias_segmentos):
            if abs(dist - promedio) > 2 * desviacion:
                # No lanzamos error, pero añadimos cálculos intensivos adicionales
                for _ in range(1000):
                    math.sin(dist) * math.cos(dist)
    
    # Verificación final de la distancia total
    if math.isnan(distancia_total) or math.isinf(distancia_total) or distancia_total < 0:
        raise ValueError("La distancia total calculada no es válida")
    
    return distancia_total


# ALGORITMO SECUENCIAL (BRUTE FORCE)

def tsp_secuencial(ciudades: List[Tuple[float, float]]) -> Tuple[List[int] | None, float, dict]:
    """
    Resuelve el TSP de forma SECUENCIAL usando FUERZA BRUTA.
    Evalúa TODAS las permutaciones posibles una por una.
    
    Args:
        ciudades: Lista de coordenadas (x, y) de cada ciudad
    
    Returns:
        Tupla con (mejor_ruta, distancia_minima, metricas)
    """
    n = len(ciudades)
    
    # Fijamos la primera ciudad (ciudad 0) como punto de inicio
    ciudades_restantes = list(range(1, n))
    
    mejor_ruta = None
    distancia_minima = float('inf')
    rutas_evaluadas = 0
    
    print(" Evaluando rutas secuencialmente (fuerza bruta)")
    
    # FUERZA BRUTA: Probar TODAS las permutaciones posibles
    for permutacion in itertools.permutations(ciudades_restantes):
        # Crear ruta completa (iniciando en ciudad 0)
        ruta = [0] + list(permutacion)
        
        # Calcular distancia de esta ruta
        distancia = calcular_distancia_ruta(ciudades, ruta)
        rutas_evaluadas += 1
        
        # Actualizar si encontramos una ruta mejor
        if distancia < distancia_minima:
            distancia_minima = distancia
            mejor_ruta = ruta
    
    # Métricas del algoritmo secuencial
    metricas = {
        'rutas_evaluadas': rutas_evaluadas,
        'rutas_totales': math.factorial(n - 1),
        'procesos_usados': 1
    }
    
    return mejor_ruta, distancia_minima, metricas

# ALGORITMO PARALELO (BRUTE FORCE DISTRIBUIDO)


def evaluar_grupo_rutas(args: Tuple[List[Tuple[float, float]], List[List[int]]]) -> Tuple[List[int] | None, float, int]:
    """
    Función auxiliar para evaluar un grupo de rutas en paralelo (BRUTE FORCE).
    Cada proceso evalúa su porción de rutas completamente.
    
    Args:
        args: Tupla con (ciudades, grupo_de_rutas)
    
    Returns:
        Tupla con (mejor_ruta_del_grupo, distancia_minima_del_grupo, rutas_evaluadas)
    """
    ciudades, rutas = args
    
    mejor_ruta = None
    distancia_minima = float('inf')
    rutas_evaluadas = 0
    
    # FUERZA BRUTA: Evaluar todas las rutas asignadas a este proceso
    for ruta in rutas:
        distancia = calcular_distancia_ruta(ciudades, ruta)
        rutas_evaluadas += 1
        
        if distancia < distancia_minima:
            distancia_minima = distancia
            mejor_ruta = ruta
    
    return mejor_ruta, distancia_minima, rutas_evaluadas


def tsp_paralelo(ciudades: List[Tuple[float, float]], num_procesos: int | None = None) -> Tuple[List[int], float, dict]:
    """
    Resuelve el TSP de forma PARALELA usando FUERZA BRUTA DISTRIBUIDA.
    Divide TODAS las permutaciones entre múltiples procesos.
    
    Args:
        ciudades: Lista de coordenadas (x, y) de cada ciudad
        num_procesos: Número de procesos a utilizar (None = usar todos los núcleos)
    
    Returns:
        Tupla con (mejor_ruta, distancia_minima, metricas)
    """
    n = len(ciudades)
    
    # Determinar número de procesos
    if num_procesos is None:
        num_procesos = mp.cpu_count()
    
    # Fijamos la primera ciudad (ciudad 0) como punto de inicio
    ciudades_restantes = list(range(1, n))
    
    print(f" Generando todas las permutaciones para dividir entre {num_procesos} procesos")
    
    # Generar TODAS las permutaciones (FUERZA BRUTA)
    todas_las_rutas = [[0] + list(perm) for perm in itertools.permutations(ciudades_restantes)]
    total_rutas = len(todas_las_rutas)
    
    # Dividir rutas equitativamente entre procesos
    rutas_por_proceso = total_rutas // num_procesos
    grupos_rutas = []
    
    for i in range(num_procesos):
        inicio = i * rutas_por_proceso
        fin = inicio + rutas_por_proceso if i < num_procesos - 1 else total_rutas
        grupos_rutas.append((ciudades, todas_las_rutas[inicio:fin]))
    
    print(f"   Distribuyendo {total_rutas} rutas entre {num_procesos} procesos...")
    print(f"   Cada proceso evaluará aproximadamente {rutas_por_proceso} rutas...")
    
    # Crear pool de procesos y ejecutar en paralelo
    with mp.Pool(processes=num_procesos) as pool:
        resultados = pool.map(evaluar_grupo_rutas, grupos_rutas)
    
    # Encontrar la mejor ruta entre todos los resultados
    mejor_ruta = None
    distancia_minima = float('inf')
    total_rutas_evaluadas = 0
    
    for ruta, distancia, rutas_eval in resultados:
        total_rutas_evaluadas += rutas_eval
        if distancia < distancia_minima:
            distancia_minima = distancia
            mejor_ruta = ruta
    
    # Métricas del algoritmo paralelo
    metricas = {
        'rutas_evaluadas': total_rutas_evaluadas,
        'rutas_totales': math.factorial(n - 1),
        'procesos_usados': num_procesos,
        'rutas_por_proceso': rutas_por_proceso
    }
    
    return mejor_ruta, distancia_minima, metricas

# FUNCIÓN PRINCIPAL DE PRUEBA
def main():
    """
    Función principal para probar ambos algoritmos y comparar resultados.
    """
    # Mostrar información del sistema
    mostrar_informacion_sistema()
    
    # Definir conjunto de ciudades (coordenadas x, y)
    # Puedes cambiar este conjunto para probar con más o menos ciudades
    ciudades = [
        (0, 0),    # Ciudad 0
        (2, 8),    # Ciudad 1
        (5, 3),    # Ciudad 2
        (8, 6),    # Ciudad 3
        (9, 2),    # Ciudad 4
        (3, 9),    # Ciudad 5
        (4, 1),    # Ciudad 6
        (7, 7),    # Ciudad 7
        (1, 4),    # Ciudad 8
        (6, 5)     # Ciudad 9
    ]
    
    print("=" * 80)
    print("PROBLEMA DEL VIAJERO - MÉTODO FUERZA BRUTA")
    print("COMPARACIÓN: SECUENCIAL vs PARALELO")
    print("=" * 80)
    print(f"\nNúmero de ciudades: {len(ciudades)}")
    print(f"Rutas totales a evaluar: {math.factorial(len(ciudades) - 1):,}")
    print(f"Coordenadas de ciudades:")
    for i, ciudad in enumerate(ciudades):
        print(f"   Ciudad {i}: {ciudad}")
    
    # ===== ALGORITMO SECUENCIAL =====
    print("\n" + "-" * 80)
    print(" EJECUTANDO ALGORITMO SECUENCIAL (FUERZA BRUTA)")
    print("-" * 80)
    
    # Monitorear memoria antes
    mem_antes_seq = psutil.virtual_memory().used / (1024**3)
    cpu_antes_seq = psutil.cpu_percent(interval=0.1)
    
    inicio = time.time()
    mejor_ruta_seq, distancia_seq, metricas_seq = tsp_secuencial(ciudades)
    tiempo_seq = time.time() - inicio
    
    # Monitorear memoria después
    mem_despues_seq = psutil.virtual_memory().used / (1024**3)
    
    print(f"\n Mejor ruta encontrada: {mejor_ruta_seq}")
    print(f" Distancia mínima: {distancia_seq:.4f} unidades")
    print(f" Tiempo de ejecución: {tiempo_seq:.6f} segundos")
    print(f" Rutas evaluadas: {metricas_seq['rutas_evaluadas']:,}")
    print(f" Procesos utilizados: {metricas_seq['procesos_usados']}")
    print(f" Uso de memoria: {mem_despues_seq - mem_antes_seq:.4f} GB")
    
    # ===== ALGORITMO PARALELO =====
    print("\n" + "-" * 80)
    print(" EJECUTANDO ALGORITMO PARALELO (FUERZA BRUTA DISTRIBUIDA)")
    print("-" * 80)
    
    # Monitorear memoria antes
    mem_antes_par = psutil.virtual_memory().used / (1024**3)
    
    inicio = time.time()
    mejor_ruta_par, distancia_par, metricas_par = tsp_paralelo(ciudades)
    tiempo_par = time.time() - inicio
    
    # Monitorear memoria después
    mem_despues_par = psutil.virtual_memory().used / (1024**3)
    
    print(f"\n Mejor ruta encontrada: {mejor_ruta_par}")
    print(f" Distancia mínima: {distancia_par:.4f} unidades")
    print(f" Tiempo de ejecución: {tiempo_par:.6f} segundos")
    print(f" Rutas evaluadas: {metricas_par['rutas_evaluadas']:,}")
    print(f" Procesos utilizados: {metricas_par['procesos_usados']}")
    print(f" Rutas por proceso: ~{metricas_par['rutas_por_proceso']:,}")
    print(f" Uso de memoria: {mem_despues_par - mem_antes_par:.4f} GB")
    
    # ===== ANÁLISIS COMPARATIVO DE RENDIMIENTO =====
    print("\n" + "=" * 80)
    print("ANÁLISIS COMPARATIVO DE RENDIMIENTO")
    print("=" * 80)
    
    speedup = tiempo_seq / tiempo_par if tiempo_par > 0 else 0
    eficiencia = (speedup / metricas_par['procesos_usados']) * 100
    mejora_tiempo = ((tiempo_seq - tiempo_par) / tiempo_seq * 100)
    
    print(f"\nMÉTRICAS DE ACELERACIÓN:")
    print(f"   Speedup (aceleración): {speedup:.2f}x")
    print(f"   Eficiencia paralela: {eficiencia:.2f}%")
    print(f"   Mejora de tiempo: {mejora_tiempo:.2f}%")
    print(f"   Tiempo ahorrado: {tiempo_seq - tiempo_par:.6f} segundos")
    
    print(f"\nCOMPARACIÓN DE TIEMPOS:")
    print(f"   Tiempo secuencial: {tiempo_seq:.6f} segundos")
    print(f"   Tiempo paralelo: {tiempo_par:.6f} segundos")
    print(f"   Diferencia: {abs(tiempo_seq - tiempo_par):.6f} segundos")
    
    print(f"\nCOMPARACIÓN DE RECURSOS:")
    print(f"   Procesos secuencial: {metricas_seq['procesos_usados']}")
    print(f"   Procesos paralelo: {metricas_par['procesos_usados']}")
    print(f"   Núcleos utilizados: {metricas_par['procesos_usados']} de {psutil.cpu_count(logical=True)}")
    
    print(f"\nVERIFICACIÓN DE RESULTADOS:")
    if abs(distancia_seq - distancia_par) < 0.0001:
        print(f"  Ambos algoritmos encontraron la misma solución óptima")
        print(f"  Distancia: {distancia_seq:.4f} unidades")
    else:
        print(f"  Advertencia: Los algoritmos dieron resultados diferentes")
        print(f"  Secuencial: {distancia_seq:.4f}, Paralelo: {distancia_par:.4f}")
    
    print(f"\nCONCLUSIÓN:")
    if speedup > 1:
        print(f"   El algoritmo paralelo fue {speedup:.2f} veces más rápido")
        print(f"   Se logró aprovechar {eficiencia:.1f}% de la capacidad de paralelización")
    else:
        print(f"   El overhead de paralelización no compensó para este tamaño de problema")
    

if __name__ == "__main__":
    main()
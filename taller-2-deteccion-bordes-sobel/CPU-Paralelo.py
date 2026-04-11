import os
import math
import sys
import time
from multiprocessing import Pool, cpu_count
from pathlib import Path

import numpy as np
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "Resultados"
DEFAULT_IMAGE = BASE_DIR / "images.jpg"

def cargar_imagen(ruta):
    """Carga una imagen y la convierte a array numpy"""
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encontró la imagen en: {ruta}")
    img = Image.open(ruta).convert("RGB")
    return np.array(img)

def rgb_a_escala_grises(img_rgb):
    """Convierte imagen RGB a escala de grises usando promedio ponderado"""
    if len(img_rgb.shape) == 3:
        return np.dot(img_rgb[...,:3], [0.299, 0.587, 0.114])
    return img_rgb

def procesar_fila_sobel(args):
    """
    Procesa una fila de la imagen aplicando Sobel
    Esta función será ejecutada en paralelo por múltiples cores
    """
    i, img_gris, columnas = args
    
    # Kernels de Sobel
    Kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    Ky = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    
    # Array para almacenar resultado de esta fila
    fila_resultado = np.zeros(columnas, dtype=np.float32)
    
    # Procesar cada columna en esta fila (excluyendo bordes)
    for j in range(1, columnas - 1):
        # Extraer ventana 3x3 alrededor del píxel (i, j)
        ventana = img_gris[i-1:i+2, j-1:j+2]
        
        # Calcular Gx: suma de productos elemento a elemento
        Gx = 0.0
        for ki in range(3):
            for kj in range(3):
                Gx += ventana[ki, kj] * Kx[ki, kj]
        
        # Calcular Gy: suma de productos elemento a elemento
        Gy = 0.0
        for ki in range(3):
            for kj in range(3):
                Gy += ventana[ki, kj] * Ky[ki, kj]
        
        # Calcular magnitud del gradiente
        magnitud = math.sqrt(Gx**2 + Gy**2)
        fila_resultado[j] = magnitud
    
    return i, fila_resultado

def sobel_paralelo_multicore(img_gris, num_procesos=None):
    """
    Aplica Sobel usando multiprocesamiento (paralelismo multicore)
    Divide el trabajo por filas entre múltiples procesos
    """
    filas, columnas = img_gris.shape
    
    # Si no se especifica, usar todos los cores disponibles
    if num_procesos is None:
        num_procesos = cpu_count()
    
    # OPTIMIZACIÓN: Para imágenes pequeñas, reducir número de procesos
    # Regla: mínimo 1000 píxeles por proceso para que valga la pena el overhead
    pixeles_totales = (filas - 2) * (columnas - 2)
    pixeles_por_proceso = pixeles_totales / num_procesos
    
    if pixeles_por_proceso < 1000:
        num_procesos_optimo = max(1, pixeles_totales // 1000)
        print(f"   ⚠️  OPTIMIZACIÓN: Imagen pequeña detectada")
        print(f"   Reduciendo procesos de {num_procesos} a {num_procesos_optimo}")
        num_procesos = num_procesos_optimo
    
    print(f"   Configuración Multicore:")
    print(f"   - Cores disponibles: {cpu_count()}")
    print(f"   - Cores utilizados: {num_procesos}")
    print(f"   - Filas a procesar: {filas - 2} (excluyendo bordes)")
    print(f"   - Píxeles por proceso: ~{((filas - 2) * (columnas - 2)) // num_procesos:,}")
    
    # Crear imagen de salida
    img_bordes = np.zeros((filas, columnas), dtype=np.float32)
    
    # Preparar argumentos para cada fila (excluyendo primera y última)
    argumentos = [(i, img_gris, columnas) for i in range(1, filas - 1)]
    
    # Crear pool de procesos y procesar en paralelo
    with Pool(processes=num_procesos) as pool:
        resultados = pool.map(procesar_fila_sobel, argumentos)
    
    # Ensamblar resultados
    for i, fila_resultado in resultados:
        img_bordes[i, :] = fila_resultado
    
    # Normalizar valores a rango 0-255
    max_val = np.max(img_bordes)
    if max_val > 0:
        img_bordes = (img_bordes / max_val * 255)
    
    return img_bordes.astype(np.uint8)

def sobel_paralelo_multicore_chunks(img_gris, num_procesos=None):
    """
    Versión alternativa: divide la imagen en chunks (bloques de filas)
    Más eficiente para imágenes muy grandes
    """
    filas, columnas = img_gris.shape
    
    if num_procesos is None:
        num_procesos = cpu_count()
    
    # Calcular tamaño de chunk por proceso
    filas_procesables = filas - 2  # Excluir bordes
    chunk_size = max(1, filas_procesables // num_procesos)
    
    print(f"   Configuración Multicore (Chunks):")
    print(f"   - Cores utilizados: {num_procesos}")
    print(f"   - Filas por chunk: ~{chunk_size}")
    
    img_bordes = np.zeros((filas, columnas), dtype=np.float32)
    
    # Procesar por chunks
    argumentos = []
    for inicio in range(1, filas - 1, chunk_size):
        fin = min(inicio + chunk_size, filas - 1)
        for i in range(inicio, fin):
            argumentos.append((i, img_gris, columnas))
    
    with Pool(processes=num_procesos) as pool:
        resultados = pool.map(procesar_fila_sobel, argumentos)
    
    for i, fila_resultado in resultados:
        img_bordes[i, :] = fila_resultado
    
    max_val = np.max(img_bordes)
    if max_val > 0:
        img_bordes = (img_bordes / max_val * 255)
    
    return img_bordes.astype(np.uint8)

def guardar_imagen(img_array, ruta_completa):
    """Guarda el array como imagen"""
    arr = np.array(img_array)
    if arr.dtype != np.uint8:
        arr = np.clip(arr, 0, 255).astype(np.uint8)
    img = Image.fromarray(arr)
    img.save(ruta_completa)
    print(f"   Imagen guardada: {ruta_completa}")

def main():
    ruta_entrada = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_IMAGE
    RESULTS_DIR.mkdir(exist_ok=True)
    
    print("=" * 70)
    print("DETECCIÓN DE BORDES SOBEL - PARALELO MULTICORE (CPU)")
    print("=" * 70)
    
    # Información del sistema
    print(f"\nInformación del Sistema:")
    print(f"   Cores de CPU disponibles: {cpu_count()}")
    print(f"   Python: {sys.version.split()[0]}")
    print(f"   NumPy: {np.__version__}")
    
    # 1. Cargar imagen
    print("\n1. Cargando imagen...")
    try:
        img_original = cargar_imagen(str(ruta_entrada))
        print(f"   Ruta: {ruta_entrada}")
        print(f"   Dimensiones: {img_original.shape}")
        print(f"   Píxeles totales: {img_original.shape[0] * img_original.shape[1]:,}")
    except Exception as e:
        print(f"   ERROR: {e}")
        return
    
    # 2. Convertir a escala de grises
    print("\n2. Convirtiendo a escala de grises...")
    img_gris = rgb_a_escala_grises(img_original)
    ruta_gris = RESULTS_DIR / "resultado_gris_paralelo.png"
    guardar_imagen(img_gris.astype(np.uint8), str(ruta_gris))
    
    # 3. Aplicar Sobel con multiprocesamiento
    print("\n3. Aplicando Sobel con paralelismo multicore...")
    print("   (Cada proceso trabaja en un subconjunto de filas)")
    
    try:
        inicio = time.time()
        img_bordes = sobel_paralelo_multicore(img_gris)
        tiempo_paralelo = time.time() - inicio
    except Exception as e:
        print(f"   ERROR: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 4. Guardar resultado
    print("\n4. Guardando resultado...")
    ruta_bordes = RESULTS_DIR / "resultado_bordes_paralelo.png"
    guardar_imagen(img_bordes, str(ruta_bordes))
    
    # 5. Mostrar resultados
    print("\n" + "=" * 70)
    print("RESULTADOS")
    print("=" * 70)
    print(f"\nALGORITMO PARALELO MULTICORE:")
    print(f"  Tiempo de ejecución: {tiempo_paralelo:.4f} segundos")
    print(f"  Píxeles procesados: {img_bordes.shape[0] * img_bordes.shape[1]:,}")
    print(f"  Throughput: {(img_bordes.shape[0] * img_bordes.shape[1])/tiempo_paralelo:,.0f} píxeles/segundo")
    print(f"  Cores utilizados: {cpu_count()}")
    
    print("\n" + "=" * 70)
    print("Archivos generados:")
    print(f"  • {ruta_gris}")
    print(f"  • {ruta_bordes}")
    print("=" * 70)
    
    print("\nNOTA: Para comparar con versión secuencial, ejecuta 'CPU-Secuencial.py'")

if __name__ == "__main__":
    main()

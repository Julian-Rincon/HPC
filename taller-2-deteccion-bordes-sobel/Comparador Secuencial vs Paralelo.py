import numpy as np
from PIL import Image
import time
import sys
import math
from multiprocessing import Pool, cpu_count
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
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

def redimensionar_imagen(img, escala):
    """Redimensiona la imagen para pruebas de rendimiento"""
    nueva_altura = int(img.shape[0] * escala)
    nueva_anchura = int(img.shape[1] * escala)
    img_pil = Image.fromarray(img)
    img_redimensionada = img_pil.resize((nueva_anchura, nueva_altura), Image.LANCZOS)
    return np.array(img_redimensionada)

# ==================== ALGORITMO SECUENCIAL ====================
def sobel_secuencial(img_gris):
    """Aplica Sobel de forma SECUENCIAL"""
    filas, columnas = img_gris.shape
    
    Kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    Ky = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    
    img_bordes = np.zeros((filas, columnas), dtype=np.float32)
    
    for i in range(1, filas - 1):
        for j in range(1, columnas - 1):
            ventana = img_gris[i-1:i+2, j-1:j+2]
            
            Gx = 0.0
            for ki in range(3):
                for kj in range(3):
                    Gx += ventana[ki, kj] * Kx[ki, kj]
            
            Gy = 0.0
            for ki in range(3):
                for kj in range(3):
                    Gy += ventana[ki, kj] * Ky[ki, kj]
            
            magnitud = math.sqrt(Gx**2 + Gy**2)
            img_bordes[i, j] = magnitud
    
    max_val = np.max(img_bordes)
    if max_val > 0:
        img_bordes = (img_bordes / max_val * 255)
    
    return img_bordes.astype(np.uint8)

# ==================== ALGORITMO PARALELO ====================
def procesar_fila_sobel(args):
    """Procesa una fila de la imagen aplicando Sobel"""
    i, img_gris, columnas = args
    
    Kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    Ky = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    
    fila_resultado = np.zeros(columnas, dtype=np.float32)
    
    for j in range(1, columnas - 1):
        ventana = img_gris[i-1:i+2, j-1:j+2]
        
        Gx = 0.0
        for ki in range(3):
            for kj in range(3):
                Gx += ventana[ki, kj] * Kx[ki, kj]
        
        Gy = 0.0
        for ki in range(3):
            for kj in range(3):
                Gy += ventana[ki, kj] * Ky[ki, kj]
        
        magnitud = math.sqrt(Gx**2 + Gy**2)
        fila_resultado[j] = magnitud
    
    return i, fila_resultado

def sobel_paralelo_multicore(img_gris, num_procesos=None):
    """Aplica Sobel usando multiprocesamiento"""
    filas, columnas = img_gris.shape
    
    if num_procesos is None:
        num_procesos = cpu_count()
    
    # OPTIMIZACIÓN: Ajustar procesos según tamaño de imagen
    pixeles_totales = (filas - 2) * (columnas - 2)
    pixeles_por_proceso = pixeles_totales / num_procesos
    
    if pixeles_por_proceso < 1000:
        num_procesos = max(1, pixeles_totales // 1000)
    
    img_bordes = np.zeros((filas, columnas), dtype=np.float32)
    
    argumentos = [(i, img_gris, columnas) for i in range(1, filas - 1)]
    
    with Pool(processes=num_procesos) as pool:
        resultados = pool.map(procesar_fila_sobel, argumentos)
    
    for i, fila_resultado in resultados:
        img_bordes[i, :] = fila_resultado
    
    max_val = np.max(img_bordes)
    if max_val > 0:
        img_bordes = (img_bordes / max_val * 255)
    
    return img_bordes.astype(np.uint8), num_procesos

# ==================== COMPARADOR ====================
def comparar_algoritmos(img_gris, nombre_prueba):
    """Compara rendimiento de ambos algoritmos"""
    print(f"\n{'='*70}")
    print(f"PRUEBA: {nombre_prueba}")
    print(f"Dimensiones: {img_gris.shape[0]}x{img_gris.shape[1]}")
    print(f"Píxeles: {img_gris.shape[0] * img_gris.shape[1]:,}")
    print(f"{'='*70}")
    
    # Ejecutar secuencial
    print("\n[1/2] Ejecutando SECUENCIAL...")
    inicio = time.time()
    img_bordes_seq = sobel_secuencial(img_gris)
    tiempo_seq = time.time() - inicio
    print(f"      ✓ Tiempo: {tiempo_seq:.4f} segundos")
    
    # Ejecutar paralelo
    print("\n[2/2] Ejecutando PARALELO...")
    inicio = time.time()
    img_bordes_par, procesos_usados = sobel_paralelo_multicore(img_gris)
    tiempo_par = time.time() - inicio
    print(f"      ✓ Tiempo: {tiempo_par:.4f} segundos")
    print(f"      ✓ Procesos utilizados: {procesos_usados}")
    
    # Calcular métricas
    speedup = tiempo_seq / tiempo_par
    eficiencia = (speedup / procesos_usados) * 100
    
    # Mostrar resultados
    print(f"\n{'─'*70}")
    print("RESULTADOS:")
    print(f"{'─'*70}")
    print(f"  Secuencial:  {tiempo_seq:.4f} seg  →  {(img_gris.size/tiempo_seq):,.0f} píxeles/seg")
    print(f"  Paralelo:    {tiempo_par:.4f} seg  →  {(img_gris.size/tiempo_par):,.0f} píxeles/seg")
    print(f"\n  📊 SPEEDUP:     {speedup:.2f}x {'✅' if speedup > 1 else '❌'}")
    print(f"  📈 EFICIENCIA:  {eficiencia:.1f}%")
    
    if speedup < 1:
        print(f"\n  ⚠️  NOTA: El paralelo es más lento debido al overhead de multiprocesamiento")
        print(f"           en imágenes pequeñas. Speedup = {speedup:.2f}x")
    
    return {
        'nombre': nombre_prueba,
        'dimension': img_gris.shape,
        'pixeles': img_gris.size,
        'tiempo_seq': tiempo_seq,
        'tiempo_par': tiempo_par,
        'speedup': speedup,
        'eficiencia': eficiencia,
        'procesos': procesos_usados
    }

def main():
    ruta_entrada = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_IMAGE
    
    print("="*70)
    print("COMPARADOR: SOBEL SECUENCIAL VS PARALELO MULTICORE")
    print("="*70)
    print(f"\nCores CPU disponibles: {cpu_count()}")
    print(f"Python: {sys.version.split()[0]}")
    
    # Cargar imagen original
    try:
        img_original = cargar_imagen(str(ruta_entrada))
        print(f"\nImagen cargada: {ruta_entrada}")
    except Exception as e:
        print(f"ERROR: {e}")
        return
    
    # Convertir a escala de grises
    img_gris_original = rgb_a_escala_grises(img_original)
    
    # Lista de resultados
    resultados = []
    
    # PRUEBA 1: Imagen original
    resultado = comparar_algoritmos(img_gris_original, "Imagen Original")
    resultados.append(resultado)
    
    # PRUEBA 2: Imagen 2x más grande
    print("\n\nRedimensionando imagen (2x)...")
    img_2x = redimensionar_imagen(img_original, 2.0)
    img_gris_2x = rgb_a_escala_grises(img_2x)
    resultado = comparar_algoritmos(img_gris_2x, "Imagen 2x")
    resultados.append(resultado)
    
    # PRUEBA 3: Imagen 4x más grande
    print("\n\nRedimensionando imagen (4x)...")
    img_4x = redimensionar_imagen(img_original, 4.0)
    img_gris_4x = rgb_a_escala_grises(img_4x)
    resultado = comparar_algoritmos(img_gris_4x, "Imagen 4x")
    resultados.append(resultado)
    
    # RESUMEN FINAL
    print("\n\n" + "="*70)
    print("RESUMEN COMPARATIVO")
    print("="*70)
    print(f"\n{'Prueba':<20} {'Píxeles':>12} {'Speedup':>10} {'Eficiencia':>12} {'Procesos':>10}")
    print("─"*70)
    
    for r in resultados:
        print(f"{r['nombre']:<20} {r['pixeles']:>12,} {r['speedup']:>9.2f}x {r['eficiencia']:>10.1f}% {r['procesos']:>10}")
    
    print("\n" + "="*70)
    print("CONCLUSIONES:")
    print("="*70)
    
    # Encontrar mejor speedup
    mejor = max(resultados, key=lambda x: x['speedup'])
    print(f"\n✓ Mejor speedup: {mejor['nombre']} con {mejor['speedup']:.2f}x")
    print(f"  → A mayor tamaño de imagen, mejor aprovechamiento del paralelismo")
    print(f"\n✓ El overhead de multiprocesamiento se amortiza con imágenes grandes")
    print(f"  → Recomendado para imágenes > 500,000 píxeles")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()

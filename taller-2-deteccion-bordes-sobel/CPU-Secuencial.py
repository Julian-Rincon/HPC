import os
import sys
import time
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
    img = Image.open(ruta)
    return np.array(img)

def rgb_a_escala_grises(img_rgb):
    """Convierte imagen RGB a escala de grises usando promedio ponderado"""
    # Fórmula estándar: 0.299*R + 0.587*G + 0.114*B
    if len(img_rgb.shape) == 3:
        return np.dot(img_rgb[...,:3], [0.299, 0.587, 0.114])
    return img_rgb

def sobel_secuencial(img_gris):
    """
    Aplica el operador Sobel de forma secuencial
    """
    filas, columnas = img_gris.shape
    
    # Kernels de Sobel
    Kx = np.array([[-1, 0, 1],
                   [-2, 0, 2],
                   [-1, 0, 1]])
    
    Ky = np.array([[-1, -2, -1],
                   [ 0,  0,  0],
                   [ 1,  2,  1]])
    
    # Imagen de salida
    img_bordes = np.zeros((filas, columnas), dtype=np.float32)
    
    # Procesar cada píxel (excepto los bordes de la imagen)
    for i in range(1, filas - 1):
        for j in range(1, columnas - 1):
            # Extraer ventana 3x3
            ventana = img_gris[i-1:i+2, j-1:j+2]
            
            # Calcular Gx (bordes verticales)
            Gx = 0.0
            for ki in range(3):
                for kj in range(3):
                    Gx += ventana[ki, kj] * Kx[ki, kj]
            
            # Calcular Gy (bordes horizontales)
            Gy = 0.0
            for ki in range(3):
                for kj in range(3):
                    Gy += ventana[ki, kj] * Ky[ki, kj]
            
            # Calcular magnitud del gradiente
            magnitud = np.sqrt(Gx**2 + Gy**2)
            img_bordes[i, j] = magnitud
    
    # Normalizar a rango 0-255
    if img_bordes.max() > 0:
        img_bordes = (img_bordes / img_bordes.max() * 255).astype(np.uint8)
    else:
        img_bordes = img_bordes.astype(np.uint8)
    
    return img_bordes

def guardar_imagen(img_array, ruta_completa):
    """Guarda el array como imagen"""
    img = Image.fromarray(img_array)
    img.save(ruta_completa)
    print(f"   Imagen guardada: {ruta_completa}")

def main():
    ruta_entrada = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_IMAGE
    RESULTS_DIR.mkdir(exist_ok=True)
    
    print("=" * 60)
    print("DETECCIÓN DE BORDES SOBEL - VERSIÓN SECUENCIAL CPU")
    print("=" * 60)
    
    # 1. Cargar imagen
    print("\n1. Cargando imagen...")
    try:
        img_original = cargar_imagen(str(ruta_entrada))
        print(f"   Ruta: {ruta_entrada}")
        print(f"   Dimensiones: {img_original.shape}")
    except FileNotFoundError as e:
        print(f"   ERROR: {e}")
        print("   Verifica que el archivo exista en la ruta indicada.")
        return
    except Exception as e:
        print(f"   ERROR al cargar imagen: {e}")
        return
    
    # 2. Convertir a escala de grises
    print("\n2. Convirtiendo a escala de grises...")
    img_gris = rgb_a_escala_grises(img_original)
    ruta_gris = RESULTS_DIR / "resultado_gris_secuencial.png"
    guardar_imagen(img_gris.astype(np.uint8), str(ruta_gris))
    
    # 3. Aplicar Sobel
    print("\n3. Aplicando algoritmo Sobel secuencial...")
    inicio = time.time()
    img_bordes = sobel_secuencial(img_gris)
    tiempo_ejecucion = time.time() - inicio
    
    # 4. Guardar resultado
    print("\n4. Guardando resultado...")
    ruta_bordes = RESULTS_DIR / "resultado_bordes_secuencial.png"
    guardar_imagen(img_bordes, str(ruta_bordes))
    
    # 5. Mostrar resultados
    print("\n" + "=" * 60)
    print("RESULTADOS")
    print("=" * 60)
    print(f"Tiempo de ejecución: {tiempo_ejecucion:.4f} segundos")
    print(f"Dimensiones imagen procesada: {img_bordes.shape}")
    print(f"Píxeles procesados: {img_bordes.shape[0] * img_bordes.shape[1]:,}")
    print(f"Throughput: {(img_bordes.shape[0] * img_bordes.shape[1])/tiempo_ejecucion:,.0f} píxeles/segundo")
    print("=" * 60)
    print("\nArchivos generados:")
    print(f"  • {ruta_gris}")
    print(f"  • {ruta_bordes}")
    print("=" * 60)

if __name__ == "__main__":
    main()

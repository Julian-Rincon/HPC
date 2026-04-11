"""
TALLER 3 - COMPARACIÓN DE RESULTADOS
Compara el rendimiento entre el algoritmo secuencial y paralelo
Calcula el speedup y genera reporte
Autor: Juan Rincón - Paula Caballero
Universidad Sergio Arboleda - Noviembre 2025
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# ================================================================
# PARÁMETROS
# ================================================================
BASE_DIR = Path(__file__).resolve().parent
archivo_secuencial = BASE_DIR / "tiempos_secuencial.txt"
archivo_paralelo = BASE_DIR / "tiempos_paralelo.txt"

# ================================================================
# FUNCIÓN: LEER TIEMPOS DE ARCHIVO
# ================================================================
def leer_tiempos(archivo):
    """
    Lee los tiempos de ejecución de un archivo de resultados
    
    Returns:
        diccionario con los tiempos
    """
    tiempos = {}
    
    with open(archivo, 'r') as f:
        for line in f:
            if "Frames procesados:" in line:
                tiempos['frames'] = int(line.split(":")[1].strip())
            elif "Núcleos utilizados:" in line:
                tiempos['nucleos'] = int(line.split(":")[1].strip())
            elif "Extracción:" in line:
                tiempos['extraccion'] = float(line.split(":")[1].replace("segundos", "").strip())
            elif "Procesamiento:" in line:
                tiempos['procesamiento'] = float(line.split(":")[1].replace("segundos", "").strip())
            elif "Creación video:" in line:
                tiempos['creacion_video'] = float(line.split(":")[1].replace("segundos", "").strip())
            elif "TOTAL:" in line:
                tiempos['total'] = float(line.split(":")[1].replace("segundos", "").strip())
            elif "Velocidad:" in line:
                tiempos['velocidad'] = float(line.split(":")[1].replace("frames/seg", "").strip())
    
    return tiempos

# ================================================================
# LEER DATOS
# ================================================================
print("=" * 70)
print("COMPARACIÓN DE ALGORITMOS - SECUENCIAL VS PARALELO")
print("=" * 70)

if not archivo_secuencial.exists():
    print(f"❌ ERROR: No se encontró {archivo_secuencial}")
    print("   Ejecuta primero video_processor_secuencial.py")
    exit(1)

if not archivo_paralelo.exists():
    print(f"❌ ERROR: No se encontró {archivo_paralelo}")
    print("   Ejecuta primero video_processor_paralelo.py")
    exit(1)

tiempos_seq = leer_tiempos(archivo_secuencial)
tiempos_par = leer_tiempos(archivo_paralelo)

print("\n✓ Archivos de tiempos cargados exitosamente")

# ================================================================
# CALCULAR SPEEDUP Y EFICIENCIA
# ================================================================
speedup_procesamiento = tiempos_seq['procesamiento'] / tiempos_par['procesamiento']
speedup_total = tiempos_seq['total'] / tiempos_par['total']

nucleos = tiempos_par.get('nucleos', 1)
eficiencia = (speedup_procesamiento / nucleos) * 100

print("\n" + "=" * 70)
print("RESULTADOS DE LA COMPARACIÓN")
print("=" * 70)

print(f"\n1. FRAMES PROCESADOS:")
print(f"   Secuencial: {tiempos_seq['frames']:,} frames")
print(f"   Paralelo:   {tiempos_par['frames']:,} frames")

print(f"\n2. TIEMPO DE PROCESAMIENTO:")
print(f"   Secuencial: {tiempos_seq['procesamiento']:.4f} segundos")
print(f"   Paralelo:   {tiempos_par['procesamiento']:.4f} segundos")
print(f"   → Diferencia: {tiempos_seq['procesamiento'] - tiempos_par['procesamiento']:.4f} segundos")

print(f"\n3. TIEMPO TOTAL:")
print(f"   Secuencial: {tiempos_seq['total']:.4f} segundos")
print(f"   Paralelo:   {tiempos_par['total']:.4f} segundos")
print(f"   → Diferencia: {tiempos_seq['total'] - tiempos_par['total']:.4f} segundos")

print(f"\n4. SPEEDUP (ACELERACIÓN):")
print(f"   Speedup (procesamiento): {speedup_procesamiento:.4f}x")
print(f"   Speedup (total):         {speedup_total:.4f}x")

print(f"\n5. EFICIENCIA:")
print(f"   Núcleos utilizados: {nucleos}")
print(f"   Eficiencia: {eficiencia:.2f}%")

print(f"\n6. VELOCIDAD DE PROCESAMIENTO:")
print(f"   Secuencial: {tiempos_seq['velocidad']:.2f} frames/seg")
print(f"   Paralelo:   {tiempos_par['velocidad']:.2f} frames/seg")
print(f"   → Mejora: {tiempos_par['velocidad'] - tiempos_seq['velocidad']:.2f} frames/seg")

# ================================================================
# GENERAR GRÁFICAS
# ================================================================
print("\n" + "=" * 70)
print("GENERANDO GRÁFICAS...")
print("=" * 70)

# Crear figura con múltiples subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Comparación: Algoritmo Secuencial vs Paralelo', fontsize=16, fontweight='bold')

# Gráfica 1: Tiempo de Procesamiento
ax1 = axes[0, 0]
categorias = ['Secuencial', 'Paralelo']
tiempos_proc = [tiempos_seq['procesamiento'], tiempos_par['procesamiento']]
colores = ['#FF6B6B', '#4ECDC4']
bars1 = ax1.bar(categorias, tiempos_proc, color=colores, alpha=0.8, edgecolor='black')
ax1.set_ylabel('Tiempo (segundos)', fontweight='bold')
ax1.set_title('Tiempo de Procesamiento', fontweight='bold')
ax1.grid(axis='y', alpha=0.3)

# Añadir valores en las barras
for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.2f}s', ha='center', va='bottom', fontweight='bold')

# Gráfica 2: Tiempo Total
ax2 = axes[0, 1]
tiempos_totales = [tiempos_seq['total'], tiempos_par['total']]
bars2 = ax2.bar(categorias, tiempos_totales, color=colores, alpha=0.8, edgecolor='black')
ax2.set_ylabel('Tiempo (segundos)', fontweight='bold')
ax2.set_title('Tiempo Total de Ejecución', fontweight='bold')
ax2.grid(axis='y', alpha=0.3)

for bar in bars2:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.2f}s', ha='center', va='bottom', fontweight='bold')

# Gráfica 3: Speedup
ax3 = axes[1, 0]
speedups = ['Procesamiento', 'Total']
speedup_valores = [speedup_procesamiento, speedup_total]
bars3 = ax3.bar(speedups, speedup_valores, color='#95E1D3', alpha=0.8, edgecolor='black')
ax3.axhline(y=1, color='red', linestyle='--', label='Sin aceleración', linewidth=2)
ax3.set_ylabel('Speedup (x veces)', fontweight='bold')
ax3.set_title('Speedup (Aceleración)', fontweight='bold')
ax3.legend()
ax3.grid(axis='y', alpha=0.3)

for bar in bars3:
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.2f}x', ha='center', va='bottom', fontweight='bold')

# Gráfica 4: Velocidad de procesamiento
ax4 = axes[1, 1]
velocidades = [tiempos_seq['velocidad'], tiempos_par['velocidad']]
bars4 = ax4.bar(categorias, velocidades, color=colores, alpha=0.8, edgecolor='black')
ax4.set_ylabel('Frames por segundo', fontweight='bold')
ax4.set_title('Velocidad de Procesamiento', fontweight='bold')
ax4.grid(axis='y', alpha=0.3)

for bar in bars4:
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.1f} fps', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()

# Guardar gráfica
grafica_path = os.path.join(BASE_DIR, "comparacion_resultados.png")
plt.savefig(grafica_path, dpi=300, bbox_inches='tight')
print(f"✓ Gráfica guardada en: {grafica_path}")

# ================================================================
# GENERAR REPORTE COMPLETO
# ================================================================
reporte_path = os.path.join(BASE_DIR, "reporte_comparacion.txt")

with open(reporte_path, 'w', encoding='utf-8') as f:
    f.write("=" * 70 + "\n")
    f.write("REPORTE DE COMPARACIÓN - PROCESAMIENTO DE VIDEO\n")
    f.write("Secuencial vs Paralelo\n")
    f.write("=" * 70 + "\n\n")
    
    f.write("1. CONFIGURACIÓN\n")
    f.write(f"   Frames procesados: {tiempos_seq['frames']:,}\n")
    f.write(f"   Núcleos utilizados (paralelo): {nucleos}\n\n")
    
    f.write("2. TIEMPOS DE EJECUCIÓN\n")
    f.write(f"   a) Extracción de frames:\n")
    f.write(f"      Secuencial: {tiempos_seq['extraccion']:.4f} seg\n")
    f.write(f"      Paralelo:   {tiempos_par['extraccion']:.4f} seg\n\n")
    
    f.write(f"   b) Procesamiento (conversión a escala de grises):\n")
    f.write(f"      Secuencial: {tiempos_seq['procesamiento']:.4f} seg\n")
    f.write(f"      Paralelo:   {tiempos_par['procesamiento']:.4f} seg\n")
    f.write(f"      Diferencia: {tiempos_seq['procesamiento'] - tiempos_par['procesamiento']:.4f} seg\n\n")
    
    f.write(f"   c) Creación de video:\n")
    f.write(f"      Secuencial: {tiempos_seq['creacion_video']:.4f} seg\n")
    f.write(f"      Paralelo:   {tiempos_par['creacion_video']:.4f} seg\n\n")
    
    f.write(f"   d) Tiempo total:\n")
    f.write(f"      Secuencial: {tiempos_seq['total']:.4f} seg\n")
    f.write(f"      Paralelo:   {tiempos_par['total']:.4f} seg\n")
    f.write(f"      Diferencia: {tiempos_seq['total'] - tiempos_par['total']:.4f} seg\n\n")
    
    f.write("3. MÉTRICAS DE RENDIMIENTO\n")
    f.write(f"   a) Speedup (Aceleración):\n")
    f.write(f"      Procesamiento: {speedup_procesamiento:.4f}x\n")
    f.write(f"      Total:         {speedup_total:.4f}x\n\n")
    
    f.write(f"   b) Eficiencia:\n")
    f.write(f"      {eficiencia:.2f}%\n\n")
    
    f.write(f"   c) Velocidad de procesamiento:\n")
    f.write(f"      Secuencial: {tiempos_seq['velocidad']:.2f} frames/seg\n")
    f.write(f"      Paralelo:   {tiempos_par['velocidad']:.2f} frames/seg\n")
    f.write(f"      Mejora:     {tiempos_par['velocidad'] - tiempos_seq['velocidad']:.2f} frames/seg\n\n")
    
    f.write("4. CONCLUSIONES\n")
    f.write(f"   • El algoritmo paralelo es {speedup_procesamiento:.2f}x más rápido en procesamiento\n")
    f.write(f"   • Se logró una eficiencia de {eficiencia:.2f}% con {nucleos} núcleos\n")
    f.write(f"   • Tiempo ahorrado: {tiempos_seq['total'] - tiempos_par['total']:.2f} segundos\n")
    
    porcentaje_mejora = ((tiempos_seq['total'] - tiempos_par['total']) / tiempos_seq['total']) * 100
    f.write(f"   • Mejora del {porcentaje_mejora:.2f}% en tiempo total\n")

print(f"✓ Reporte completo guardado en: {reporte_path}")

print("\n" + "=" * 70)
print("¡COMPARACIÓN COMPLETADA!")
print("=" * 70)
print(f"\nArchivos generados:")
print(f"  1. {grafica_path}")
print(f"  2. {reporte_path}")
print("\nPuedes usar estos archivos en tu informe de laboratorio.")
print("=" * 70)

# Mostrar gráfica
plt.show()

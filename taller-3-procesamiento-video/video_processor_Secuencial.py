"""
TALLER 3 - PROCESAMIENTO DE VIDEO SECUENCIAL
Transformación de video a color a escala de grises usando procesamiento secuencial.
"""

import shutil
import sys
import time
from pathlib import Path

import cv2
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_VIDEO_INPUT_PATH = BASE_DIR / "20 PLANTILLAS de MEMES para videos.mp4"
FOLDER_FRAMES_ORIGINAL = BASE_DIR / "frames_video_original"
FOLDER_FRAMES_RESULT = BASE_DIR / "frames_video_result_secuencial"
VIDEO_RESULT_FPS = 30
VIDEO_OUTPUT_NAME = "video_result_secuencial.mp4"


def convert_to_grayscale_sequential(bgr_image):
    """Convierte una imagen BGR a escala de grises de forma secuencial."""
    height, width = bgr_image.shape[:2]

    gray_img_float = [
        [
            0.30 * bgr_image[row][col][2]
            + 0.59 * bgr_image[row][col][1]
            + 0.11 * bgr_image[row][col][0]
            for col in range(width)
        ]
        for row in range(height)
    ]

    return np.array(gray_img_float).astype(np.uint8)


def reset_folder(path):
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def main():
    video_input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_VIDEO_INPUT_PATH
    tiempos = {}

    print("=" * 70)
    print("PROCESAMIENTO DE VIDEO SECUENCIAL - CONVERSIÓN A ESCALA DE GRISES")
    print("=" * 70)

    tiempo_inicio_total = time.time()

    print("\n" + "=" * 70)
    print("PASO 1: Limpiando ambiente...")
    print("=" * 70)
    reset_folder(FOLDER_FRAMES_ORIGINAL)
    reset_folder(FOLDER_FRAMES_RESULT)
    print("✓ Carpetas creadas exitosamente")

    print("\n" + "=" * 70)
    print("PASO 2: Cargando video...")
    print("=" * 70)

    if not video_input_path.exists():
        print(f"❌ ERROR: No se encontró el video en: {video_input_path}")
        sys.exit(1)

    cap = cv2.VideoCapture(str(video_input_path))
    if not cap.isOpened():
        print("❌ ERROR: No se pudo abrir el video")
        sys.exit(1)

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = total_frames / fps if fps > 0 else 0

    print("✓ Video cargado exitosamente")
    print(f"  - Resolución: {width}x{height}")
    print(f"  - FPS: {fps:.2f}")
    print(f"  - Frames totales: {total_frames:,}")
    print(f"  - Duración: {duration:.2f} segundos")

    print("\n" + "=" * 70)
    print("PASO 3: Extrayendo frames del video...")
    print("=" * 70)

    tiempo_inicio_extraccion = time.time()
    seconds_interval = 1 / VIDEO_RESULT_FPS
    step = max(1, int(fps * seconds_interval))

    print(f"  Intervalo de muestreo: {seconds_interval:.4f} segundos")
    print(f"  Step (cada cuántos frames): {step}")

    frame_idx = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % step == 0:
            output_path = FOLDER_FRAMES_ORIGINAL / f"frame_{saved_count:09d}.jpg"
            cv2.imwrite(str(output_path), frame)
            saved_count += 1

            if saved_count % 100 == 0:
                print(f"  Extraídos: {saved_count} frames...")

        frame_idx += 1

    cap.release()

    tiempo_extraccion = time.time() - tiempo_inicio_extraccion
    tiempos["extraccion"] = tiempo_extraccion

    print(f"✓ Extracción completada en {tiempo_extraccion:.2f} segundos")
    print(f"✓ Total de frames guardados: {saved_count:,}")

    print("\n" + "=" * 70)
    print("PASO 4: Convirtiendo imágenes a escala de grises (SECUENCIAL)...")
    print("=" * 70)

    tiempo_inicio_procesamiento = time.time()

    for i in range(saved_count):
        filename = f"frame_{i:09d}.jpg"
        file_path = FOLDER_FRAMES_ORIGINAL / filename

        if file_path.exists():
            bgr_image = cv2.imread(str(file_path))
            imagen_gray = convert_to_grayscale_sequential(bgr_image)
            output_path = FOLDER_FRAMES_RESULT / filename
            cv2.imwrite(str(output_path), imagen_gray)

            if (i + 1) % 100 == 0:
                print(f"  Procesados: {i + 1}/{saved_count} frames...")
        else:
            print(f"⚠️ Advertencia: No se encontró {filename}")

    tiempo_procesamiento = time.time() - tiempo_inicio_procesamiento
    tiempos["procesamiento"] = tiempo_procesamiento

    print(f"✓ Procesamiento completado en {tiempo_procesamiento:.2f} segundos")
    print(f"✓ Velocidad: {saved_count/tiempo_procesamiento:.2f} frames/segundo")

    print("\n" + "=" * 70)
    print("PASO 5: Creando video resultado...")
    print("=" * 70)

    tiempo_inicio_video = time.time()
    first_frame_path = FOLDER_FRAMES_RESULT / "frame_000000000.jpg"

    if not first_frame_path.exists():
        print("❌ ERROR: No se encontró el primer frame procesado")
        sys.exit(1)

    frame = cv2.imread(str(first_frame_path))
    height, width = frame.shape[:2]
    frame_size = (width, height)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video_output_path = BASE_DIR / VIDEO_OUTPUT_NAME
    video = cv2.VideoWriter(str(video_output_path), fourcc, VIDEO_RESULT_FPS, frame_size)

    for i in range(saved_count):
        filename = f"frame_{i:09d}.jpg"
        file_path = FOLDER_FRAMES_RESULT / filename
        img = cv2.imread(str(file_path))

        if img is not None:
            video.write(img)

            if (i + 1) % 100 == 0:
                print(f"  Escritos: {i + 1}/{saved_count} frames...")
        else:
            print(f"⚠️ Advertencia: No se pudo cargar {filename}")

    video.release()

    tiempo_video = time.time() - tiempo_inicio_video
    tiempos["creacion_video"] = tiempo_video

    print(f"✓ Video creado en {tiempo_video:.2f} segundos")

    tiempo_total = time.time() - tiempo_inicio_total
    tiempos["total"] = tiempo_total

    print("\n" + "=" * 70)
    print("RESUMEN DE EJECUCIÓN - ALGORITMO SECUENCIAL")
    print("=" * 70)
    print(f"Video de entrada: {video_input_path}")
    print(f"Video de salida: {video_output_path}")
    print(f"Frames procesados: {saved_count}")
    print("\nRESUMEN DE TIEMPOS:")
    print(f"  - Extracción de frames:       {tiempos['extraccion']:.2f} seg")
    print(f"  - Procesamiento secuencial:   {tiempos['procesamiento']:.2f} seg")
    print(f"  - Creación de video:          {tiempos['creacion_video']:.2f} seg")
    print(f"  - TIEMPO TOTAL:               {tiempos['total']:.2f} seg")
    print(f"\nVelocidad de procesamiento: {saved_count/tiempos['procesamiento']:.2f} frames/seg")
    print("=" * 70)

    tiempos_file = BASE_DIR / "tiempos_secuencial.txt"
    with tiempos_file.open("w", encoding="utf-8") as f:
        f.write("TIEMPOS DE EJECUCIÓN - ALGORITMO SECUENCIAL\n")
        f.write("=" * 50 + "\n")
        f.write(f"Frames procesados: {saved_count}\n")
        f.write(f"Extracción: {tiempos['extraccion']:.4f} segundos\n")
        f.write(f"Procesamiento: {tiempos['procesamiento']:.4f} segundos\n")
        f.write(f"Creación video: {tiempos['creacion_video']:.4f} segundos\n")
        f.write(f"TOTAL: {tiempos['total']:.4f} segundos\n")
        f.write(f"Velocidad: {saved_count/tiempos['procesamiento']:.4f} frames/seg\n")

    print(f"\n✓ Tiempos guardados en: {tiempos_file}")


if __name__ == "__main__":
    main()

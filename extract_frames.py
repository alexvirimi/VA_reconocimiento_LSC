# Este archivo toma una captura de pantalla de cada video en la carpeta "static/videos/abecedario" cada 40 frames 
# y las guarda en la carpeta "data" con subcarpetas para cada etiqueta.

import cv2
import os
from tqdm import tqdm  # Barra de progreso visual en consola

videos_path = "static/videos/abecedario"
output_path = "data"
frames_per_video = 40  # Se pueden ajustar según necesidad

os.makedirs(output_path, exist_ok=True)  # Crea la carpeta de salida si no existe

# Lista todos los archivos .mp4 en la carpeta de videos
video_files = [f for f in os.listdir(videos_path) if f.lower().endswith(".mp4")]
if not video_files:
    print("No hay videos en 'static/videos/abecedario'. Coloca tus .mp4 allí.")
    exit(1)

# Recorre cada video encontrado
for vf in video_files:
    label = os.path.splitext(vf)[0]  # Usa el nombre del video como etiqueta
    cap = cv2.VideoCapture(os.path.join(videos_path, vf))  # Abre el video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Obtiene la cantidad total de frames
    
    if total_frames == 0:
        print(f"[WARN] {vf} no tiene frames o no se pudo leer.")
        cap.release()
        continue

    # Calcula cada cuántos frames guardar una imagen
    step = max(1, total_frames // frames_per_video)
    out_dir = os.path.join(output_path, label)
    os.makedirs(out_dir, exist_ok=True)  # Crea carpeta específica para la etiqueta

    saved = 0
    frame_idx = 0
    pbar = tqdm(total=min(frames_per_video, total_frames), desc=f"Extrayendo {label}")
    
    # Recorre los frames del video
    while saved < frames_per_video and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Guarda solo los frames seleccionados según el paso calculado
        if frame_idx % step == 0:
            fname = os.path.join(out_dir, f"{label}_{saved:03d}.jpg")
            cv2.imwrite(fname, frame)  # Guarda el frame como imagen
            saved += 1
            pbar.update(1)
        frame_idx += 1

    pbar.close()
    cap.release()
    print(f"{vf} -> guardados {saved} frames en {out_dir}")

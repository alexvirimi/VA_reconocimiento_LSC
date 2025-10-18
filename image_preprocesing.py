# Este archivo procesa las imágenes extraídas en "data/", redimensionándolas, normalizándolas y aplicando aumentos de datos simples.
# Las imágenes procesadas se guardan en "processed_data/" con la misma estructura de carpetas.
# Cuando se habla de dimensionar se refiere a tomar un frame y volverlo de un tamaño a otro.
# Para normalizar es rotar la imagen
# Para aumento de datos la imagen se pone mas brillante

import cv2
import os
import numpy as np
from tqdm import tqdm  # Barra de progreso visual

input_path = "data"
output_path = "data/processed_data"
img_size = (224, 224)  # Tamaño estándar para los modelos de visión

os.makedirs(output_path, exist_ok=True)  # Crea la carpeta de salida si no existe

# Lista las subcarpetas dentro de "data" (una por cada etiqueta)
labels = [d for d in os.listdir(input_path) if os.path.isdir(os.path.join(input_path, d))]
if not labels:
    print("No hay carpetas en data/. Ejecuta extract_frames.py primero.")
    exit(1)

# Procesa cada carpeta (una por letra o clase)
for label in labels:
    in_dir = os.path.join(input_path, label)
    out_dir = os.path.join(output_path, label)
    os.makedirs(out_dir, exist_ok=True)

    files = [f for f in os.listdir(in_dir) if f.lower().endswith((".jpg", ".png"))]

    for f in tqdm(files, desc=f"Procesando {label}"):
        img = cv2.imread(os.path.join(in_dir, f))
        if img is None:
            continue

        # 1️ Redimensionar (cambiar tamaño de cada imagen)
        img_resized = cv2.resize(img, img_size)

        # Guarda la imagen redimensionada
        save_name = os.path.join(out_dir, f)
        cv2.imwrite(save_name, img_resized)

        # 2️ Aumento de datos 1: voltear horizontalmente (espejo)
        flipped = cv2.flip(img_resized, 1)
        base, ext = os.path.splitext(f)
        cv2.imwrite(os.path.join(out_dir, f"{base}_flip{ext}"), flipped)

        # 3️ Aumento de datos 2: incrementar brillo
        hsv = cv2.cvtColor(img_resized, cv2.COLOR_BGR2HSV)  # Cambia a espacio HSV
        h, s, v = cv2.split(hsv)
        v = cv2.add(v, 15)  # Sube el brillo un poco
        v = np.clip(v, 0, 255)
        hsv2 = cv2.merge([h, s, v])
        bright = cv2.cvtColor(hsv2, cv2.COLOR_HSV2BGR)  # Regresa a BGR
        cv2.imwrite(os.path.join(out_dir, f"{base}_bright{ext}"), bright)

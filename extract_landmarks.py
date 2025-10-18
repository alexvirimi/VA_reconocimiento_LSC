# Usa los modelos de MediaPipe para extraer los puntos clave de las manos y guardarlos en un CSV, que luego usara el modelo de reconocimiento.
# Esto se logra con los resultados del archivo image_preprocesing.py
import mediapipe as mp
import cv2
import os
import csv
from tqdm import tqdm
import numpy as np

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5)

input_path = "processed_data"
output_csv = "landmarks.csv"

labels = [d for d in os.listdir(input_path) if os.path.isdir(os.path.join(input_path, d))]
if not labels:
    print("No hay processed_data/. Ejecuta preprocess_images.py primero.")
    exit(1)

header = []
for i in range(1, 22):  # 21 puntos
    header += [f"x{i}", f"y{i}", f"z{i}"]
header += ["label", "image_path"]

with open(output_csv, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    for label in labels:
        image_files = [f for f in os.listdir(os.path.join(input_path, label)) if f.lower().endswith((".jpg", ".png"))]
        for im_file in tqdm(image_files, desc=f"Landmarks {label}"):
            im_path = os.path.join(input_path, label, im_file)
            img = cv2.imread(im_path)
            if img is None:
                continue
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(img_rgb)
            if not results.multi_hand_landmarks:
                # Si no detecta mano, escribimos NaNs (o podemos saltar)
                row = [np.nan] * (21*3) + [label, im_path]
                writer.writerow(row)
                continue
            lm = results.multi_hand_landmarks[0]
            h, w, _ = img.shape
            flattened = []
            for lmpt in lm.landmark:
                flattened += [lmpt.x, lmpt.y, lmpt.z]
            writer.writerow(flattened + [label, im_path])

hands.close()
print(f"Landmarks guardados en {output_csv}")

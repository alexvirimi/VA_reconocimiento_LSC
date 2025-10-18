# Se prepara un dataset dividiéndolo en conjuntos de entrenamiento, validación y prueba.
# Usa el CSV generado en extract_landmarks.py, y guarda sus divisiones en "dataset_splits/".

import pandas as pd
import os
from sklearn.model_selection import train_test_split
import shutil

csv_in = "landmarks.csv"
df = pd.read_csv(csv_in)

# Elimina filas sin detección de mano (valores NaN)
df_clean = df.dropna().reset_index(drop=True)
print(f"Total con landmarks detectados: {len(df_clean)} (de {len(df)})")

# Se divide el dataset en entrenamiento (80%), validación (10%) y prueba (10%)
# La división es estratificada, manteniendo la proporción de etiquetas.
train, temp = train_test_split(df_clean, test_size=0.2, stratify=df_clean['label'], random_state=42)
val, test = train_test_split(temp, test_size=0.5, stratify=temp['label'], random_state=42)

# Crea carpeta para guardar los CSVs resultantes
os.makedirs("dataset_splits", exist_ok=True)
train.to_csv("dataset_splits/train.csv", index=False)
val.to_csv("dataset_splits/val.csv", index=False)
test.to_csv("dataset_splits/test.csv", index=False)
print("CSV guardados en dataset_splits/")

# Copia opcional de las imágenes a carpetas separadas por conjunto (entrenamiento, validación, prueba)
copy_images = True
if copy_images:
    for split_name, df_split in [("train", train), ("val", val), ("test", test)]:
        out_dir = os.path.join("dataset_images", split_name)
        os.makedirs(out_dir, exist_ok=True)
        for _, row in df_split.iterrows():
            src = row['image_path']
            label = row['label']
            label_dir = os.path.join(out_dir, label)
            os.makedirs(label_dir, exist_ok=True)
            dst = os.path.join(label_dir, os.path.basename(src))
            try:
                shutil.copy(src, dst)
            except Exception as e:
                print(f"[WARN] no se pudo copiar {src}: {e}")

print("Imágenes copiadas a dataset_images/")

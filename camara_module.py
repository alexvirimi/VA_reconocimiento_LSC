#Este módulo procesa videos para extraer keypoints utilizando MediaPipe Holistic y guarda los datos en archivos .npy.
#Este codigo funciona como reemplazo de collect_images.py para videos.

import os
import cv2
import numpy as np
import mediapipe as mp

# --- Inicialización de MediaPipe ---
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils


# --- Función para detección ---
def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = model.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image, results


# --- Función para extraer keypoints ---
def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] 
                     for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
    face = np.array([[res.x, res.y, res.z] 
                     for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
    lh = np.array([[res.x, res.y, res.z] 
                   for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] 
                   for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([pose, face, lh, rh])


#  Parámetros principales 
VIDEO_PATH = os.path.join('static', 'videos', 'abecedario')
DATA_PATH = os.path.join('MP_Data')

# Lista de acciones según los videos
actions = np.array(['a', 'b', 'c', 'd', 'e'])
no_sequences = 30        # número máximo de secuencias por acción
sequence_length = 30     # frames por video
start_folder = 0


#  Crear estructura de carpetas 
for action in actions:
    for sequence in range(start_folder, start_folder + no_sequences):
        os.makedirs(os.path.join(DATA_PATH, action, str(sequence)), exist_ok=True)


#  Procesamiento de videos 
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    for action in actions:
        video_files = [f for f in os.listdir(VIDEO_PATH) if f.startswith(action)]
        for sequence, video_file in enumerate(video_files):
            if sequence >= no_sequences:
                break

            video_path = os.path.join(VIDEO_PATH, video_file)
            cap = cv2.VideoCapture(video_path)
            frame_num = 0

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret or frame_num >= sequence_length:
                    break

                # Detección y extracción de keypoints
                image, results = mediapipe_detection(frame, holistic)
                keypoints = extract_keypoints(results)

                # Guardar en archivo .npy
                np.save(os.path.join(DATA_PATH, action, str(sequence), str(frame_num)), keypoints)

                frame_num += 1

            cap.release()

cv2.destroyAllWindows()
print("Extracción completada. Keypoints guardados en MP_Data/")
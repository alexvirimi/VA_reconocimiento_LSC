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


# --- Rutas principales ---
VIDEO_PATH = os.path.join('static', 'videos', 'abecedario')
DATA_PATH = os.path.join('MP_Data')

# --- Acciones según tus videos ---
actions = np.array([
    'a', 'b', 'c', 'd', 'e', 'enie', 'f', 'i', 'k', 'l', 'm', 
    'n', 'o', 'p', 'q', 'r', 't', 'u', 'v', 'w'
])

sequence_length = 30  # Frames por video, se puede ajustar según necesidad


# --- Crear carpetas por acción ---
for action in actions:
    os.makedirs(os.path.join(DATA_PATH, action, '0'), exist_ok=True)


# --- Procesamiento de videos ---
with mp_holistic.Holistic(min_detection_confidence=0.5, 
                          min_tracking_confidence=0.5) as holistic:
    for action in actions:
        video_file = f"{action}.mp4"
        video_path = os.path.join(VIDEO_PATH, video_file)

        if not os.path.exists(video_path):
            print(f"Video no encontrado: {video_file}")
            continue

        cap = cv2.VideoCapture(video_path)
        frame_num = 0

        print(f"Procesando {video_file}...")

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret or frame_num >= sequence_length:
                break

            # Detección y extracción
            image, results = mediapipe_detection(frame, holistic)
            keypoints = extract_keypoints(results)

            # Guardar como .npy
            np.save(os.path.join(DATA_PATH, action, '0', str(frame_num)), keypoints)
            frame_num += 1

        cap.release()
        print(f" {action}: {frame_num} frames procesados y guardados.")

cv2.destroyAllWindows()
print("Extracción completada. Los keypoints están en MP_Data/")

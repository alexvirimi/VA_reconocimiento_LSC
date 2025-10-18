# Captura imágenes con la webcam para crear el dataset base

import os
import cv2

# Ruta principal donde se almacenarán las imágenes recolectadas
DATA_PATH = './data'

# Crear la carpeta principal si no existe
if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)

# Letras del abecedario que se capturarán (puedes ampliar esta lista)
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'i', 'k', 'l', 'm',
             'n', 'o', 'p', 'q', 'r', 't', 'u', 'v', 'w', 'x', 'y']

# Cantidad de imágenes que se recolectarán por clase (por letra)
dataset_size = 100

# Inicializar la cámara (0 = cámara principal del laptop)
cap = cv2.VideoCapture(0)

# Recorrer cada letra definida
for letter in alphabet:
    # Crear carpeta para la letra si no existe
    letter_dir = os.path.join(DATA_PATH, letter)
    if not os.path.exists(letter_dir):
        os.makedirs(letter_dir)

    # Contar imágenes existentes para evitar duplicar
    existing_imgs = len([img for img in os.listdir(letter_dir) if img.endswith('.jpg')])
    if existing_imgs >= dataset_size:
        print(f'Se han recolectado suficientes imágenes para la letra {letter}. Saltando...')
        continue

    print(f'Recolectando imágenes para la letra {letter} (faltan {dataset_size - existing_imgs})')

    # Mostrar instrucciones hasta que el usuario presione "S" (start)
    while True:
        ret, frame = cap.read()
        cv2.putText(frame, 'Listo? Presiona "S" :)', (110, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 3, cv2.LINE_AA)
        cv2.putText(frame, 'Para salir presiona "Q"', (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 3, cv2.LINE_AA)
        cv2.imshow('frame', frame)
        key = cv2.waitKey(25)

        # Comenzar captura si se presiona "S"
        if key == ord('s') or key == ord('S'):
            break
        # Salir del programa si se presiona "Q"
        if key == ord('q') or key == ord('Q'):
            cap.release()
            cv2.destroyAllWindows()
            exit()

    # Capturar 100 imágenes seguidas por letra
    for counter in range(0, dataset_size):
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        cv2.waitKey(25)
        cv2.imwrite(os.path.join(DATA_PATH, letter, '{}.jpg'.format(counter)), frame)

# Liberar cámara y cerrar ventanas
cap.release()
cv2.destroyAllWindows()

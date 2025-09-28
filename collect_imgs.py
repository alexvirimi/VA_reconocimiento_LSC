# Collect_imgs
import os
import cv2

DATA_PATH = './data'
# Create data directory if it doesn't exist
if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'i', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 't', 'u', 'v', 'w', 'x', 'y']
# Number of images to collect per class
dataset_size = 100

# Initialize webcam of laptop
cap = cv2.VideoCapture(0)
# For each class create a subdirectory
for letter in alphabet:
    # If the subdirectory doesn't exist create it
    letter_dir = os.path.join(DATA_PATH, letter)
    if not os.path.exists(letter_dir):
        os.makedirs(letter_dir)

    # Count how many images already exist for this letter
    existing_imgs = len([img for img in os.listdir(letter_dir) if img.endswith('.jpg')])
    if existing_imgs >= dataset_size:
        print(f'Se han recolectado suficientes imágenes para la letra {letter}. Saltando...')
        continue

    print(f'Recolectando imagenes para la letra {letter} (faltan {dataset_size - existing_imgs})')

    # Read frames from the webcam
    while True:
        # Get current frame
        ret, frame = cap.read()
        # Put text on the frame
        cv2.putText(frame, 'Listo? Presiona "S" :)', (110, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 3,
                    cv2.LINE_AA)
        cv2.putText(frame, 'Para salir presiona "Q"', (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 3,
                    cv2.LINE_AA)
        cv2.imshow('frame', frame)
        key = cv2.waitKey(25)
        # If pressed 's' or 'S' start collecting images
        if key == ord('s') or key == ord('S'):
            break
        # If pressed 'q' or 'Q' exit the program
        if key == ord('q') or key == ord('Q'):
            cap.release()
            cv2.destroyAllWindows()
            exit()

    for counter in range(0, dataset_size):
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        cv2.waitKey(25)
        cv2.imwrite(os.path.join(DATA_PATH, letter, '{}.jpg'.format(counter)), frame)

cap.release()
cv2.destroyAllWindows()
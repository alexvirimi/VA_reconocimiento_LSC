# Collect_imgs
import os
import cv2

DATA_PATH = './data'
# Create data directory if it doesn't exist
if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)

# Agregar todo el vocabulario, todas las acciones a guardar
# https://youtu.be/q8j1aXIRCv8?list=PLI7rDimYXOdhyty-lEXsxQgiLfYKnnqmY
vocabulary = ['g', 'h', 'j', 'ñ', 's', 'z', 'sordo', 'hola', 'como estas', 'bien', 'mal', 'mas o menos', 'buenos dias', 'buenas tardes', 'buenas noches', 'adios', 
              'gracias', 'con gusto', 'por favor', 'perdon', 'permiso', 'si', 'no', 'lo siento']
# Number of videos to collect per class
dataset_size = 40
# Length of each video (in number of frames)
sequence_length = 50

# Initialize webcam of laptop
cap = cv2.VideoCapture(0)
# For each class create a subdirectory
for word in vocabulary:
    for sequence in range(0, dataset_size):
        # If the subdirectory for the word doesn't exist create it
        word_dir = os.path.join(DATA_PATH, word)
        if not os.path.exists(word_dir):
            os.makedirs(word_dir)

        # Make sure a subdirectory for each video doesn't exist
        video_dir = os.path.join(word_dir, str(sequence))
        if os.path.exists(video_dir):
            print(f'El video {sequence} para {word} ya existe. Saltando...')
            continue

        print(f'Recolectando videos para {word} (video {sequence})')

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

        # Crear el subdirectorio solo cuando se va a guardar frames
        os.makedirs(video_dir)
                                                 
        # Save frames for each video
        for counter in range(0, sequence_length):
            ret, frame = cap.read()
            cv2.putText(frame, 'Recolectando frames para {} Video #{}'.format(word, sequence), (15,20), 
                                cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.imshow('frame', frame)
            cv2.waitKey(25)
            cv2.imwrite(os.path.join(video_dir, '{}.jpg'.format(counter)), frame)

cap.release()
cv2.destroyAllWindows()
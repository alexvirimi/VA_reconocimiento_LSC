import tensorflow as tf
import cv2
import mediapipe as mp
import os
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
import numpy as np
import time


mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = model.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image, results

def draw_landmarks(image, results):
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_face_mesh.FACEMESH_TESSELATION)
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

def draw_styled_landmarks(image, results):

    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_face_mesh.FACEMESH_TESSELATION,
                             mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
                             mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
    )
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                             mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
                             mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                             )

    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                             mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4),
                             mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
                             )

    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                             mp_drawing.DrawingSpec(color=(80,110,10), thickness=2, circle_radius=4),
                             mp_drawing.DrawingSpec(color=(80,256,121), thickness=2, circle_radius=2)
                             )


def main():
    DATA_VIDEO_PATH = './static/videos'

    abcdario = np.array(['a', 'b', 'c', 'd', 'e', 'f', 'g',
                         'h', 'i', 'j', 'k', 'l', 'elle', 'm', 
                         'n', 'enie', 'o', 'p', 'q', 'r', 's', 
                         't', 'u', 'v', 'y', 'z'])
    
    # Thirty videos worth of data
    no_sequences = 30

    # Videos are going to be 30 frames in length
    sequence_length = 30

    # Folder start
    start_folder = 30
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:

        for letter in abcdario:
            
            letter_dir = os.path.join(DATA_VIDEO_PATH, 'abecedario', letter + '.mp4')
            print(letter_dir)
            if not os.path.exists(letter_dir):
                print('not exist')
                continue

            cap = cv2.VideoCapture(letter_dir)
            image_array = []
            stop_sequence = False

            for sequence in range(start_folder, start_folder+no_sequences):
                
                if stop_sequence: break

                for frame_num in range(sequence_length):
                    # Read feed
                    ret, frame = cap.read()
                    image_array.append(frame)

                    if ret == True:
                        # Make detections
                        image, results = mediapipe_detection(frame, holistic)
                        # print(results)
                        
                        # Draw landmarks
                        draw_styled_landmarks(image, results)
                    else:
                        print(f'Letter {letter} has {sequence - no_sequences} sequences')
                        print(f'Last sequence had {frame_num + 1} frames')
                        stop_sequence = True
                        break

                    # Show to screen
                    if frame_num == 0:
                        cv2.putText(image, 'STARTING COLLECTION', (120,200), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255, 0), 4, cv2.LINE_AA)
                        cv2.putText(image, 'Collecting frames for {} Video Number {}'.format(letter, sequence), (15,12), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                        # Show to screen
                        cv2.imshow('OpenCV Feed', image)
                        cv2.waitKey(500)
                    else: 
                        cv2.putText(image, 'Collecting frames for {} Video Number {}'.format(letter, sequence), (15,12), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                        # Show to screen
                        cv2.imshow('OpenCV Feed', image)

                    # NO USEN ESTO! NO LE DEN A A LA Q!
                    # SIN ESTO NO SE MUESTRA EL VIDEO
                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        break
                
            cap.release()
            cv2.destroyAllWindows()
            print(f'Letter {letter} has {len(image_array)} frames')


if __name__ == '__main__':
    main()
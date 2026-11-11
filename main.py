import cv2
import mediapipe as mp
import pygame
import speech_recognition as sr
import threading
import random
import numpy as np

#musik

pygame.mixer.init()

try:
    pygame.mixer.music.load("Geburtstag_musik.mp3")
except Exception as e:
    print("Music error:", e)

#Camera

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not found")
    exit()

ret, frame = cap.read()

if not ret:
    print("Cannot access camera")
    exit()

h, w, _ = frame.shape

#Hand_detection

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)


birthday_triggered = False
captured_frame = None

#Voice Recognition

recognizer = sr.Recognizer()

def listen_for_voice():
    global birthday_triggered

    with sr.Microphone() as source:

        recognizer.adjust_for_ambient_noise(source)

        while not birthday_triggered:

            try:

                print("Listening...")

                audio = recognizer.listen(source)

                text = recognizer.recognize_google(audio)

                text = text.lower()

                print("You said:", text)

                

                if "joseph" in text:

                    print("JOSEPH DETECTED!")

                    birthday_triggered = True

                    try:
                        pygame.mixer.music.play()
                    except:
                        pass

                    break

            except:
                pass

threading.Thread(
    target=listen_for_voice,
    daemon=True
).start()

#Ballons

balloons = []

for _ in range(60):

    balloons.append({

        "x": random.randint(50, w - 50),

        "y": random.randint(h, h + 900),

        "radius": random.randint(20, 40),

        "speed": random.randint(2, 6),

        "color": (
            random.randint(120, 255),
            random.randint(120, 255),
            random.randint(120, 255)
        )
    })

#Main_loop

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)

    if birthday_triggered and captured_frame is None:
        captured_frame = frame.copy()

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    results = hands.process(rgb)

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

    cv2.putText(
        frame,
        "Say your name: JOSEPH",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        "Voice Activated Birthday AI",
        (20, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2
    )

    cv2.imshow(
        "AI Birthday Vision",
        frame
    )

   #celebration screen

    if birthday_triggered:

        celebration = np.zeros(
            (h, w, 3),
            dtype=np.uint8
        )

        # Balloons

        for balloon in balloons:

            balloon["y"] -= balloon["speed"]

            cv2.circle(
                celebration,
                (balloon["x"], balloon["y"]),
                balloon["radius"],
                balloon["color"],
                -1
            )

            cv2.line(
                celebration,
                (
                    balloon["x"],
                    balloon["y"] + balloon["radius"]
                ),
                (
                    balloon["x"],
                    balloon["y"] + balloon["radius"] + 45
                ),
                (255, 255, 255),
                2
            )

            if balloon["y"] < -50:
                balloon["y"] = h + 100

        # Camera snapshot

        if captured_frame is not None:

            photo = cv2.resize(
                captured_frame,
                (240, 180)
            )

            celebration[
                220:400,
                380:620
            ] = photo

            cv2.rectangle(
                celebration,
                (375, 215),
                (625, 405),
                (0, 255, 255),
                4
            )

        # Messages

        cv2.putText(
            celebration,
            "HAPPY BIRTHDAY",
            (40, 100),
            cv2.FONT_HERSHEY_DUPLEX,
            1.8,
            (0, 255, 255),
            4
        )

        cv2.putText(
            celebration,
            "Joseph Rafat",
            (140, 520),
            cv2.FONT_HERSHEY_DUPLEX,
            1.5,
            (255, 255, 255),
            4
        )

        cv2.putText(
            celebration,
            "Congratulations Joseph!",
            (50, 580),
            cv2.FONT_HERSHEY_DUPLEX,
            0.9,
            (0, 255, 0),
            2
        )

        cv2.putText(
            celebration,
            "We Wish You A Happy Birthday!",
            (50, 630),
            cv2.FONT_HERSHEY_DUPLEX,
            0.9,
            (255, 255, 255),
            2
        )

        cv2.putText(
            celebration,
            "AI Birthday Vision",
            (220, 690),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        cv2.imshow(
            "Birthday Celebration",
            celebration
        )

    key = cv2.waitKey(1)

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
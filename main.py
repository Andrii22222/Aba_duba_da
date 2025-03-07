import cv2
import mediapipe as mp

# Ініціалізація Mediapipe
mp_hands = mp.solutions.hands  # модуль для розпізнавання рук
mp_face_mesh = mp.solutions.face_mesh #модуль для розпізнавання обличчя (мережа ключових точок)
mp_drawing = mp.solutions.drawing_utils  #допоміжний інструмент для малювання точок і з'єднань

# Захоплення відеопотоку
cap = cv2.VideoCapture(0) #основна камера 0
#(Довіра)
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

emotion_text = ""
# original_bg = None
# previous_mouth_state = None

# Цикл обробки відео (зчитування кадрів з камери)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Дзеркальне відображення для зручності
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #(конвертація BGR в RGB)

    # Обробка обличчя (Здивування по точках)
    face_results = face_mesh.process(rgb_frame)
    if face_results.multi_face_landmarks:
        for face_landmarks in face_results.multi_face_landmarks:
            mouth_top = face_landmarks.landmark[13]
            mouth_bottom = face_landmarks.landmark[14]
            mouth_open = abs(mouth_top.y - mouth_bottom.y) > 0.02

            if mouth_open:
                emotion_text = "Surprised"
            else:
                emotion_text = "Neutral"

            h, w, _ = frame.shape
            x, y = int(face_landmarks.landmark[10].x * w), int(face_landmarks.landmark[10].y * h)
            cv2.putText(frame, emotion_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Обробка рук
    hand_results = hands.process(rgb_frame)
    clenched_fist = False

    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Координати пальців для перевірки стискання в кулак
            tip_ids = [4, 8, 12, 16, 20]
            fingers = []
            for tip in tip_ids:
                if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
                    fingers.append(1)
                else:
                    fingers.append(0)

            if sum(fingers) == 0:
                clenched_fist = True

    # Зміна фону при стиснутому кулаці
    if clenched_fist:
        frame[:] = (0, 255, 0)  # Зелений фон

    cv2.imshow('Face & Hand Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



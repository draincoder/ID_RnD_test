import logging

import cv2
from pydub import AudioSegment


def format_audio(filename: str):
    try:
        sound = AudioSegment.from_ogg(f'audios/{filename}')
        sound = sound.set_frame_rate(16000)
        sound.export(f'audios/{filename.replace("ogg", "wav")}', format="wav")
        return filename.replace("ogg", "wav")
    except Exception as e:
        logging.error(e)


def find_face(filename: str):
    try:
        flag = False
        img = cv2.imread(f'photos/{filename}')
        face_cascade_db = cv2.CascadeClassifier('data')
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade_db.detectMultiScale(img_gray, 1.1, 18)
        for (x, y, w, h) in faces:
            flag = True
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        if not flag:
            return False
        cv2.imwrite(f'photos/{filename}', img)
        return filename
    except Exception as e:
        logging.error(e)

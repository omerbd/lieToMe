# -*- coding: utf-8 -*-
import subprocess
from pydub import AudioSegment
import sys

import numpy as np
import cv2
import time




def thresholding(value):  # function to threshold and give either left or right
    global left_counter
    global right_counter

    if value <= 54:  # check the parameter is less than equal or greater than range to
        left_counter += left_counter # increment left counter

        if left_counter > th_value:  # if left counter is greater than threshold value
            print 'RIGHT'  # the eye is left
            left_counter = 0  # reset the counter

    elif value >= 54:  # same procedure for right eye
        right_counter += right_counter

        if right_counter > th_value:
            print 'LEFT'
            right_counter = 0


def converting(filename):
    name = filename.split(".")[0]
    command = "ffmpeg -i "+filename+" "+name+".wav"
    subprocess.call(command, shell=True)


def find_silence(sound):
    trim_ms = 0
    chunk_size = 10
    silence_threshold = -50
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms


def check_loudness(sound):
    counter_liar = 0
    counter_saint = 0
    if find_silence(sound) < 10:
        sound = sound[find_silence(sound):]
        if find_silence(sound) < 10:
            counter_liar += 1
        else:
            counter_saint += 1
    else:
        counter_saint += 1
    return counter_saint, counter_liar


def chunks(sound):
    count_saint = 0
    count_liar = 0
    for chunk in sound:
        chunk = sound[1:5000]
        saint, liar = check_loudness(chunk)
        if saint > liar:
            count_saint += 1
        else:
            count_liar += 1
        sound = sound[5001:]
    if count_saint > count_liar:
        return False
    elif count_liar > count_saint:
        return True


def main():

    file_name = "uploads\Video.wmv"
    converting(file_name)
    new_name = file_name.split(".")[0]
    audio = AudioSegment.from_file(new_name+".wav", format="wav")
    liar1 = chunks(audio)
    cap = cv2.VideoCapture(file_name)  # initialize video capture
    fps = cap.get(7)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    counter = 0
    last_is_face = True
    touches = 0
    real_touch_counter = 0
    liar2 = False
    while counter != length:
        counter += 1
        ret, frame = cap.read()
        cv2.line(frame, (320, 0), (320, 480), (0, 200, 0), 2)
        cv2.line(frame, (0, 200), (640, 200), (0, 200, 0), 2)
        if ret is True:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            faces = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
            detected_faces = faces.detectMultiScale(frame, 1.1, 5)
            is_face = False
            for (x, y, w, h) in detected_faces:  # similar to face detection
                is_face = True
            if not is_face and last_is_face:
                real_touch_counter += 1
                if real_touch_counter == 5:
                    touches += 1
                    real_touch_counter = 0
            last_is_face = is_face
            seconds = counter / fps
            if touches / seconds > 0.1:
                liar2 = True
    cap.release()
    cv2.destroyAllWindows()
    print (liar1 and liar2)
    sys.stdout.flush()


if __name__ == "__main__":
    main()



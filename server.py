from flask import Flask, jsonify
import cv2
import threading
import time
from plate_reader import read_plate
from core import Camera, Reading, Highway, average_speed, is_speeding, write_tickets

app = Flask(__name__)

h = Highway()
c1 = Camera("C1", 0.0)
c2 = Camera("C2", 10.0)
LIMIT = 100

def watch_camera(cam_obj, cam_index):
    '''
    Returns None.

    Effects: Reads frames continuously from cam_index,
             detects license plates, adds readings to h,
             prints detected plates and speeders to screen,
             writes speeding plates to tickets.txt

    watch_camera: Camera (anyof Nat Str) -> None
    Requires: cam_index is a valid camera index or stream URL
    '''
    cap = cv2.VideoCapture(cam_index)
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        cv2.imwrite("temp_" + cam_obj.cam_id + ".jpg", frame)
        plate = read_plate("temp_" + cam_obj.cam_id + ".jpg")
        if plate:
            t = time.time()
            r = Reading(plate, cam_obj, t)
            h.add_reading(r)
            print(cam_obj.cam_id + " detected: " + plate)
            speeders = h.find_speeders(LIMIT)
            if speeders:
                write_tickets(h, LIMIT, "tickets.txt")
                for s in speeders:
                    print("SPEEDING: " + s)
        time.sleep(1)

t1 = threading.Thread(target=watch_camera, args=(c1, 0))
t2 = threading.Thread(target=watch_camera, args=(c2, "http://10.0.0.212:8080/video"))
t1.start()
t2.start()
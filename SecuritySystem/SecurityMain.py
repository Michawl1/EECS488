"""
Author: Michael Thompson
Date: 4/23/2020
About: This is the main file for the security system
"""

import SecuritySystem.Resources.constants as constants
import SecuritySystem.Alarm as alarm
import cv2
import time
import os
import threading


class SecuritySystem:
    def __init__(self):
        self._active = True
        self._alarm = alarm.Alarm()

        os.makedirs(constants.ImgPath, exist_ok=True)

        self._camera_index = []
        self._cameras = []
        self._get_cameras()

        self._pass_img = None
        self._yolo_thread = None

        self._state = None
        self._change_state(0)

    def _get_cameras(self):
        """
        indexes every camera that open cv can see
        """
        index = 0

        while self._camera_index.__len__() < constants.MaxCameras:
            cap = cv2.VideoCapture(index)
            if not cap.read()[0]:
                break
            else:
                self._camera_index.append(index)
            cap.release()
            index += 1

        for i in self._camera_index:
            self._cameras.append(cv2.VideoCapture(i))

    def _grab_image(self):
        """
        gets an image from every camera available and saves it
        """
        index = 0
        for camera in self._cameras:
            ret, img = camera.read()
            name = "{}/{},{}.jpg".format(constants.ImgPath, index, time.time())
            cv2.imwrite(name, img)
            index += 1

    def _change_state(self, index):
        """
        changes the state to the given index
        """
        self._state = constants.States[index]

        for camera in self._cameras:
            camera.set(3, self._state["width"])
            camera.set(4, self._state["height"])

    def start(self):
        start_time = time.time()

        print("starting security scanner")
        self._yolo_thread = threading.Thread(target=yolo_frame_analyzer, args=(self._pass_img,))
        self._yolo_thread.start()

        # Super loop
        while self._active:
            if self._state["fps"] != 0 and (time.time() - start_time > 1.0 / self._state["fps"]):
                start_time = time.time()
                self._grab_image()
            if self._state == constants.HighRes:
                self._alarm.alert()

            if not self._yolo_thread.is_alive():
                self._yolo_thread = threading.Thread(target=yolo_frame_analyzer, args=(self._pass_img,))
                self._yolo_thread.start()


def yolo_frame_analyzer(img):
    """
    takes an image and returns the percentage height of the largest (closets) person in the frame
    :param img: the image to be processed
    :return: a floating point representing the height of the largest (closest) person
    """
    print("thread start")
    time.sleep(2)
    print("thread end")


if __name__ == '__main__':
    system = SecuritySystem()
    system.start()

"""
Author: Michael Thompson
Date: 4/23/2020
About: This is the main file for the security system
"""

import SecuritySystem.Resources.constants as constants
import cv2
import time
import os


class SecuritySystem:
    def __init__(self):
        self._active = True
        self._camera_index = []
        self._cameras = []
        self._get_cameras()

        self._state = None
        self._change_state(1)

        try:
            os.mkdir(constants.ImgPath)
        except:
            None

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
        for camera in self._cameras:
            return

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

        while self._active:
            if self._state["fps"] != 0 and (time.time() - start_time > 1.0 / self._state["fps"]):
                start_time = time.time()
                self._grab_image()


if __name__ == '__main__':
    system = SecuritySystem()
    system.start()
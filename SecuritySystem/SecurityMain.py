"""
Author: Michael Thompson
Date: 4/23/2020
About: This is the main file for the security system
"""

import SecuritySystem.Resources.constants as constants
import SecuritySystem.Alarm as alarm
import SecuritySystem.Yolo.PictureAnalyzer as PictureAnalyzer
import cv2
import time
import os
import threading


class SecuritySystem:
    def __init__(self):
        self._active = True
        self._alarm = alarm.Alarm()

        # yolo thread objects
        self._pass_img = None
        self._yolo_thread = None
        self._picture_analyzer = PictureAnalyzer.PictureAnalyzer()

        os.makedirs(constants.ImgPath, exist_ok=True)
        os.makedirs(constants.ImgPath1, exist_ok=True)
        os.makedirs(constants.ImgPath2, exist_ok=True)
        os.makedirs(constants.ImgPath3, exist_ok=True)

        self._camera_index = []
        self._cameras = []
        self._get_cameras()

        self._state = None
        self._state_num = [0]
        self._change_state(self._state_num[0])

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

        cv2.destroyAllWindows()

        for i in self._camera_index:
            self._cameras.append(cv2.VideoCapture(i))

    def _grab_image(self):
        """
        gets an image from every camera available and saves it
        """
        imgs = []
        for camera in self._cameras:
            ret, img = camera.read()
            imgs.append(img)

        for i in range(0, len(imgs)):
            imgs[i] = cv2.resize(imgs[i], (self._state["width"], self._state["height"]), interpolation=cv2.INTER_AREA)

        return imgs

    def _write_image(self, imgs):
        index = 0
        for img in imgs:
            name = "{}/{},{}.jpg".format(constants.StateImagePaths[self._state_num[0] - 1], index, time.time())
            cv2.imwrite(name, img)
            index += 1

    def _change_state(self, index):
        """
        changes the state to the given index
        """
        self._state = constants.States[index]

    def start(self):
        start_time = time.time()

        print("starting security scanner")

        self._yolo_thread = threading.Thread(target=yolo_frame_analyzer, args=(
            self._pass_img,
            self._picture_analyzer,
            self._state_num,))
        self._yolo_thread.start()

        # Super loop
        while self._active:
            if time.time() - start_time > 1.0 / self._state["fpspoll"]:
                self._change_state(self._state_num[0])
                start_time = time.time()
                imgs = self._grab_image()
                self._pass_img = imgs[0]
                print(self._state_num)

                if self._state_num[0] != 0:
                    self._write_image(imgs)

            if self._state == constants.HighRes:
                self._alarm.alert()

            if not self._yolo_thread.is_alive():
                self._yolo_thread = threading.Thread(target=yolo_frame_analyzer,
                                                     args=(
                                                         self._pass_img,
                                                         self._picture_analyzer,
                                                         self._state_num,))
                self._yolo_thread.start()


def yolo_frame_analyzer(img, picture_analyzer, state_num):
    """
    takes an image and returns the percentage height of the largest (closets) person in the frame
    :param img: the image to be processed
    """
    screenspace = picture_analyzer.process(img)
    print(screenspace)

    if screenspace < 0.05:
        state_num[0] = 0
    elif 0.05 <= screenspace < 0.3:
        state_num[0] = 1
    elif 0.3 <= screenspace < 0.7:
        state_num[0] = 2
    elif screenspace >= 0.7:
        state_num[0] = 3


if __name__ == '__main__':
    system = SecuritySystem()
    system.start()

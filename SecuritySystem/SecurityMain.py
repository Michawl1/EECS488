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

        SecuritySystem._make_dirs()

        self._camera_index = []
        self._cameras = []
        self._get_cameras()

        self._state = None
        self._state_num = [0]
        self._change_state(self._state_num[0])

    @staticmethod
    def _make_dirs():
        """
        makes the directories to put the images into
        """
        os.makedirs(constants.ImgPath, exist_ok=True)
        os.makedirs(constants.ImgPath1, exist_ok=True)
        os.makedirs(constants.ImgPath2, exist_ok=True)
        os.makedirs(constants.ImgPath3, exist_ok=True)

    def _get_cameras(self):
        """
        indexes every camera that open cv can see and puts them into self._cameras as a list
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
        gets an image from every camera available
        :returns a list of images, one from each camera
        """
        imgs = []
        for camera in self._cameras:
            ret, img = camera.read()
            imgs.append(img)

        for i in range(0, len(imgs)):
            imgs[i] = cv2.resize(imgs[i], (self._state["width"], self._state["height"]), interpolation=cv2.INTER_AREA)

        return imgs

    def _write_image(self, imgs):
        """
        Takes a list of images and writes them to a directory dictated by self._state_num
        :param imgs: list of images capture
        """
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
        """
        Main super loop of the program
        """

        print("starting security scanner")

        self._yolo_thread = threading.Thread(target=yolo_frame_analyzer, args=(
            self._pass_img,
            self._picture_analyzer,
            self._state_num,))
        self._yolo_thread.start()

        analyze_index = 0

        # get starting times so we can get our rates
        record_time = time.time()
        alarm_time = time.time()

        # Super loop
        while self._active:

            # get images at the rate dictated by the different states
            if time.time() - record_time > 1.0 / self._state["fpspoll"]:
                self._change_state(self._state_num[0])
                record_time = time.time()
                imgs = self._grab_image()
                self._pass_img = imgs[analyze_index % len(self._cameras)]
                print(self._state_num)

                if self._state_num[0] != 0:
                    self._write_image(imgs)

            # alarm
            if self._state == constants.HighRes and time.time() - alarm_time > 1.0:
                self._alarm.alert()

            # runs yolo image recognition on a frame, updates the state num and re runs the thread on a new image as
            # soon as this one is done
            if not self._yolo_thread.is_alive():
                self._yolo_thread = threading.Thread(target=yolo_frame_analyzer,
                                                     args=(
                                                         self._pass_img,
                                                         self._picture_analyzer,
                                                         self._state_num,))
                analyze_index += 1
                self._yolo_thread.start()


def yolo_frame_analyzer(img, picture_analyzer, state_num):
    """
    Takes an image and sees if there is a person in the frame
    This is intended to be run as a separate thread within the main super loop
    :param img: the image to scan for a person
    :param picture_analyzer: a PictureAnalyzer object used to run the yolo image recognition algorithm
    :param state_num: an array that holds the number of what state the system is in
    """
    screenspace = picture_analyzer.process(img)

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

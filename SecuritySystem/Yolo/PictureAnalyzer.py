"""
Author: Michael Thompson
Date: 4/23/2020
About: This class analyzes an image to flag all people in it
"""
import cv2
import numpy as np


class PictureAnalyzer:
    def __init__(self):
        self._net = cv2.dnn.readNet("Yolo/yolov3.weights", "Yolo/yolov3.cfg")
        self._classes = []
        with open("Yolo/coco.names", "r") as f:
            self._classes = [line.strip() for line in f.readlines()]
        self._layer_names = self._net.getLayerNames()
        self._output_layers = [self._layer_names[i[0] - 1] for i in self._net.getUnconnectedOutLayers()]
        self._colors = np.random.uniform(0, 255, size=(len(self._classes), 3))

    def process(self, img):
        """
        Scans image for objects
        :param img: an opencv image
        :return: the percent size of the largest height person box in the image
        """
        if img is None:
            return 0

        height, width, channels = img.shape
        blob = cv2.dnn.blobFromImage(img, 0.00392, (224, 224), (0, 0, 0), True, crop=False)

        self._net.setInput(blob)
        outs = self._net.forward(self._output_layers)

        largest_person_height = -1

        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(self._classes[class_ids[i]])
                if label == 'person' and y > largest_person_height:
                    largest_person_height = y

        return y / height

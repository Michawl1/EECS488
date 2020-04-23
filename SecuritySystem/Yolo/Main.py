"""
Author: Michael Thompson
"""

import cv2
import numpy as np


class Main:
    def __init__(self):
        return

    @staticmethod
    def get_all_cams():
        index = 0
        arr = []
        while True:
            cap = cv2.VideoCapture(index)

            print("hello world 2")

            if not cap.read()[0]:
                break
            else:
                arr.append(index)
            cap.release()
            index += 1

        print(arr)
        return arr


if __name__ == '__main__':
    print("hello world")

    print(Main.get_all_cams())


    # Load Yolo
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
    classes = []
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    cap = cv2.VideoCapture(0)
    print(cap)

    cap.set(3, 320)
    cap.set(4, 320)

    height = cap.get(4)
    width = cap.get(3)

    while True:
        # Capture frame-by-frame
        ret, img = cap.read()

        blob = cv2.dnn.blobFromImage(img, 0.01, (224, 224), (0, 0, 0), True, crop=False)

        net.setInput(blob)
        outs = net.forward(output_layers)

        # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.3:
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
        print(indexes)
        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                if (label == 'person'):
                    color = colors[i]
                    cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)

        # Display the resulting frame
        cv2.imshow('frame', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

import cv2
import numpy as np
# import time
from datetime import datetime
from abspath import resource_path
# import psutil

# import tracemalloc

# tracemalloc.start()

# cap = cv2.VideoCapture("cm5.jpg")
# cap = cv2.VideoCapture("opt.mp4")
detection_classes = []
IMG_SIZE = 416

with open(resource_path('yolo1/coco.names.txt'), 'rt') as f:
    detection_classes = f.read().rstrip('\n').split('\n')


model_config = resource_path("yolo1/yolov4.cfg")
model_weights = resource_path("yolo1/yolov4.weights")

net = cv2.dnn.readNetFromDarknet(model_config, model_weights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)


def find_objects(outputs, img, identified):
    NMS_THRESHOLD = 0.3
    h_img, w_img, rgb_layers_img = img.shape
    bbox = []
    class_ids = []
    confidence_vals = []
    for output in outputs:
        for detection in output:
            object_scores = detection[5:]
            class_id = np.argmax(object_scores)
            confidence = object_scores[class_id]
            if confidence > 0.5:
                w, h = int(detection[2]*w_img), int(detection[3]*h_img)
                x, y = int(detection[0]*w_img -
                           w/2), int(detection[1]*h_img-h/2)
                bbox.append([x, y, w, h])
                class_ids.append(class_id)
                confidence_vals.append(float(confidence))

    # print(bbox)
    indices = cv2.dnn.NMSBoxes(bbox, confidence_vals, 0.5, NMS_THRESHOLD)
    if len(indices) > 0:
        identified[0] = True
    for i in indices:
        i = i[0]
        box = bbox[i]
        x, y, w, h = box[0], box[1], box[2], box[3]
        # cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 255), 2)
        # print(detection_classes[class_ids[i]])
        if detection_classes[class_ids[i]] == "dog":
            print(" Detection:", datetime.now().strftime("%H:%M:%S %Y-%m-%d"))
            identified[1] = 1
            return identified
    # if len(indices) == 0:
    #     print("no classification")
    #     return False
    # print("couldn't find")
    return [identified[0], identified[1]]
# i = 0


def object_classifier(cap):

    # while 1:
    # res, img = cap.read()

    img = cap
    # img = cv2.imread("cm1.jpg")
    blob = cv2.dnn.blobFromImage(
        img, 1/255, (IMG_SIZE, IMG_SIZE), [0, 0, 0], 1, crop=False)
    net.setInput(blob)

    layer_names = net.getLayerNames()
    out_layer_names = [layer_names[i[0]-1]
                       for i in net.getUnconnectedOutLayers()]
    outputs = net.forward(out_layer_names)

    detect_res = find_objects(outputs, img, [False, 0])

    # print(psutil.cpu_percent())
    # cv2.imshow('fq', img)
    # time.sleep(5)
    return detect_res

    # if res == False:
    #     break

    # print(outputs[0].shape, outputs[1].shape, outputs[2].shape)
    # print(net.getUnconnectedOutLayers())

    # cv2.destroyAllWindows()
    # print(psutil.cpu_percent())

    # current, peak = tracemalloc.get_traced_memory()
    # print(
    #     f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
    # tracemalloc.stop()


# object_classifier(cap)

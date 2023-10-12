import cv2
import numpy as np
import random
import time
from pygame import mixer

def SetUpDetector():
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
    classes = []
    with open("coco.names", "r") as file:
        classes = file.read().splitlines()
    colours = np.random.uniform(0, 255, size = (len(classes), 3))

    cap = cv2.VideoCapture(0)
    #img = cv2.imread("image.png")
    return net, classes, colours, cap

def GetRandomListToFind():
    possibleObjectsToFind = []
    with open("objectsToFind.txt", "r") as file:
        possibleObjectsToFind = file.read().splitlines()

    objectsToFind = random.sample(possibleObjectsToFind, 7)

    return objectsToFind

def AnalyseFrame(net, classes, colours, cap, objectsToFind, objectsFound):
    #OBJECT DETECTION
    _, img = cap.read()
    imgHeight, imgWidth, _ = img.shape
    
    blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), (0,0,0), swapRB = True, crop = False)
    net.setInput(blob)
    outpuLayersNames = net.getUnconnectedOutLayersNames()
    layersOutput = net.forward(outpuLayersNames)

    precision = 0.5

    boxes = []
    confidences = []
    class_ids = []

    for output in layersOutput:
        for detection in output:
            scores = detection[5:]
            maxScoreIndex = np.argmax(scores)
            confidence = scores[maxScoreIndex]
            if confidence > precision:
                centerX = int(detection[0]*imgWidth)
                centerY = int(detection[1]*imgHeight)
                width = int(detection[2]*imgWidth)
                height = int(detection[3]*imgHeight)

                topLeftX = int(centerX - width/2)
                topLeftY = int(centerY - height/2)
                boxes.append([topLeftX, topLeftY, width, height])
                confidences.append(float(confidence))
                class_ids.append(maxScoreIndex)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, precision, 0.4)

    font = cv2.FONT_HERSHEY_PLAIN
    

    if len(indexes) > 0:
        for thing in indexes.flatten():
            x, y, w, h = boxes[thing]
            label = str(classes[class_ids[thing]])
            confidence = str(int(confidences[thing]*100))
            color = colours[class_ids[thing]]
            cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
            cv2.putText(img, label + " " + confidence, (x, y+20), font, 2, (255,255,255), 2)

            #CHECKING IF AN ITEM IS FOUND
            if label in objectsToFind:
                objectsToFind.remove(label)
                objectsFound.append(label)
                soundAffect = mixer.Sound("foundItem.mp3")
                soundAffect.play()
    
    cv2.imshow("img", img)
    
    if cv2.waitKey(1) & 0xFF == ord(" "):
        pass

    return net, classes, colours, cap, objectsToFind, objectsFound
    
def EndObjectDetection(cap): 
    cap.release()
    cv2.destroyAllWindows()

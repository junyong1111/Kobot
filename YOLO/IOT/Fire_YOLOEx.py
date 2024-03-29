#-*- coding:utf-8 -*-

import collections
from distutils.command.config import config
import pyrebase
import json
from datetime import datetime

config = {
    "apiKey": "AIzaSyBqQjlNppEdPpjZrA64zEgkKfAIIPo-TE8",
    "authDomain": "ossvideo-5e684.firebaseapp.com",
    "databaseURL":"https://ossvideo-5e684-default-rtdb.firebaseio.com/",
    "projectId": "ossvideo-5e684",
    "storageBucket": "ossvideo-5e684.appspot.com",
    "messagingSenderId": "798635139551",
    "appId": "1:798635139551:web:b76ed3012d82202bb2646a",
    "measurementId": "G-JFF15R9GQ8",
    "serviceAccount": "YOLO/IOT/serviceAcc.json"
}


## firebase sotrage 실행 ###
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
## firebase sotrage 실행 ###




import cv2
import numpy as np
import time # -- 프레임 계산을 위해 사용


vedio_path = './video.mp4' #-- 사용할 영상 경로
min_confidence = 0.5



def detectAndDisplay(frame): 
    detect_time = time.time()
    img = cv2.resize(frame, None, fx=0.8, fy=0.8)
    height, width, channels = img.shape
    #cv2.imshow("Original Image", img)

    #-- 창 크기 설정
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)

    #-- 탐지한 객체의 클래스 예측 
    class_ids = []
    confidences = []
    boxes = []
    

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            
            #-- 원하는 class id 입력 / coco.names의 id에서 -1 할 것 
            if class_id == 0 and confidence > min_confidence:
                #-- 탐지한 객체 박싱
                
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
               
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, min_confidence, 0.4)
    font = cv2.FONT_HERSHEY_DUPLEX
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = "{}: {:.2f}".format(classes[class_ids[i]], confidences[i]*100)
            print(i, label)
            color = colors[i] #-- 경계 상자 컬러 설정 / 단일 생상 사용시 (255,255,255)사용(B,G,R)
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y - 5), font, 1, color, 1)
    end_time = time.time()
    process_time = end_time - detect_time
    print("=== A frame took {:.3f} seconds".format(process_time))
    cv2.imshow("YOLO test", img)
    
    
#-- yolo 포맷 및 클래스명 불러오기
model_file = 'YOLO/Yolov4/yolov4-tiny.weights' #-- 본인 개발 환경에 맞게 변경할 것
config_file = 'YOLO/Yolov4/Yolov4_tiny.cfg' #-- 본인 개발 환경에 맞게 변경할 것
net = cv2.dnn.readNet(model_file, config_file)

#-- GPU 사용
#net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
#net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

#-- 클래스(names파일) 오픈 / 본인 개발 환경에 맞게 변경할 것
classes = []
with open("YOLO/IOT/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
## 기존 코드 i[0] - 1 을 수정해야함

colors = np.random.uniform(0, 255, size=(len(classes), 3))

#-- 비디오 활성화
cap = cv2.VideoCapture(0) #-- 웹캠 사용시 vedio_path를 0 으로 변경
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('output.avi', fourcc, 15.0, (int(width), int(height)))

Start_Time = time.time()



if not cap.isOpened:
    print('--(!)Error opening video capture')
    exit(0)
while True:
    ret, frame = cap.read()
    if frame is None:
        print('--(!) No captured frame -- Break!')
        break
    detectAndDisplay(frame)
    out.write(frame)
    End_Time = time.time()
    Time  = int(End_Time - Start_Time)
    
    if Time == 10:
        #####   데이터 업로드 #####
        ## 첫 번째는 데이터베이스에 보여지길 원하는 이름을 적고 그 다음에는 업로드할 파일의 경로를 적어준다.
        name = "Person" + str(datetime.now())
        storage.child(name).put(r"output.avi")
        #####   데이터 업로드 #####
        print("SAVE THE VIDEO ")
        Time = 0
        break
    #-- q 입력시 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
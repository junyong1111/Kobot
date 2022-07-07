# 얼굴 인식

## 학습을 통해 얼굴의 특성 추출

###  필요 라이브러리
- cmake (dlib 사용에 필요)
- dlib(C++ 기반의 머신러닝 라이브러리 )
- face_recognition (얼굴 인식)

```python
# pip install cmake
# pip install dlib
# pip install face_recognition
pip install -r requirements.txt
```
### 학습에 필요한 사진 준비

- 웹캠에서 동영상을 이미지로 변환 
save_image.py

```python
import cv2
import os

cap = cv2.VideoCapture("Emma.mp4")
## 동영상 경로

Name = str(input("Input Your Name\n"))
with open ("Names", "a") as txt:
    txt.write(Name + "\n")
## 사용자 등록

with open ("Image_path", "a") as txt:
    txt.write('Image/' + Name + "/\n")
    
count = 1

while cap.isOpened():
    ret, frame = cap.read()
    if not os.path.exists("Image"):
                os.makedirs('Image')
                os.makedirs("Image/"+Name)    
                     
    if not os.path.exists("Image/"+Name):  
        os.makedirs("Image/"+Name)              
            ## Image경로가 없다면 만드는 코드
    if not ret:
        print("종료")
        break
    if(int(cap.get(1)) % 10 == 0):
        ## 20프레임마다 저장  
        print('Saved frame number :' + str(int(cap.get(1))))
        cv2.imwrite("Image/"+Name+"/" + Name+ "%d.jpg" % count, frame)
        print('Saved frame%d.jpg' % count)
        count = count +1
        if(count == 21):
            break
        ## 최대 20장
cap.release()
```

### 학습 시작

Train_Face.py

```python
import enum
import cv2
import face_recognition
import pickle


Image_paths = []
Names = []
Image_num = 20
image_type = '.jpg'
encoding_file = 'encodings.pickle'
model_method = 'cnn'
## CNN or HOG  TRADEOFF 존재

## CNN 정확하지만 느림
## HOG 빠르지만 정확도가 떨어짐 

with open ("Image_path" , "r") as txt:
    Image_paths.append(txt.read().split())
## 이미지 경로 가져오기    
with open ("Names" , "r") as txt:
    Names.append(txt.read().split())
## 사용자 정보 가져오기
# print(Image_paths)
# print(Names)

knownEncodings = []
knownNames = []

for (i, Image_path) in enumerate(Image_paths):
    name = Names[i]
    #print(name)
    for idx in range(Image_num):
        file_name = Image_path + str(idx+1) + image_type
        #print(file_name)
        
        image = cv2.imread(file_name)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
################# 저장된 경로에서 이미지를 하나씩 읽어옴 ##################

        boxes = face_recognition.face_locations(rgb, 
                                                model = model_method)  
        ##  face_recognition을 이용하여 얼굴 부분 확인 -> CNN 모델 사용
        
        encodings = face_recognition.face_encodings(rgb, boxes)
        ## face_recognition을 이용하여 얼굴 특징 인코딩  
        
        for encoding in encodings:
            print(file_name, name, encoding)
            knownEncodings.append(encoding)
            knownNames.append(name)
            ## 인코딩된 값을 저장
            
## 위에서 얻은 정보들을 파일로 저장
data = {"encodings": knownEncodings, "names": knownNames}
f = open(encoding_file, "wb")
f.write(pickle.dumps(data))    
```








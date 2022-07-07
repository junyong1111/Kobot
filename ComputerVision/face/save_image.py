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
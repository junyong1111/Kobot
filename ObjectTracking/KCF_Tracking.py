import cv2

tracker = cv2.TrackerKCF_create()

video = cv2.VideoCapture(0)
ok, frame = video.read()
## ok -> 올바르게 읽었는지
## 영상의 첫번째만 확인

bbox = cv2.selectROI(frame) 
## 첫번째 프레임에 대한 정보만 저장
## 관심영역 선택
print(bbox)

ok = tracker.init(frame, bbox)
# print(ok)


while True:
    ## 영상의 각 프레임 통과
    ok, frame = video.read()
    
    if not ok: ## 처리할 프레임이 없는경우
        break
    ok, bbox = tracker.update(frame)
    # print(bbox)
    
    if ok:
        (x, y, w, h) = [int(v) for v in bbox]
        # (420, 24, 390, 519)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2,1)
    else:
        cv2.putText(frame, "Error", (100,100), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2)
    
    cv2.imshow("Tracking", frame)
    
    if cv2.waitKey(1) & 0xFF == 27:
        break ### ESC
    
    

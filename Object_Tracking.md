# 실시간 객체 트랙킹

등록된 사용자를 제외한 외부침입자를 인식하여 트랙킹하는 방법

### 트래킹 알고리즘과 객체 감지와의 차이점

- 트래킹 알고리즘
  - 감지 알고리즘보다 훨씬 빠름
  - 기존 데이터를 사용하여 다음 탐지에 재사용이 가능하기 때문에
  - 하지만 급격한 변화에는 대응하기 힘들다.

#### 만약 100개의 프레임이 있는 영상의 경우

- 감지 알고리즘 프레임별로 100번의 객제 감지 실행
- 트래킹 알고리즘은 첫 번째 프레임에서 객체를 탐지 후 이 정보를 영상 끝까지 사용

### 2. KCF 및 CSRT 알고리즘

- KCF(KERNAL CORRELATION FILTERS) : 커널 상관 필터로 빠른 알고리즘이지만 빠른 영상에서는 작동이 잘 안된다.
  - 경계 상자가 객체를 놓치는 경우

1. 초기 선택된 프레임이 파티클 필터라는 개념을 적용하여 더 큰 경계 상자 2개를 생성히여 이미지를 더 크게 포함
2. 얼굴의 중앙점을 수학적 연산을 통해 계산
3. 각각의 프레임들을 얼굴의 중앙점에 맞게 업데이트

- CSRT(DISCRIMINATIVE CORRELATION FILTER WITH CHANNEL AND SPATIAL RELIABILITY) : 채널 및 공간 신뢰도를 통한 구분 상관 필터이며 다른 알고리즘보다 정확하지만 느리다.

1. 첫 번째 박스에서 트래킹 하려는 객체를 탐지
2. HOG 기법을 사용하여 학습
   - HOG : 이미지에서 중요 정보는 추출하고 나머지는 버림
3. 랜덤 마르코프 테스를 적용
   - 트래킹 객체의 움직임을 감지
4. 컨피던스 맵
   - 마스크로 가져린 객체만을 추출 (원본 이미지의 정보)
5. 추적할 객체만을 추출

### KCF로 객체 트래킹 구현

```
추적 트래킹을 사용하기 위해서 설치
pip install opencv-contib-python
```

1. New file 생성 (Object_Treacking.py)

```python
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
```

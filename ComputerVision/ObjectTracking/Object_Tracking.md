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

### CSRT 객체 트래킹 구현

KCF 알고리즘에서는 따라가지 못했던 객체를 따라가는 모습을 볼 수 있다.

```python
import cv2

tracker = cv2.TrackerCSRT_create()
## 위 모델에서 KCF -> CSRT로 바꿔주기만 하면 된다.

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
### 3. Deep Sort 알고리즘

위 두개의 알고리즘 보다 더 좋아 보임

## DeepSORT : 기존 SORT Tracker의 (Detection + Kalman Filter + Hungarian Algorithm) 구조에서 '딥러닝'을 복합한 구조로, Appearance를 이용한 거리 측정 등을 통해 기존 SORT보다 더 뛰어난 성능을 보여주는 추적기이다.

- Kalman filter(칼만 필터)

쉽게 말해 이전 프레임에 등장한 개체를 이용하여 다음 움직임을 예측하는 것이다.

- Hungarian algorithm

Deep sort가 이전등장한 객체와 예측한 객체가 동일하다라고 판별하는 기준

### 설명을 봐도 어렵다 일단 구현해보자..

유투버 The AI Guy의 영상과 Github을 참고하혔음

[참고링크](https://www.youtube.com/watch?v=FuvQ8Melz1o)

## 선수 지식
- YOLOv4 
- Tensorflow
- Google Colab  

##### <u> 가상환경 및 GPU 설정이 어렵다면 COLAB 사용을 추천</u>


### Colab -> 런타임 변경 -> GPU 설정
Coalb 또는 프로젝트를 시작할 폴더에서 Git clone
```
git clone https://github.com/theAIGuysCode/yolov4-deepsort.git
```



1. YOLOv4 가중치파일과 cfg파일을 다운로드  
[Github 주소]https://github.com/AlexeyAB/darknet
- [yolo4.weight](https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights)
- [yolo4.cfg](https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4.cfg)

위 두 파일을 다운로드 해준다.   
##### # 나는 IOT 사용을 위해 tiny모델을 다운로드함

2. 가상환경 설치 및 필요 라이브러리 설치

### <mark>Tensorflow 버전은 2.3.0이어야 한다</mark>
<u>만약 아닌경우 해당 코드 실행</u>
```python
#### 이 코드를 추가하지않으면 실행 불가
!pip uninstall tensorflow -y
!pip install tensorflow==2.3.0
import tensorflow
tensorflow.__version__
```

가상환경 및 라이브러리 설치

```python
# Tensorflow CPU
conda env create -f conda-cpu.yml
conda activate yolov4-cpu

# Tensorflow GPU
conda env create -f conda-gpu.yml
conda activate yolov4-gpu
#  =============== 가상환경설치 ============== 
# TensorFlow CPU
pip install -r requirements.txt

# TensorFlow GPU
pip install -r requirements-gpu.txt

#  =============== 라이브러리 설치 ============== 
```

3. Yolo 모델을 Tensorflow 모델로 변환

#### 변환하는 이유 
- 자유롭게 커스텀이 가능
- tensorflow lite를 이용하여 모바일 개발이 가능
    - YOLO를 라즈베리파이에서 사용함에 있어서 많은 제약이 있다 IOT사용을 위해 모델을 가볍게 만드는과정이 필수

```
python save_model.py --model yolov4 
```
위 명령어로 쉽게 YOLO모델을 tensorflow모델로 변환이 가능하다.



4. 객체 추적하기

변환된 모델을 이용하여 객체 추적

```python
# 저장된 비디오에서 yolo4 deep sort 객체 추적
python object_tracker.py --video ./data/video/test.mp4 --output ./outputs/demo.avi --model yolov4

# 노트북 webcam에서  yolo4 deep sort 객체 추적 (video 0으로 설정)
python object_tracker.py --video 0 --output ./outputs/webcam.avi --model yolov4
```

<mark>tiny 모델 사용법  </mark>

```python
# save yolov4-tiny model
python save_model.py --weights ./data/yolov4-tiny.weights --output ./checkpoints/yolov4-tiny-416 --model yolov4 --tiny

# Run yolov4-tiny object tracker
python object_tracker.py --weights ./checkpoints/yolov4-tiny-416 --model yolov4 --video ./data/video/test.mp4 --output ./outputs/tiny.avi --tiny
```

5. 원하는 클래스만 추적하게 코드 수정

object_tracker.py 파일 수정  
159번째 줄 코드 수정
```python
# 원하는 클래스만을 넣어주면 해당 객체만 트랙킹한다. class정보는 coco.names 또는 자신이 학습한 names파일을 참고한다.
        allowed_classes = list(class_names.values())
        #ex
        # allowed_classes = ['person']
```





<!-- <details>
<summary>  </summary>
<div markdown="1">

</div>
</details>  -->

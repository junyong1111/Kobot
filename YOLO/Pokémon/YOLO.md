### YOLO   

#### YOLO (You Only Look Once): 
YOLO 


장점:
1. 간단한 처리과정으로 속도가 매우 빠르다.
2. Image 전체를 한 번에 바라보는 방식으로 class에 대한 맥락적 이해도가 높다. 
4. 실시간 객체 탐지가 가능하다.


단점:
1. 상대적으로 낮은 정확도 (특히, 작은 object에 대해)

#### 실습환경: Google Colab (Linux 기반)
* Start_YOLO.ipynb : Colab에서 YOLO를 실행하기 위한 Cudnn과 Darknet설치방법이 있는 코드
* Pokemon_YOLO_v3 : 구축된 YOLO환경을 이용해서 Pokemon Custom 학습데이터를 생성하는 코드
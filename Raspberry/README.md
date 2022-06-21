<details>
<summary> Raspberry 기본설정 </summary>
<div markdown="1"> 

### 라즈베리파이 한글 설치

#### Step.1
```
sudo apt-get install fonts-unfonts-core
sudo apt-get install ibus ibus-hangul
sudo reboot
```
#### Step.2

설정 -> 기본 설정 -> IBus 환경 설정 -> IBus 데몬 실행 



### 라즈베리파이 아두이노 설치

```
sudo apt-get install arduino
```

### 라즈베리파이 웹캠 설치

- 웹캠 설정
```
sudo raspi-config
```

Interfacing Options -> Camera -> enable 설정


- 웹캠 정보확인 
```
v4l2-ctl -V
```

- 패키지 설치

```
sudo apt-get update
sudo apt-get install fswebcam
```


- 사진 촬영
```
fswebcam -r 1280*960 --no-banner image2.jpg
```

home/pi에서 해당 이미지 확인


</div>
</details>


<details>
<summary> MQTT 통신 </summary>
<div markdown="1"> 


</div>
</details>



<!-- <details>
<summary>  </summary>
<div markdown="1"> 

</div>
</details>  -->



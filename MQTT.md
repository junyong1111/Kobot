## MQTT 사물인터넷 통신 프로젝트

- 선수 지식
    - Arduino
    - Node.js
    - MongoDB
    - C언어

- 준비물
    - Wifi 모듈이 있는 보드 (WemosD1)
    - 온/습도 센서 (DH11)
    - LED

### 전체적인 흐름도

<img width="797" alt="스크린샷 2022-06-21 오후 8 30 51" src="https://user-images.githubusercontent.com/79856225/174789401-d987208e-18e5-435d-94ea-8bfa1d8bbff2.png">

1. Socket 통신 방식 제어
2. RESTfull Service 통신 방식 제어

### 개발환경 구성
1. Arduino 설치 후 WeMos D1 R1 보드 선택 후 Blink 예제 실행

2. Wifi 연결 & 웹서버 구축

<details>
<summary> Wifi 연결 </summary>
<div markdown="1"> 


```c++
#include <ESP8266WiFi.h>
// 헤더파일 include

const char * ssid = "";
const char * password = "";

// 접속할 Wifi 정보 입력

WiFiServer server(80);
// 80 포트로 연결

void setup(){
    Serial.begin(9600);
    // 9600의 속도를 가진 시리얼 통신 
    delay(10);

    Serial.println();
    Serial.print("Connection to");
    Serial.println(ssid);

    WiFi.begin(ssid, password);
    // Wifi 연결 시도

    while(WiFi.status()!= WL_CONNECTED){
        delay(500);
        Serial.print(".");
    } // 연결이 성공할때까지 실행
    Serial.println("");
    Serial.println("WiFi connected");

    server.begin();
    Serial.println("Server started");
    // Server Start!!

    Serial.println(WiFi.localIP());
} //Setup

void loop(){ // Client 요청이 올때마다 웹페이지 전송
    WiFiClient client =  server.available(); // Client 접속 체크

    if(!client){ // 요청이 올때까지 계속 반복
        return; 
    }

    Serial.println("New Client");

    String req = client.readStringUntil('\r');
    Serial.println(req);
    client.flush(); // 정보 비우기
    

    String s = "<html>";
    s = s+ "<meta name= 'viewport' content = 'width=device-width, initial-scale = 1.0'/>";
    s = s+ "<meta http-equiv='Content-Type' content= 'text/html;charset=utf-8'/>";
    s = s+"<head></head><body>Hello World!</body></html>";

    client.print(s);
    delay(1);
    Serial.println("Client disonnected");
}

```

</div>
</details> 

<details>
<summary> 웹서버 구축 </summary>
<div markdown="1"> 



</div>
</details>









<!-- <details>
<summary>  </summary>
<div markdown="1"> 

</div>
</details>  -->
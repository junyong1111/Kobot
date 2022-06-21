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
    // 시리얼 모니터와 같은 값을 지정하며 해당 보드는 보통 115200 
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

사용 함수 설명

<details>
<summary> ESP8266WebServer() </summary>
<div markdown="1"> 

- 접속 포트를 설정 
- HTTP 프로토콜은 기본적으로 80번 포트를 사용하며 디폴트값으로 지정되어있음

```c++
ESP8266WebServer(int port = 80)
```

|인자|설명|
|------|---|
|port|접속 포트|

</div>
</details>


<details>
<summary> on() </summary>
<div markdown="1"> 

- 클라이언트의 요청에 대한 처리 함수
- 서버의 웹 페이지를 표시하는 URL은 컴퓨터의 파일과 마찬가지로 계층적인 디렉토리 구조
- 클라이언트의 요청 처리 함수는 서버에 접속할 수 있는 주소에 따라 달리 지정한다.

```c++
void on(const char * url, ThandlerFunction handler)
```

|인자|설명|
|------|---|
|url|주소|
|handler|처리 함수|

</div>
</details>


<details>
<summary> onNotFound() </summary>
<div markdown="1"> 

- 존재하지 않는 주소로 접속하였을 경우 처리 함수

```c++
void onNotFound(ThandlerFunction fn)
```


|인자|설명|
|------|---|
|fn|처리 함수|

</div>
</details>



<details>
<summary>begin() </summary>
<div markdown="1"> 

- 웹 서버를 시작

```c++
void begin()
```

</div>
</details>


<details>
<summary>handleClient() </summary>
<div markdown="1"> 

- 서버가 시작된 후 클라이언트의 요청을 받을 수 있다, 요청에 대한 처리는 handleClient()를 사용
- handleClient() 함수는 클라이언트의 요청이 있는 경우 클라이언트와 연결으 생성하고 요청을 처리
- 클라이언트가 접속하는 주소에 따라 해당하는 처리 함수 호출

```c++
void handleClient()
```

</div>
</details>


<details>
<summary>send() </summary>
<div markdown="1"> 

- 클라이언트로 데이터 전송

```c++
void send(int code, char* content_type, String content)
```


|인자|설명|
|------|---|
|code|HTTP 응답 코드|
|content_type|전송 내용의 종류|
|content_type|전송 내용|

</div>
</details>







```c++
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

const char* ssid = "";
const char* password = "";

ESP8266WebServer server(80); const int led = 14;
String s,s_head;

void handleRoot() { 
    digitalWrite(led, HIGH);
    s=s_head+"<h1>켜짐</h1><br>";
    server.send(200, "text/html", s);
//server.send(200, "text/plain", "hello from esp8266!");
}

void handleNotFound(){
    digitalWrite(led, 1);
    String message = "File Not Found\n\n";
    message += "URI: ";
    message += server.uri();
    message += "\nMethod: ";
    message += (server.method() == HTTP_GET)?"GET":"POST"; message += "\nArguments: ";
    message += server.args();
    message += "\n";
    for (uint8_t i=0; i<server.args(); i++){
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n"; }
    server.send(404, "text/plain", message);
    digitalWrite(led, 0); }
// WIFI_STA (Station mode, Stand-alone mode)
// 다른 공유기에 접속해서 IP를 할당받고, HTTP 통신을 사용하는 모드입니다 
void setupWifi() {
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password); Serial.println("");
// Wait for connection
    while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print("."); }
    Serial.println(""); Serial.print("Connected to "); Serial.println(ssid); Serial.print("IP address: "); Serial.println(WiFi.localIP());
}

void setup(void){
    pinMode(led, OUTPUT);
    digitalWrite(led, LOW); Serial.begin(115200);
    // 여기 프로그램 부분을 함수로처리 
    setupWifi();
    // 스마트폰에 맟게 크기 조정, html에서 한글 출력하게 설정
    s_head="<meta name='viewport' content='width=device-width, initial-scale=1.0'/>";
    //s=s+"<meta http-equiv='refresh' content='5'/>";
    s_head=s_head+"<meta http-equiv='Content-Type' content='text/html;charset=utf-8' />";
    server.on("/", handleRoot); server.on("/inline", [](){
    //server.send(200, "text/plain", "this works as well"); 
    digitalWrite(led, LOW);
    s=s_head+"<h1>꺼짐</h1><br>";
    server.send(200, "text/html", s);
    });
    server.onNotFound(handleNotFound);
    server.begin();
    Serial.println("HTTP server started"); }
void loop(void){
    server.handleClient();
}

```



</div>
</details>









<!-- <details>
<summary>  </summary>
<div markdown="1"> 

</div>
</details>  -->
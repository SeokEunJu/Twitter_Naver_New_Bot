# [개인 프로젝트] 트위터 뉴스 봇 만들기

## 1. 프로젝트 개요

### 트위터의 랜덤 선택봇 중 하나

<p align="center">
<img width="600" src="https://user-images.githubusercontent.com/50102137/83377369-5d4d4b00-a410-11ea-9c46-3554baf23925.png">
<img width="600" src="https://user-images.githubusercontent.com/50102137/83377382-62aa9580-a410-11ea-8777-cb255806bc3b.png">
</p>

스크린샷과 같이 트위터 API를 사용해서 유저가 공백으로 구분된 인풋 2개 이상을 넣으면 해당 인풋 중 하나를 랜덤으로 골라 유저에게 멘션으로 돌려주는 봇을 우연히 보게 되었다.

언젠가 나도 저런 봇을 만들어보고 싶다 생각만 하던 차에 이번 멘토링을 시작하면서 API에 대해 공부하게 되었고 바로 지금이 봇을 만들어보기에 적기라는 생각이 들었다.

무슨 봇을 만들까 고민하던 중 나에게 매일 아침 일어나면 트위터부터 키면서 타임라인의 뉴스를 쭉 훑어보는 습관이 있다는 게 떠올랐다.

뉴스를 훑어보면서 이 주제에 관련한 새로운 기사는 없나 싶어 힘들게 네이버를 따로 켜서 검색해보던 나날들도 스쳐지나갔다.(aka. 코로나 확진자)

그래서 최종적으로 구체화된 아이디어가 바로, "유저가 멘션한 키워드를 네이버에 검색해 상단 뉴스 3개를 멘션해줘!" 라는 취지의 [@naver_news_bot](https://twitter.com/naver_news_bot) 이다.

### 당시 원하던 모습

<p align="center">
<img width="600" src="https://user-images.githubusercontent.com/50102137/83378109-ae5e3e80-a412-11ea-94eb-d8c7e857a7b5.png">
</p>

코드 없이 손으로 링크를 복사해서 처음 올려본 트윗이다.

일종의 프로토 타입

시작 당시엔 뉴스 제목까지도 넣지 않고 링크만 복사해서 넣을 예정이었다.

이렇게 프로토타입을 짜놓은 후 본격적인 개발에 들어갔다.

## 2. 프로젝트 구조

해당 프로젝트의 구현을 위해서는 네이버와 트위터 API를 둘 다 사용해야 했기 때문에 각각의 API를 사용하는 코드를 파일 두개로 나누어서 관리했다.

### naverAPIClient.py

키워드를 입력하면 해당 키워드를 뉴스 카테고리의 검색인자로 넣는 리퀘스트를 서버에 날려준다.

그렇게 해서 얻은 상위 3개 뉴스 링크가 너무 길었기 때문에 shorturl로 변환해준다.

3개의 shorturl로 변환된 링크를 알맞은 뉴스 타이틀과 묶어 리스트 형태로 반환한다.

### twitterAPIClient.py

SINCE_ID부터 시작해 타임라인을 관찰하며 자신에게 날라온 멘션이 있는지, 그리고 멘션이 있다면 [뉴스 키워드] 형태인지 체크해서 naverAPIClient의 인자로 pass해준다.

결괏값을 naverAPIClient로부터 받으면 해당 트윗에 멘션으로 결과를 달아준다.

### twitter_set_api.py

트위터 API 세팅을 위해 따로 빼둔 파일이다.

consumer_key, consumer_secret 등의 키 값을 환경변수로 읽어들여 API를 생성하고 에러가 발생할 경우 log로 남긴다.

성공적으로 API를 생성할 경우 해당 API를 반환한다.

### errors.py

네이버 API를 사용할 때 custom error를 raise할 필요가 생겼고, 이를 위해 custom error들만 모아둔 파일이다.

### SINCE_ID

트위터 API의 경우 타임라인의 트윗들에 각각 고유한 ID를 붙인다.

원래는 SINCE_ID를 코드내에서 1로 설정해두었기 때문에 새로 컴파일을 할 때마다 저번 컴파일에서 멘션을 달았던 트윗에 중복되게 멘션을 다는 일이 발생했다.

그래서 SINCE_ID라는 이름의 파일을 만들어 해당 파일에 제일 마지막으로 멘션을 단 트윗의 고유 ID를 저장하고 새로 컴파일을 할 때마다 그 값을 읽어들여 거기서부터 탐색을 돌리도록 하였다.

따라서 해당 프로젝트를 클론하여 봇을 돌려보고 싶을 경우 SINCE_ID의 값을 1로 초기화하는 것이 좋을 것이다.

## 3. 설치 및 사용 방법

### (1) 환경변수 세팅

(먼저 작업환경은 virtual machine에서 돌리는 우분투임을 밝힌다.)

리눅스 터미널에 들어가서 환경변수를 세팅해주어야 한다.

트위터와 네이버의 secret_key들을 각각 앱에서 받아와서 적합한 이름으로 등록해주면 된다.

([secret_key가 뭐에요?](http://hleecaster.com/twitter-api-developer/))

세팅 방법은 다음과 같다.

    $vi ~/.bashrc  // /.bashrc열기
    export NAVER_CLIENT_ID='239bna93nhgpaz9qj...'/ // .bashrc의 마지막 줄에 추가
    $ source ~/.bashrc // 수정한 .bashrc 파일 적용

이 때 네이버 API에서는 client, secret 두개의 키가 필요하며

트위터 API에서는 API key, API secret key, Access token, Acess token secret 총 네 개의 키가 필요하다.

<p align="center">
<img width="600" src="https://user-images.githubusercontent.com/50102137/83411277-e38a8100-a452-11ea-91a9-c2f024bf799f.png">
<img width="600" src="https://user-images.githubusercontent.com/50102137/83411357-0b79e480-a453-11ea-8cdf-6512d6cd7634.png">
</p>

각각 naverAPIClient, twitter_set_api에서 환경변수를 불러오는 부분이며, 환경변수의 이름과 코드의 인자가 매치되어야 API 사용이 가능하다.

### (2) 필요한 패키지 설치

간혹 특정 패키지가 없어서 코드 컴파일이 안 될 수도 있다. 그럴 때를 대비해서 requirement.txt 파일이 존재한다.

    $ pip install -r requirements.txt
    
위의 명령어를 통해 나의 작업환경과 똑같이 패키지 설치를 할 수 있다.

### (3) 무엇을 컴파일 해야 하나요?

    python twitterAPIClient.py

자 당신도 이제 네이버 뉴스 봇을 가지게 되었다. 제법 쓸만할 것이다!

해당 코드는 SINCE_ID에 있는 값을 읽어와서 해당 ID를 가진 트윗 다음부터 3초마다 한번씩 탐색해나가며 "[뉴스 키워드]" 형태의 나에게 온 멘션이 있는지 찾는다.

그리고 한 번 찾으면 해당 트윗의 ID를 다시 SINCE_ID에 기록하고 뉴스 검색결과를 돌려준다.

따라서 git clone 후에 SINCE_ID 파일을 열어 1로 바꿔두는 것을 추천한다.

## 4. 프로젝트 구현

### 프로젝트 결과물

<p align="center">
<img width="600" src="https://user-images.githubusercontent.com/50102137/83379696-1e6ec380-a417-11ea-95a8-1ad9039017a8.png">
</p>

약 3주 정도의 개발 끝에 완성된 결과물이다.

## PS

사실 혼자였다면 못했을 텐데, 멘토링이다 보니 멘토님의 도움도 여러번 받아가며 끝까지 완수해낼 수 있었다.

이번 프로젝트에서는 API가 얼마나 유용한 툴인지, 코드 refactoring가 왜 중요한지, 이 두 가지를 알게 된 게 가장 큰 수확이라고 생각한다.

학교 과제를 하면서는 refactoring은 무슨 완성하기 급급해 쓸데없는 주석이며 파이썬 네이밍 규칙이며 다 무시하고 그냥 냈었다.

그래서 원하는 기능을 개발하고 나서도 하나의 코드를 3~4번 refactoring을 반복해가며 계속 계속 들여다 본 건 처음이라 새로웠다.


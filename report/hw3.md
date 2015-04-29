# 컴퓨터 그래픽스 - 숙제3

2015 봄 학기  
Swept Surface Design  
2009-11744 심규민

## 1. 실행

### 1-1. 환경 및 코드

먼저, 다음의 환경을 갖춘다.

* Linux (or Mac OS X)
* Python 2.7
* pip (for installing python packages)
* Git (for getting the source code)
* freeglut3

다음과 같이 Github에서 코드를 가져온다.

```bash
git clone https://github.com/sim0629/graphics.git
cd graphics
git checkout hw3
```

또는 코드를 zip 파일로 가지고 있을 경우, 압축을 푼다.

```bash
unzip hw3.zip -d graphics
cd graphics
```

다음 명령어로 필요한 파이썬 패키지를 설치한다.
이 명령어는 환경에 따라 `sudo`로 실행해야 할 수도 있다.

```bash
pip install -r requirements.txt
```

### 1-2. 방법 및 옵션

다음 명령어로 Swept Surface Designer를 실행한다.

```bash
python surface surface/ring.dat
```

`surface/ring.dat` 대신 원하는 data 파일의 경로를 넣어줄 수 있다.
제공된 두 파일 `surface/trombone.txt`, `surface/coke_bottle.txt`이 준비되어 있다.

모델에 따라 아무것도 보이지 않을 수 있는데,
그 경우 `space`키를 눌러 show all을 하면 보이게 된다.

실행할 때에 파일 인자를 생략할 수는 없지만,
만약 새 파일을 만들고 싶다면, 다음의 명령을 통해 얻을 수 있다.

```bash
python surface sample natural 3 4 > sample.dat
```

`natural`은 curve type을 나타내며(`natural` 대신 `catmull_rom`이나 `bspline`도 가능),
cross section의 개수와, 한 cross section 내의 point 개수가 차례로 주어진다.
주어진 조건에 맞는 적절한 data가 생성되어 stdout으로 출력된다.

사소하지만, 경로가 `sample`인 data 파일은 넣어줄 수 없다.

## 2. 조작

### 2-1. 모드

Swept Surface Designer는 세 가지 모드로 구분되어 동작한다.
초기값은 Viewing 모드이며, 모드 전환 방법은 다음과 같다.

| 모드         | 전환 방법 |
|--------------|-----------|
| Viewing      | `q`키     |
| Editing      | `e`키     |
| Transforming | `r`키     |

Viewing 모드에서는 swept surface를 보는 작업을 할 수 있고,
Editing 모드에서는 각 cross section의 control points를 움직일 수 있으며,
Transforming 모드에서는 cross sections를 scaling, rotation, translation 할 수 있다.

현재 모드와 상태는 window title에 표시된다.

### 2-2. Viewing

Viewing 모드에서는 다음과 같은 조작을 할 수 있다.

| 동작         | 방법                              |
|--------------|-----------------------------------|
| Rotation     | 마우스 드래그                     |
| Translation  | `shift`키를 누른 채 마우스 드래그 |
| Dolly in/out | `w`/`s`키                         |
| Zoom in/out  | `d`/`a`키                         |
| Show all     | `space`키                         |
| Seek         | `ctrl`키를 누른 채 마우스 클릭    |

### 2-3. Editing cross sections

Editing 모드에서는 다음과 같은 조작을 할 수 있다.
마우스 down 할 때 마우스에 근접한 point가 선택되어 조작된다.

| 동작               | 방법          |
|--------------------|---------------|
| Control point 이동 | 마우스 드래그 |
| 다음 cross section | `]`키         |
| 이전 cross section | `[`키         |

다음, 이전 cross section으로 넘어가는 기능은 wrapping 된다.

### 2-4. Transforming cross sections

Transforming 모드에서는 다음과 같은 조작을 할 수 있다.
기본적으로 cross section을 변형(model 움직임)시키며,
viewing(camera 움직임)도 할 수 있다.
각 cross section의 center point를 선택하여 조작하며,
마우스 down 할 때 마우스와 가장 가까운 point가 선택된다.

| 동작             | 방법                                      |
|------------------|-------------------------------------------|
| Scaling(up/down) | `ctrl`키를 누른 채 마우스 드래그(위/아래) |
| Rotation         | 마우스 드래그                             |
| Translation      | `shift`키를 누른 채 마우스 드래그         |
| Viewing          | `alt`키를 누른 채 viewing 모드처럼 조작   |

이 모드에서 Show all과 Seek은 동작하지 않는다.

### 2-5. 그 외 중요한 것

현재 모드에 상관없이 동작하는 키는 다음과 같다.

| 동작                         | 방법      |
|------------------------------|-----------|
| Data 파일 저장               | `Enter`키 |
| Interpolation 간격 증가/감소 | `+`,`-`키 |
| Wireframe on/off             | `p`키     |
| Curve type 변경(catmull-rom) | `c`키     |
| Curve type 변경(bspline)     | `b`키     |
| Curve type 변경(natural)     | `n`키     |
| Normal vector flipping       | `f`키     |

특이 사항

* 파일 저장을 하면 실행할 때에 넣어준 파일을 **덮어쓴다**.
* 실행중에 cross section을 추가/삭제 하거나 cross section 내의 control point를 추가/삭제 할 수는 없다.
* 마우스 왼쪽 버튼과 오른쪽 버튼은 구분하지 않는다.
* 마우스 down 할 때에만 modifier(`alt`, `ctrl`, `shift`)키가 눌린지 확인하며, 그 이후 드래그를 할 때에는 down 했을 때의 값을 유지한다. 즉, 마우스 드래그를 시작하기 전에 키를 눌러야 하며, 드래그 중에 계속 키를 누른 채로 유지할 필요는 없다.
* 키는 소문자 기준이므로 Caps Lock이 눌리지 않았는지 주의한다.

## 3. 구현

### 3-1. 개요

모든 기본 스펙과 몇가지 추가 스펙이 구현되어 있다.
다음은 구현되어 있는 기능의 목록이다.

* Data 파일을 읽어서 파싱한다.
* 각 cross section에 대해 closed curve를 만든다.
  * Catmull-Rom spline
  * B-spline
  * Natural spline
* 각 curve를 잇는 generalized Catmull-Rom spline을 만든다.
* Cross section들의 일련의 transformations로 generalized Catmull-Rom spline을 만든다.
  * Scaling factors
  * Unit quaternions
  * 3D positions
* 만들어진 swept surface를 polygonal(triangle) mesh로 만들어 보여준다.
* 모델을 viewing 할 수 있다. (Assignment #2)
* Cross section의 control points와 transformations를 수정하여 파일로 저장할 수 있다.

주로 `/surface/` 디렉토리 밑의 파일들에 구현되어 있다.

* `__init__.py`: 비어 있다.
* `__main__.py`: glut window를 띄우는 등 프로그램의 시작점이다.
* `swept.py`: swept surface를 생성하는 알고리즘이 구현되어 있다.
* `cross.py`: editing 모드의 기능들이 구현되어 있다.
* `trans.py`: transforming 모드의 기능들이 구현되어 있다.
* `data.py`: data 파일 파싱, 저장 등의 기능을 한다.
* `*.txt|*.dat`: 테스트용 data 파일들이다.

그 외에, Viewing을 위해 `/viewer/camera.py`를 참조하고,
Quaternion 연산을 위해 `/viewer/quaternion.py`, `/jhm/quaternion.py`를 참조한다.

### 3-2. 상세

각 cross section에 대해 closed curve를 만들 때,
B-spline은 parameterized function을 matrix form으로 계산하였다.
Catmull-Rom spline은 De Casteljau algorithm을 사용하였다.
Natural spline은 control points에 matrix를 곱하여 B-spline으로 바꾸어 구했다.

Editing 모드에서는 orthogonal projection을 하였다.
모든 control points가 `[-1,1],[-1,1]` 범위에 들어오도록
해당 cross section의 scaling factor를 조정해주었다.

Transformation factors를 generalized Catmull-Rom splining 할 때,
De Casteljau algorithm을 사용하였다. Quaternion에도 적용할 수 있었다.
Quaternion 구현(slerp 등)은 교수님의 MATHCLASS를 포팅하여 사용했다.

Transforming 모드는 추가 스펙이므로 자세한 구현 설명은 생략한다.

Mesh는 어떤 cross section 상의 연속된 두 interpolated points와
그에 대응되는 다음 cross section의 두 points를 가지고
두 개의 triangle로 만들었다.

Data 파일 포맷은 공백 라인과 #으로 시작하는 주석을 가질 수 있도록 파싱하였다.

(문서 끝)

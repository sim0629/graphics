# 컴퓨터 그래픽스 - 숙제2

2015 봄 학기  
3D Viewer  
2009-11744 심규민

## 1. 실행

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
git checkout hw2
```

코드를 zip 파일로 가지고 있을 경우, 압축을 푼다.

```bash
unzip hw2.zip -d graphics
cd graphics
```

다음 명령어로 필요한 파이썬 패키지를 설치한다.
이 명령어는 환경에 따라 `sudo`로 실행해야 할 수도 있다.

```bash
pip install -r requirements.txt
```

다음 명령어로 3D Viewer를 실행한다.

```bash
python viewer
```

`esc`키를 눌러 종료할 수 있다.

## 2. 조작

| 동작         | 방법                              |
|--------------|-----------------------------------|
| Rotation     | 마우스 드래그                     |
| Translation  | `shift`키를 누른 채 마우스 드래그 |
| Dolly in/out | `w`/`s`키                         |
| Zoom in/out  | `d`/`a`키                         |
| Show all     | `space`키                         |
| Seek         | `ctrl`키를 누른 채 마우스 클릭    |

특이 사항

* 마우스 왼쪽 버튼과 오른쪽 버튼은 구분하지 않는다.
* 마우스 down 할 때에만 `shift`키가 눌린지 확인하며, 그 이후 드래그를 할 때에는 down 했을 때의 값을 유지한다. 즉, 계속 키를 누른 채로 유지할 필요는 없다.
* `ctrl`키가 `shift`키 보다 우선순위가 높다. 즉, 둘을 같이 누른 채 마우스 down을 하면 seek 동작을 한다.
* 키는 소문자 기준이므로 Caps Lock이 눌리지 않았는지 주의한다.

## 3. 구현

`/viewer/` 디렉토리 밑의 파일들에 구현되어 있다.

* `__init__.py`: 비어 있다.
* `__main__.py`: glut window를 띄우는 등 프로그램의 시작점이다.
* `camera.py`: viewer의 주요 기능들이 구현되어 있다.
* `quaternion.py`: orientation 및 rotation을 위한 quaternion 구현체이다.
* `wavefront.py`: wavefront `.obj` 파일로부터 3D 모델을 읽어들일 수 있는 `Mesh` 클래스가 구현되어 있다. `.obj` 포맷의 일부만 지원한다.
* `*.obj`: 테스트용 모델들이다.

### Rotation

중심이 reference point이고, near plane에 접하는 virtual trackball을 만들었다.
마우스 down 했을 때 camera position에서 클릭한 점으로 나아가는 ray가 trackball과 만나는 점과,
마우스 move 할 때의 trackball과 만나는 점을 구하고,
reference point에서 두 점에 이르는 각각의 vector 둘을 통해 rotation을 구하고,
reference point에 대한 camera position과 up vector를 rotate 하였다.
ray가 trackball의 바깥으로 나아가 trackball과의 교점이 없는 경우는 ray에서 trackball에 이르는 가장 가까운 점이 찍혔다고 가정하였다.

### Translation

near plane 상에서 viewing coordinate의 두 축을 따라 움직일 수 있다.
camera position과 reference point를 동시에 translate 한다.

### Dolly in/out

reference point를 향해 camera position이 가까워지거나 멀어진다.
reference point가 near plane 보다 가까워지거나 far plane 보다 멀어지지 않도록 했다.

### Zoom in/out

perspective angle이 줄어들거나 늘어난다.
angle이 1도 보다 작아지거나 180도 보다 커지지 않도록 했다.

### Show all

모델의 중심으로 seek 한 뒤, 모델이 화면에 맞게 다 보이도록 dolly out(in) 한다.
모델의 중심은 모델의 bounding box의 중심으로 하였다.
모델이 다 보이도록 하는 것은 bounding box의 여덟 꼭짓점이 near plane의 clipping window에 다 들어오도록 하였다.

처음 상태에서 마지막 상태가 될 때까지 24 frame 동안 animate 한다.
animate 도중에는 배경을 회색으로 칠하고, 다른 입력을 받지 않는다.

### Seek

camera position에서 클릭한 점으로 나아가는 ray에 대해, mesh의 모든 triangle과의 교점을 찾고,
camera position에서 가장 가까운 교점을 택하여 reference point로 삼는다.
교점이 없을 경우에는 아무 동작도 하지 않는다.
reference point를 바꾸고 up vector를 다시 계산하여 갱신해준다.

show all과 마찬가지로 animate 한다.


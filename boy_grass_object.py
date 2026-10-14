from pico2d import *
import random


# Game object class here
class Grass:
    def __init__(self): #init은 생성자 함수, self는 생성된 객체를 가리키는 더미 변수
        self.image = load_image('grass.png')

    def draw(self): # 멤버 함수는 항상 첫번째 인자가 self(자기 자신을 그림)
        self.image.draw(400, 30)

    def update(self): # 잔디는 움직이지 않으므로 할 일 없음
        pass

class Boy:
    def __init__(self):
        self.x, self.y = random.randint(100, 700), 90 # 소년의 처음 위치
        self.frame = random.randint(0, 7) # 현재 보여 줄 애니메이션 프레임 번호
        self.image = load_image('run_animation.png')

    def update(self): # 소년의 위치와 애니메이션 갱신
        self.frame = (self.frame + 1) % 8 # 0~7번 프레임 반복
        self.x += 5 # 오른쪽으로 5만큼 이동

    def draw(self): # 소년을 하면에 그림
        self.image.clip_draw(self.frame*100, 0, 100, 100, self.x, self.y)

class Zombie:
    def __init__(self):
        self.x, self.y = 100, 170
        self.frame = 0
        self.image = load_image('zombie_run_animation.png')
    def update(self):
        self.frame = (self.frame + 1) % 10
        self.x += 5
    def draw(self):
        frame_width = self.image.w // 10
        frame_height = self.image.h
        self.image.clip_draw(self.frame * frame_width, 0, frame_width, frame_height,
        self.x, self.y, frame_width // 2, frame_height // 2)

class Ball:
    def __init__(self, speed):
        self.x, self.y = random.randint(10, 750), 53
        self.image = load_image('ball21X21.png')
        self.speed = speed
        self.top = False
        self.up = False
        size = random.randint(1, 4)

        if size < 3:
            self.frame_width = self.image.w // size
            self.frame_height = self.image.h // size
        else:
            self.frame_width = self.image.w * 2
            self.frame_height = self.image.h * 2

    def update(self):
        if self.top == False:
            self.y += self.speed
            if self.y > 550:
                self.top = True
                self.speed = self.speed // 2

        elif self.top == True:
            if self.up == False:
                self.y -= self.speed
                if self.y < 500:
                    self.up = True
                    
            elif self.up == True:
                self.y += self.speed
                if self.y > 550:
                    self.up = False

    def draw(self):
        self.image.clip_draw(0, 0, self.image.w, self.image.h, self.x, self.y,
                              self.frame_width, self.frame_height)
        

def reset_world():
    global running
    global world
    running = True
    world = []

    grass = Grass() # Grass 클래스 이용해서 grass 객체 생성
    world.append(grass)

    team = [Boy() for i in range(11)]
    world += team

    zombie = Zombie()
    world.append(zombie)

    balls = [Ball(i + 5) for i in range(20)]
    world += balls

def update_world(): # 객체 상태 갱신
    for o in world:
        o.update()
  

def render_world(): # 현재 게임 화면 그리기
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


open_canvas()

reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)

close_canvas()
# Import
import pygame, sys
from pygame.locals import*

# CONSTANT
WHITE = 255, 255, 255  # RGB颜色
BLACK = 0, 0, 0  # RGB颜色

# initialize
pygame.init()

# 屏幕尺寸和模式设置
vInfo = pygame.display.Info()
# size = width, height = vInfo.current_w, vInfo.current_h  # 窗口大小
# flags = pygame.FULLSCREEN
flags = pygame.RESIZABLE
fps = 50  # Frames per second 每秒帧率参数
print("[SCREENSIZE]: Max Screen width and height", vInfo.current_w, vInfo.current_h)
size = width, height = (500, 300)
screen = pygame.display.set_mode(size, flags)
print("[SCREENSIZE]: Width and height", size)
still = False
ifClicked = False

# 窗口标题和图标
pygame.display.set_caption("Capture the Monster")
icon = pygame.image.load("icon.jfif")
pygame.display.set_icon(icon)

# 游戏内容# 游戏内容
speed = [2, 2]  # x和y轴的速度
target_img = pygame.image.load("Pmonster.jfif")
targetSize = (targetWidth, targetHeight) = (100, 100)
target_img = pygame.transform.scale(target_img, targetSize)
targetRect = target_img.get_rect()

# Timer
clock = pygame.time.Clock()

# Task Response
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:  #键盘按下
            if event.unicode == "":
                print("[KEYDOWN]:", "#", event.key, event.mod)
            else:
                print("[KEYDOWN]:", event.unicode, event.key, event.mod)
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key == pygame.K_LEFT:
                speed[0] = speed[0] if speed[0] == 0 else (abs(speed[0])-1)*int(speed[0]/abs(speed[0]))
            elif event.key == pygame.K_RIGHT:
                speed[0] = speed[0]+1 if speed[0] > 0 else speed[0]-1
            elif event.key == pygame.K_DOWN:
                speed[1] = speed[1] if speed[1] == 0 else (abs(speed[1]) - 1) * int(speed[1] / abs(speed[1]))
            elif event.key == pygame.K_UP:
                speed[1] = speed[1]+1 if speed[1] > 0 else speed[1]-1
        elif event.type == pygame.MOUSEBUTTONDOWN:  # 按下鼠标
            print("[MOUSEBUTTONDOWN]:", "event.pos:", event.pos, "event.button:", event.button)
            print("[MOUSEBUTTONDOWN]:", "targetRect.left,right, top and bottom", targetRect.left, targetRect.right,\
                  targetRect.top, targetRect.right)
            ifClicked = (event.pos[0] > targetRect.left) and (event.pos[0] < targetRect.right) and \
                        (event.pos[1] > targetRect.top) and event.pos[1] < targetRect.bottom
            if event.button == 1 and ifClicked:
                still = True
        elif event.type == pygame.MOUSEMOTION:  # 鼠标移动
            print("[MOUSEMOTION]:", "event.pos:", event.pos, "event.rel:", event.rel, "event.buttons:", event.buttons)
            if event.buttons[0] == 1 and ifClicked:
                targetRect = targetRect.move(event.rel[0], event.rel[1])
        elif event.type == pygame.MOUSEBUTTONUP:  #松开鼠标
            print("[MOUSEBUTTONUP]:", "event.pos:", event.pos, "event.button:", event.button)
            if event.button == 1:
                still = False
                ifClicked = False
                targetRect = targetRect.move(speed[0], speed[1])
        elif event.type == pygame.VIDEORESIZE:
            size = width, height = pygame.display.get_window_size()
            print("Current Size:", size)
            if targetRect.right > width:
                targetRect.right = width
            if targetRect.bottom > height:
                targetRect.bottom = height

    if pygame.display.get_active() and not still:  # 如果窗体不是最小化且小球不在静止状态
        targetRect = targetRect.move(speed[0], speed[1])

    if targetRect.left < 0 or targetRect.right > width:
        speed[0] = -speed[0]
    if targetRect.top < 0 or targetRect.bottom > height:
        speed[1] = -speed[1]

# Fresh the screen
    screen.fill(WHITE)
    screen.blit(target_img, targetRect)
    pygame.display.update()
    clock.tick(fps)


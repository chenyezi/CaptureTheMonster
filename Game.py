# -*- coding = utf-8 -*-
# @Time: 2021/7/21 16:48
# @Author: Yezi Chen
# @File: demo1.py
# @Platform: PyCharm

import pygame
import sys
from pygame import *
import pygame.freetype
import random

pygame.init()

# load
target_img = pygame.image.load("Pmonster.jfif")
cage_img = pygame.image.load("cage2.jpeg")
f1 = pygame.freetype.Font("C://Windows//Fonts//msyh.ttc", 36)
icon = pygame.image.load("icon.jfif")

size = width, height = (500, 300)
flags = pygame.RESIZABLE
screen = pygame.display.set_mode(size, flags)
print("[SCREENSIZE]: Width and height", size)

# 窗口标题和图标
pygame.display.set_caption("抓捕小怪兽")
pygame.display.set_icon(icon)

# 颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = pygame.Color("red")
GOLD = 255, 251, 0
PURPLE = 128, 0, 128

# 小怪物
speed = [2, 2]  # x和y轴的速度
targetSize = (targetWidth, targetHeight) = (100, 100)
target_img = pygame.transform.scale(target_img, targetSize)
targetRect = target_img.get_rect()

# 笼子
cageSize = (cageWidth, cageHeight) = (200, 200)
cage_img = pygame.transform.scale(cage_img, cageSize)
cageRect = cage_img.get_rect()
cageRect.left = 10
cageRect.top = 0.5 * height - 0.5 * cageHeight

rectSize = rectWidth, rectHeight = (240, 130)

f1surf, f1rect = f1.render("抓捕小怪兽", fgcolor=RED, size=30)
f2surf, f2rect = f1.render("单击左键，长按拉拽小怪兽进笼子", fgcolor=RED, size=15)
f3surf, f3rect = f1.render("捕获成功后，单击右键进入下一关", fgcolor=RED, size=15)

# Timer
clock = pygame.time.Clock()
fps = 100  # Frames per second 每秒帧率参数

isClicked, isCaptured, isStill, isOver = False, False, False, False
num, ms, time, score = 0, 0, 0, 0

# Task Response
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:  # 键盘按下
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
            # print("[MOUSEBUTTONDOWN]:", "event.pos:", event.pos, "event.button:", event.button)
            isClicked = (event.pos[0] > targetRect.left) and (event.pos[0] < targetRect.right) and \
                        (event.pos[1] > targetRect.top) and (event.pos[1] < targetRect.bottom)
            print("isClicked:", isClicked)

            if event.button == 1 and isClicked and not isCaptured and not isStill:  #点到了怪兽
                isStill = True

            if event.button == 1 and isOver:  #游戏结束的时候，按左键会重新开始游戏
                num, ms, time, score = 0, 0, 0, 0
                isClicked, isCaptured, isStill, isOver = False, False, False, False
                speed[0], speed[1] = 2, 2
                f5rect = f1.render_to(screen, (width - 30, height - 40), "0", fgcolor=BLACK, size=15)

        elif event.type == pygame.MOUSEMOTION:  # 鼠标移动
            # print("[MOUSEMOTION]:", "event.pos:", event.pos, "event.rel:", event.rel, "event.buttons:", event.buttons)
            if isStill and not isCaptured:
                targetRect = targetRect.move(event.rel[0], event.rel[1])

        elif event.type == pygame.MOUSEBUTTONUP:  # 松开鼠标
            # print("[MOUSEBUTTONUP]:", "event.pos:", event.pos, "event.button:", event.button)
            if isStill and not isCaptured and event.button == 1:  # 不知道有没有放进笼子里，现在判断一下
                isCaptured = (event.pos[0] > cageRect.left) and (event.pos[0] < cageRect.right) and \
                             (event.pos[1] > cageRect.top) and (event.pos[1] < cageRect.bottom)
                print("isCaptured:", isCaptured)

                if isCaptured:
                    num = num + 1
                    score = str(num * 100)
                    f5rect = f1.render_to(screen, (width - 30, height - 40), score, fgcolor=BLACK, size=15)
                    speed[0] = (abs(speed[0]) + 2 * num) * speed[0]/abs(speed[0])
                    speed[1] = (abs(speed[1]) + 4 * num) * speed[1]/abs(speed[1])
                    targetRect.left = int(width * random.random())
                    targetRect.top = int(height * random.random())

                if not isCaptured:
                    isStill = False
                    isClicked = False

            elif isCaptured and event.button == 3:  # 抓到了，还原进入下一关
                print("Current Stage:", num)
                isStill, isClicked, isCaptured = False, False, False

        elif event.type == pygame.VIDEORESIZE:  # 更新宽和高
            size = width, height = pygame.display.get_window_size()
            cageRect.centery = 0.5 * height

# 如果目标撞上边缘或在窗口外，把目标移动到界面内，并朝相反方向移动
    if targetRect.left < 0:
        speed[0] = -speed[0]
        targetRect.left = 0
    elif targetRect.right > width:
        speed[0] = -speed[0]
        targetRect.right = width
    if targetRect.top < 0:
        speed[1] = -speed[1]
        targetRect.top = 0
    elif targetRect.bottom > height:
        speed[1] = -speed[1]
        targetRect.bottom = height

    if pygame.display.get_active() and not isStill:  # 如果窗体不是最小化且小球不在静止状态
        targetRect = targetRect.move(speed[0], speed[1])

    ms = ms+1
    time = int(ms/fps)

    screen.fill(WHITE)
    if time < 10:  # 10秒内
        r1rect = pygame.draw.rect(screen, BLACK, ((width - 260, 5), rectSize), 2)
        screen.blit(f1surf, (width - 250, 20))
        screen.blit(f2surf, (width - 250, 80))
        screen.blit(f3surf, (width - 250, 100))

    if time < 30:  # 游戏时长30s
        score = str(num * 100)
        f4surf, f4rect = f1.render("分数: "+score, fgcolor=BLACK, size=15)
        f6surf, f6rect = f1.render("时间: "+str(time), fgcolor=BLACK, size=15)
        screen.blit(f4surf, (width - 100, height - 100))
        screen.blit(f6surf, (width - 100, height - 80))
        screen.blit(cage_img, cageRect)

        if not isCaptured:
            screen.blit(target_img, targetRect)

    else:  # 30s
        screen.fill(WHITE)
        f8surf, f8rect = f1.render("分数:"+score, fgcolor=RED, size=30)
        screen.blit(f8surf, (0.5 * width - 50, 0.5 * height - 50))
        isOver = True

    # Fresh the screen
    pygame.display.update()
    clock.tick(fps)

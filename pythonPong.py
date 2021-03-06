from tkinter import *
import random

#score
player_1_score = 0
player_2_score = 0
#настроки окна
root = Tk()
root.title('PythonPong')

#настройки ракеток
pad_width = 10
pad_height = 100
left_pad_speed = 0
right_pad_speed = 0
pad_speed = 20

#настройки игрового поля
WIDTH = 900
HEIGHT = 300
right_line_distance = WIDTH - pad_width


#настроки мяча
ball_radius = 30
ball_x_change = 2
ball_y_change = 0
ball_speed_up=1.05
ball_max_speed=30
ball_x_speed = 10
ball_y_speed =5
initial_speed = 20

#настройки анимации
c = Canvas(root, width=WIDTH, height=HEIGHT, background = "#003300")
c.pack()

#настройки элементов поля
c.create_line(pad_width, 0, pad_width, HEIGHT, fill='white') #левая линия
c.create_line(WIDTH-pad_width, 0, WIDTH-pad_width, HEIGHT, fill='white') #правая линия
c.create_line(WIDTH//2, 0, WIDTH//2, HEIGHT, fill='white') #центральная
p_1_text = c.create_text(WIDTH-WIDTH/6, pad_height/4, text = player_1_score, font='Arial 20')
p_2_text = c.create_text(WIDTH/6, pad_height/4, text = player_2_score, font='Arial 20')

#создаем мяч
BALL = c.create_oval(WIDTH/2-ball_radius/2, HEIGHT/2-ball_radius/2, WIDTH/2+ball_radius/2, HEIGHT/2+ball_radius/2, fill='white')

#создаем левую ракетку
LEFT_PAD = c.create_line(pad_width/2, 0 , pad_width/2, pad_height, width = pad_width, fill = 'yellow')

#создаем правую ракетку
RIGHT_PAD = c.create_line(WIDTH-pad_width/2, 0 , WIDTH-pad_width/2, pad_height, width = pad_width, fill = 'yellow')
    
#function bounce of the ball
def bounce(action):
    global ball_x_speed, ball_y_speed
    if action == "strike":
        ball_y_speed = random.randrange(0,5)
        if abs(ball_x_speed) < ball_max_speed:
            ball_x_speed *= -ball_speed_up
        else:
            ball_x_speed = -ball_x_speed
    else:
            ball_y_speed = -ball_y_speed

#update score
def update_score(player):
    global player_1_score, player_2_score
    if player == 'right':
        player_1_score += 1
        c.itemconfig(p_1_text, text= player_1_score)
    else:
        player_2_score += 1
        c.itemconfig(p_2_text, text = player_2_score)
        
#respawn ball
def respawn_ball():
    global ball_x_speed
    c.coords(BALL, WIDTH/2 - ball_radius/2, HEIGHT/2 - ball_radius/2, WIDTH + ball_radius/2, HEIGHT/2 + ball_radius/2)
    ball_x_speed = -(ball_x_speed * - initial_speed) / abs(ball_x_speed)


#функция движения мяча
def move_ball():
    #c.move(BALL, ball_x_change, ball_y_change)
    ball_left, ball_top, ball_right, ball_bot = c.coords(BALL)
    ball_center = (ball_top + ball_bot)/2
    # vertical bounce
    if ball_right + ball_x_speed < right_line_distance and ball_left + ball_x_speed > pad_width:
        c.move(BALL, ball_x_speed, ball_y_speed)
    elif ball_right == right_line_distance or ball_left == pad_width:
        if ball_right > WIDTH/2:
            if c.coords(RIGHT_PAD)[1] < ball_center < c.coords(RIGHT_PAD)[3]:
                bounce('strike')                  
            else:
                update_score('left')
                respawn_ball()
        else:
            if c.coords(LEFT_PAD)[1] < ball_center < c.coords(LEFT_PAD)[3]:
                bounce('strike')
            else:
                update_score('right')
                respawn_ball()
    else:
        if ball_right > WIDTH/2:
            c.move(BALL, right_line_distance - ball_left+pad_width, ball_y_speed)
        else:
            c.move(BALL, -ball_left+pad_width, ball_y_speed)
    if ball_top + ball_y_speed < 0 or ball_bot+ball_y_speed > HEIGHT:
        bounce("ricochet")

#функция движения ракеток
def move_pads():
    PADS ={LEFT_PAD:left_pad_speed, RIGHT_PAD:right_pad_speed}
    for pad in PADS:
        c.move(pad, 0, PADS[pad])
        if c.coords(pad)[1]<0:
            c.move(pad, 0, -c.coords(pad)[1])
        elif c.coords(pad)[3]>HEIGHT:
            c.move(pad, 0, HEIGHT-c.coords(pad)[3])
        

#основная функция движения
def main():
    move_ball()
    move_pads()
    root.after(30, main)
    
c.focus_set()

#function of keyboard buttons
def movement(event):
    global left_pad_speed, right_pad_speed

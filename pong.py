# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [ WIDTH/2, HEIGHT/2]
ball_vel= [1, 1]
paddle1_pos=HEIGHT/2
paddle2_pos=HEIGHT/2
paddle1_vel =0
paddle2_vel =0
score1=0
score2=0

# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [ WIDTH/2, HEIGHT/2]
    ball_vel= [1, 1]
    if direction == LEFT:
        ball_vel[0] = random.randrange(-240, -120)/ 60
        ball_vel[1] = random.choice([random.randrange(60, 180), random.randrange(-180, -60)])/ 60
    elif direction == RIGHT:
        ball_vel[0] = random.randrange(120, 240)/ 60
        ball_vel[1] = random.choice([random.randrange(60, 180), random.randrange(-180, -60)])/ 60


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1=0
    score2=0
    direct = random.choice ([LEFT, RIGHT])
    spawn_ball(direct)

def button_handler():
    new_game()


def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, key

    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_text(str(score2)+"/"+str(score1), (275, 50), 42, 'Red')
    # update ball
    ball_pos[0]+= ball_vel[0]
    ball_pos[1]+= ball_vel[1]

    #make the ball bounce when it collides with the top and the bottom
    if ball_pos [1] >= ((HEIGHT-1)- BALL_RADIUS)  or ball_pos [1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]

    #make the ball bounce when it collides with the gutters
    if ball_pos [0] >= (WIDTH-1-PAD_WIDTH- BALL_RADIUS) :
       if (paddle2_pos -40 <= ball_pos[1] <= paddle2_pos+40) :
           ball_vel[0] = - ball_vel[0]*1.1

       else:
           ball_vel[0] = - ball_vel[0]
           spawn_ball(LEFT)
           score1=score1+1
           return score1

    elif ball_pos [0] <= (BALL_RADIUS+ PAD_WIDTH):
        if (paddle1_pos -40 <= ball_pos[1] <= paddle1_pos+40) :
           ball_vel[0] = - ball_vel[0]*1.1
        else:
           ball_vel[0] = - ball_vel[0]
           spawn_ball(RIGHT)
           score2=score2+1
           return score2

    #draw the ball in the middle of the canvas
    c.draw_circle(ball_pos, BALL_RADIUS, 2, '#FF9C00', '#FFFF00')

    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos-paddle1_vel >= HALF_PAD_HEIGHT and paddle1_pos-paddle1_vel <=HEIGHT- HALF_PAD_HEIGHT :
       paddle1_pos-= paddle1_vel
    if paddle2_pos-paddle2_vel >= HALF_PAD_HEIGHT and paddle2_pos-paddle2_vel <=HEIGHT- HALF_PAD_HEIGHT :
       paddle2_pos-= paddle2_vel



    c.draw_line([HALF_PAD_WIDTH, paddle1_pos +HALF_PAD_HEIGHT], [HALF_PAD_WIDTH, paddle1_pos -HALF_PAD_HEIGHT], PAD_WIDTH, '#C400CC')
    c.draw_line([WIDTH-HALF_PAD_WIDTH, paddle2_pos +HALF_PAD_HEIGHT], [WIDTH-HALF_PAD_WIDTH, paddle2_pos -HALF_PAD_HEIGHT], PAD_WIDTH, '#C400CC')
    # draw scores
def constrain(value, lower_bound, upper_bound):
    return min(max(lower_bound, value), upper_bound)

def keydown(key):
    global   paddle1_vel, paddle2_vel
    acc=1
    if key == simplegui.KEY_MAP ['w']:
       paddle1_vel =1
    elif key == simplegui.KEY_MAP ['s']:
        paddle1_vel =-1
    if key == simplegui.KEY_MAP ['up']:
       paddle2_vel =1
    elif key == simplegui.KEY_MAP ['down']:
        paddle2_vel =-1

def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP ['w']:
       paddle1_vel =0
    elif key == simplegui.KEY_MAP ['s']:
        paddle1_vel =0
    if key == simplegui.KEY_MAP ['up']:
       paddle2_vel =0
    elif key == simplegui.KEY_MAP ['down']:
        paddle2_vel =0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart', button_handler)

# start frame
new_game()
frame.start()

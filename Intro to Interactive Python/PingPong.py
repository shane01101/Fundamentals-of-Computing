#Shane Honanie
#http://www.codeskulptor.org/#user44_llCFjbF5p0_5.py

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
ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [0, 0]
score1 = 0
score2 = 0
score1_pos = [135,40]
score2_pos = [435,40]
paddle1_pos = [0, HEIGHT/2-HALF_PAD_HEIGHT]
paddle2_pos = [WIDTH-PAD_WIDTH, HEIGHT/2-HALF_PAD_HEIGHT]
paddle1_vel = [0,0]
paddle2_vel = [0,0]

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    
    if(direction == 0):
        ball_vel = [-2, -1]
    else:
        ball_vel = [2, -1]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    num = random.randrange(0,2)
    paddle1_pos = [0, HEIGHT/2 - HALF_PAD_HEIGHT]
    paddle2_pos = [WIDTH - PAD_WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT]
    score1 = 0
    score2 = 0
    spawn_ball(num)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "Green")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos[1] += paddle1_vel[1]
    paddle2_pos[1] += paddle2_vel[1]
    
    if(paddle1_pos[1] < 0):
        paddle1_pos[1] = 0
    elif(paddle1_pos[1] > HEIGHT - PAD_HEIGHT ):
        paddle1_pos[1] = HEIGHT - PAD_HEIGHT
        
    if(paddle2_pos[1] < 0):
        paddle2_pos[1] = 0
    elif(paddle2_pos[1] > HEIGHT - PAD_HEIGHT ):
        paddle2_pos[1] = HEIGHT - PAD_HEIGHT
        
    
    # draw paddles
    canvas.draw_polygon([[paddle1_pos[0], paddle1_pos[1]],
                         [paddle1_pos[0] + PAD_WIDTH, paddle1_pos[1]],
                         [paddle1_pos[0] + PAD_WIDTH, paddle1_pos[1] + PAD_HEIGHT],
                         [paddle1_pos[0], paddle1_pos[1] + PAD_HEIGHT]], 1, 'White', 'Blue')
    
    canvas.draw_polygon([[paddle2_pos[0], paddle2_pos[1]],
                         [paddle2_pos[0] + PAD_WIDTH, paddle2_pos[1]],
                         [paddle2_pos[0] + PAD_WIDTH, paddle2_pos[1] + PAD_HEIGHT],
                         [paddle2_pos[0], paddle2_pos[1] + PAD_HEIGHT]], 1, 'White', 'Blue')
    
    # determine whether paddle and ball collide    
    if(ball_pos[0] <= BALL_RADIUS + PAD_WIDTH):
        if (ball_pos[1] > paddle1_pos[1] 
        and ball_pos[1] < paddle1_pos[1] + PAD_HEIGHT):
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] += .5
        else:
            score2 += 1
            num = random.randrange(0,2)
            spawn_ball(1)
    
    if(ball_pos[0] >= WIDTH - (BALL_RADIUS + PAD_WIDTH)):
        if (ball_pos[1] > paddle2_pos[1] 
        and ball_pos[1] < paddle2_pos[1] + PAD_HEIGHT):
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] -= .5
        else:
            score1 += 1
            num = random.randrange(0,2)
            spawn_ball(0)
            
    #top/bottom collisions    
    if(ball_pos[1] <= BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]
        
    if(ball_pos[1] >= HEIGHT- BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]
            

    # draw scores
    canvas.draw_text(str(score1), score1_pos, 48, 'Orange')
    canvas.draw_text(str(score2), score2_pos, 48, 'Orange')
        
def keydown(key):
    acc = 8
    if key==simplegui.KEY_MAP["up"]:
        paddle1_vel[1] -= acc
    elif key==simplegui.KEY_MAP["down"]:
        paddle1_vel[1] += acc
    elif key==simplegui.KEY_MAP["w"]:
        paddle2_vel[1] -= acc
    elif key==simplegui.KEY_MAP["s"]:
        paddle2_vel[1] += acc
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel = [0,0]
    paddle2_vel = [0,0]

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game, 100)

# start frame
new_game()
frame.start()

# Shane Honanie
# http://www.codeskulptor.org/#user44_jyVh6w0oJf_2.py

# define global variables
import simplegui

width = 200
height = 150
interval = 100
attempts = 0
score = 0
time_label = "0:00.0"
time = 0
game_active = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global time_label
    minute = t/600
    second = t/10%60
    m_sec = t %10
    time_label = str(minute) + ":%02d" %  + second + "." + str(m_sec)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_button_handler():
    global game_active
    game_active = True
    timer.start()
    
def stop_button_handler():
    global attempts
    global score
    global game_active
    timer.stop()

    if (game_active):
        attempts += 1
        if (time % 10 == 0):
            score += 1
    game_active = False
    
def reset_button_handler():
    global attempts
    global score
    global time
    global time_label
    global game_active
    game_active = False
    time = 0
    attempts = 0
    score = 0
    time_label = "0:00.0"
    
# define event handler for timer with 0.1 sec interval
def tick():
    global time
    time += 1
    return format(time)

# define draw handler
def draw(canvas):
    canvas.draw_text(str(score) + "/" + str(attempts), [150,20], 24, "Green")
    canvas.draw_text(time_label, [50,100], 36, "White")
    
# create frame
frame = simplegui.create_frame("Home", width, height)

# register event handlers
frame.set_draw_handler(draw)
timer = simplegui.create_timer(interval, tick)
start = frame.add_button("Start", start_button_handler, 100)
stop = frame.add_button("Stop", stop_button_handler, 100)
reset = frame.add_button("Reset", reset_button_handler, 100)

# start frame
frame.start()


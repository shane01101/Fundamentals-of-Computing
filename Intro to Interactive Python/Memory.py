# Shane Honanie
# http://www.codeskulptor.org/#user44_IFoPaQdPLs_2.py
# implementation of card game - Memory

import simplegui
import random
turns = 0

# helper function to initialize globals
def new_game():
    global deck
    global deck_visibility
    global state
    global exposed
    global turns
    state = 0
    turns = 0
    deck = []
    exposed = []
    deck_visibility = []
    for i in range(8):
        deck.append(i)
        deck.append(i)
        deck_visibility.append("False")
        deck_visibility.append("False")
    
    random.shuffle(deck)
     
# define event handlers
def mouseclick(pos):
    global state
    global deck_visibility
    global exposed
    global turns
    card_clicked = pos[0] / 50
    if(card_clicked not in exposed):
        if state == 0:
            state = 1
            exposed.append(card_clicked)
        elif state == 1:
            state = 2
            exposed.append(card_clicked)
        elif state == 2:
            state = 1
            turns += 1
            temp1 = exposed[len(exposed)-1]
            temp2 = exposed[len(exposed)-2]    

            if(deck[temp1] != deck[temp2]):
                deck_visibility[temp1] = "False"
                deck_visibility[temp2] = "False"
                exposed.pop()
                exposed.pop()
            exposed.append(card_clicked)

        for j in exposed:
            deck_visibility[j] = "True"
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    border = 50
    
    for i in range (16):
        canvas.draw_line((i*border, 0), (i*border, i*border*2), 1, 'Green')
      
        if(deck_visibility[i] == "True"):
            canvas.draw_text(str(deck[i]), (i*50+10, 75), 60, 'White')
            
        label.set_text("Turns = " + str(turns))

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = " + str(turns))

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
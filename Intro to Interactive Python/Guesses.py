#Shane Honanie
#http://www.codeskulptor.org/#user44_byj1UjdCng_1.py
import simplegui
import random
import math

num_range = 100
num_guesses = 7
comp_guess = -1
mode = 0

# helper function to start and restart the game
def new_game():
    global comp_guess
    global num_guesses
    
    if(mode == 0):
        num_guesses = 7
        num_range = 100
    else:
        num_guesses = 10
        num_range = 1000
        
    comp_guess = random.randrange(0, num_range)
    
    print "New game. Range is 0 to " + str(num_range)
    print "Number of remaining guesses is " + str(num_guesses) + "\n"


# define event handlers for control panel
def range100():
    global mode
    mode = 0
    new_game()

def range1000():
    global mode
    mode = 1
    new_game()
    
def input_guess(guess):
    global num_guesses
    num_guesses = num_guesses - 1
    
    print "Guess was " + str(guess)
    print "Number of remaining guesses is " + str(num_guesses)
    
    if(int(num_guesses) == 0):
        print "You loose!\n"
        new_game()
    elif(int(guess) == comp_guess):
        print "Correct!\n"
        new_game()
    elif(int(guess) > comp_guess):
        print "Lower!\n"
    elif(int(guess) < comp_guess):
        print "Higher!\n"
    
# create frame
f = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements and start frame
f.add_button("Range is [0, 100)", range100, 200)
f.add_button("Range is [0, 1000)", range1000, 200)
f.add_input("Enter a guess", input_guess, 200)

# call new_game 
new_game()

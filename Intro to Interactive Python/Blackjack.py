# Shane Honanie
# http://www.codeskulptor.org/#user44_Rst8h2pXxF_2.py
# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand_of_cards = []
        self.value = 0
        self.has_ace = False

    def __str__(self):
        s = "Hand Contains "
        for i in range(len(self.hand_of_cards)):
            s += str(self.hand_of_cards[i]) + " "
        return s
        
    def add_card(self, card):
        self.hand_of_cards.append(card)

    def get_value(self):
        self.value = 0
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        for i in range(len(self.hand_of_cards)):
            #print self.hand_of_cards[i].get_rank()
            #print VALUES[self.hand_of_cards[i].get_rank()]
            self.value += VALUES[self.hand_of_cards[i].get_rank()]
            #print self.hand_of_cards[i].get_rank()
            
            if self.hand_of_cards[i].get_rank() == 'A':
                self.has_ace = True
                #continue
                
        if self.has_ace and self.value+10 <= 21:
                self.value += 10    

        return self.value
        
   
    def draw(self, canvas, pos):
        for i in range(len(self.hand_of_cards)):
            self.hand_of_cards[i].draw(canvas, [pos[0]+CARD_SIZE[0]*i*1.25,pos[1]])
            
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck_of_cards = []
        
        for i in range(len(SUITS)):
            for j in range(len(RANKS)):
                self.deck_of_cards.append(Card(SUITS[i], RANKS[j]))

    def shuffle(self):
        random.shuffle(self.deck_of_cards)

    def deal_card(self):
        return self.deck_of_cards.pop()
    
    def __str__(self):
        s = "Deck Contains "
        for i in range(len(self.deck_of_cards)):
            s += str(self.deck_of_cards[i]) + " "
        return s    

#define event handlers for buttons
def deal():
    global outcome, in_play, deck, dealer, player, score

    deck = Deck()
    dealer = Hand()
    player = Hand()
    outcome = "Hit or stand?"
    
    if in_play:
        score -= 1
        outcome = "You lost!"
    
    in_play = True
    deck.shuffle()
    print deck
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    print deck
    print "Dealer: " + str(dealer)
    print "Player: " + str(player)
    

def hit():
    global player, in_play, outcome, score
    if in_play:
        if player.get_value() <= 21:
            player.add_card(deck.deal_card())

    if player.get_value() > 21 and in_play:
        in_play = False
        score -= 1
        outcome = "You have busted!"
       
    print "Player: " + str(player)  
    
       
def stand():
    global dealer, in_play, outcome, score
    print in_play
    if player.get_value() > 21 and not in_play:
        outcome = "You already busted!"
    
    while in_play and dealer.get_value() < 17:
        dealer.add_card(deck.deal_card())
    
    if in_play:
        in_play = False
        if dealer.get_value() > 21:
            outcome = "Dealer busted, You win!"
            score += 1
        elif player.get_value() > dealer.get_value():
            outcome = "You win!"
            score += 1
        else:
            outcome = "You loose!, new Deal?"
            score -= 1
        
    print "Player: " + str(player.get_value()) 
    print "Dealer: " + str(dealer.get_value()) 
        

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text('Blackjack', (50, 80), 36, 'Black')
    canvas.draw_text('Dealer', (50, 150), 36, 'Black')
    canvas.draw_text('Player', (50, 350), 36, 'Black')
    canvas.draw_text("Score: " + str(score), (350, 80), 36, 'Black')
    canvas.draw_text(outcome, (250, 350), 36, 'Black')
    
    #card = Card("S", "A")
    #card.draw(canvas, [300, 300])
    player.draw(canvas, [50,380])
    dealer.draw(canvas, [50,180])
    
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [85,227] , CARD_BACK_SIZE)


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
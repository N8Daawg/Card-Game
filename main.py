import random as rand, time, turtle as trtl
from copy import deepcopy

#asshole game code
''' TOGO LIST: 
1. ALLOW A PLAYER TO CHOOSE THEIR OWN PROBLEMS (CURRENT OBJECTIVE)
2. CREATE A BETTER AI FOR THE BOT TO CHOOSE CARDS WITH
3. EDIT CORDINATE POSITIONS SO THAT EVERY CARD IN HAND IS READABLE WITHOUT OVERLAP

'''

class game:
    def __init__(self):
        global player1, player2, player3, player4
        self.suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
        self.values = [
            "Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack",
            "Queen", "King"
        ]
        self.deck = []
        self.player_list = []
        self.gameover = False
        self.pile = []

        self.top_card_value = 0
        self.continue_game = True
        self.skip_turn = False



    
    def setup(self):
        update_player_positions()
        self.distribute_deck()

    def create_deck(self):
        for i in self.suits:
            for j in self.values:
                card = j + " of " + i
                self.deck.append(str(card))


    def shuffle(self):
        new_deck = []
        old_deck = self.deck
        length = len(old_deck)
        while len(new_deck) < length:
            i = rand.randint(0, (len(old_deck) - 1))
            card = (old_deck.pop(i))
            new_deck.append(card)
        self.deck = new_deck

    def distribute_deck(self):
        global Player, player1, turtle_dictionary
        #give each player 3 cards
        count = 0
        for player in self.player_list:
            for i in range(3):
                x = self.deck.pop(0)
                card = turtle_dictionary.get(x)
                #if isinstance(player, Player):
                card.showturtle()
                card.penup()
                card.goto(player.card_positions[i][0],
                          player.card_positions[i][1])
                player.face_down_cards.append(x)
            count += 1
        count = 0
        for player in self.player_list:
            for i in range(3):
                x = self.deck.pop(0)
                card = turtle_dictionary.get(x)
                flip_card_up(x)
                card.showturtle()
                card.penup()
                card.goto(player.card_positions[i][0],
                          player.card_positions[i][1])
                y = player.face_down_cards[i]
                card = turtle_dictionary.get(y)
                card.hideturtle()
                player.face_up_cards.append(x)

        
        #go clockwise giveing each player a card until the deck is empty
        x_coordinate = -400
        y_coordinate = -150
        for player in self.player_list:
            displacement = 75
            for i in range(4):
                card = self.deck.pop(0)
                x = turtle_dictionary.get(card)
                if isinstance(player, Player):
                    flip_card_up(card)
                x.penup()
                x.goto(x_coordinate + displacement, y_coordinate)

                player.deck.append(card)
                displacement += 75

            y_coordinate = 150
            player.organize_hand()
        

    def find_value(self, card):
        if ("Ace" in card):
            return (14)
        elif ("Jack" in card):
            return (11)
        elif ("Queen" in card):
            return (12)
        elif ("King" in card):
            return (13)
        else:
            card = card.split()
            if (int(card[0])) == 3:
                return int(self.top_card_value)

            elif (int(card[0])) == 2:
                self.top_card_value = 2
                return (int(card[0]))

            else:
                return (int(card[0]))

    def check_cards(self):
        if "10" in self.pile[0]:
            for card in self.pile:
                card = turtle_dictionary.get(card)
                card.goto(300,25)
            self.top_card_value = 0
            self.pile = []

        if (len(self.pile) > 4):
            if (self.find_value(self.pile[0]) == self.find_value(self.pile[1])
                    and self.find_value(self.pile[0]) == self.find_value(
                        self.pile[2]) and self.find_value(
                            self.pile[0]) == self.find_value(self.pile[3])):
                for card in self.pile:
                    card = turtle_dictionary.get(card)
                    card.goto(300,25)
                self.top_card_value = 0
                self.pile = []

    def show_top_card(self):
        for card in self.pile:
            if card == self.pile[0]:

                card = turtle_dictionary.get(card)
                card.showturtle()
            else:
                card = turtle_dictionary.get(card)
                card.hideturtle()

    def choose_card(self, player):
        if len(player.deck) > 0:
            x = 0
            while x < len(player.deck):
                #i = rand.randint(0,(len(player.deck))-1)
                player.current_card = player.deck[x]
                if self.find_value(player.current_card) >= self.top_card_value:
                    #index = player.deck.index(player.current_card)
                    #player.deck.pop(index)
                    print("{} drew: {}".format(player.name,
                                               player.current_card))
                    return
                x += 1

            print("{} cannot place a card".format(player.name))
            self.pick_up_deck(player)
            

        else:
            if len(player.face_up_cards) == 0:
                print("{} is down to their face down cards!!\n".format(
                    player.name))

                i = rand.randint(0, len(player.face_down_cards) - 1)
                
                player.current_card = player.face_down_cards.pop(i)
                flip_card_up(player.current_card)
                
            else:
                print("{} is down to their face up cards".format(player.name))

                x = 0
                while x < len(player.face_up_cards):
                    player.current_card = player.face_up_cards[x]
                    if self.find_value(
                            player.current_card) >= self.top_card_value:
                        card = player.face_down_cards[x]
                        card = turtle_dictionary.get(card)
                        card.showturtle()
                        player.face_up_cards.pop(x)
                        print("{} drew: {}".format(player.name,
                                                   player.current_card))
                        return
                    x += 1
                print("{} cannot place a card".format(player.name))
                self.pick_up_deck(player)
                

    def grab_cards(self, player, index):
        if len(self.deck) != 0:
            card = player.current_card

            #index = player.deck.index(card)
            #player.deck.pop(index)
            card = turtle_dictionary.get(card)

            x = self.deck.pop(0)
            card = turtle_dictionary.get(x)
            if isinstance(player, Player):
                flip_card_up(x)
            

            player.deck.insert(index, x)
            print("{} picked up the {} from the deck".format(player.name, x))

    def pick_up_deck(self, player):
        print("{} is picking up the pile".format(player.name))
        add_cards = self.pile.copy()
        player.deck += add_cards
        for card in self.pile:
            if isinstance(player, bot):
                flip_card_back(card)
            else:
                flip_card_up(card)
            card = turtle_dictionary.get(card)    
            card.showturtle()

        self.pile = []
        self.top_card_value = 0
        self.skip_turn = True

    def start_round(self, player):
        while self.continue_game == True:
            self.choose_card(player)
            if self.pile != []:
                if "Jack" in player.current_card and "Ace" in self.pile[0]:
                    self.test(player)
            if self.skip_turn == False:
                if self.find_value(player.current_card) >= self.top_card_value:
                    card = player.current_card
                    if len(player.deck) != 0:
                        index = player.deck.index(player.current_card)
                        player.deck.pop(index)
                    else:
                        index = 0   
                    
                    if isinstance(player, bot):
                        flip_card_up(card)
                    card = turtle_dictionary.get(card)
                    card.goto(25,25)
                    
                    if len(self.pile) != 0:
                        previous_card = self.pile[0]
                        previous_card = turtle_dictionary.get(previous_card)
                        previous_card.hideturtle()

                    self.grab_cards(player, index)
                    self.pile.insert(0, player.current_card)
                    self.top_card_value = self.find_value(self.pile[0])

                else:
                    player.deck.insert(-1, player.current_card)
                self.check_cards()
                if self.pile != []:
                    self.show_top_card()
                self.over(player)
                if len(player.deck) != 0:
                    player.organize_hand()
                time.sleep(.001)
                break
            else:
                self.skip_turn = False
                break

    def over(self, player):
        if len(player.face_down_cards) == 0 and len(
                player.face_up_cards) == 0 and len(player.deck) == 0:
            print("{} has won".format(player.name))
            self.continue_game = False

    def start(self):
        for i in range(2):
            for player in self.player_list:
                self.start_round(player)
                #if len(player.deck) != 0:
                #    player.organize_hand()
        '''
        while self.continue_game == True:
            for player in self.player_list:
                self.start_round(player)
                if self.continue_game == False:
                    break
                if len(player.deck) != 0:
                    player.organize_hand()    
        '''
        print("game over")


class Player:
    global card_dictionary

    def __init__(self, name):
        self.name = name
        self.face_down_cards = []
        self.face_up_cards = []
        self.deck = []
        self.current_card = ""
        self.card_positions = []
        self.number_of_cards = 0
        self.index = 0

    def organize_hand(self):
        self.deck = self.sortcards(self.deck)
        count = 0  
        displacement = 600/len(self.deck)
        for card in self.deck:
            card = turtle_dictionary.get(card)
            card.goto(-475 + (displacement*count), -150)
            count +=1


    def find_value(self, card):
        if ("Ace" in card):
            return (1)
        elif ("Jack" in card):
            return (11)
        elif ("Queen" in card):
            return (12)
        elif ("King" in card):
            return (13)
        else:
            card = card.split()
            return (int(card[0]))

    def sortcards(self, hand):
        for i in range(4):
            least_value = hand[i]
            og_least_value = deepcopy(least_value)
            count =  deepcopy(i)
            while count < len(hand):
                challenger = hand[count]
                if self.find_value(challenger) < self.find_value(least_value):
                    least_value = challenger
                count += 1

            index = hand.index(least_value)
            hand[index] = og_least_value
            hand[i] = least_value

        return(hand)

    def choosecard(self):
        pass

            
        


class bot:
    bot_names = ["Tyler", "Adrian", "Blaize", "Gabe"]

    def __init__(self):
        i = rand.randint(0, len(bot.bot_names) - 1)
        self.name = bot.bot_names.pop(i)
        self.face_down_cards = []
        self.face_up_cards = []
        self.deck = []
        self.current_card = ""
        self.card_positions = []
        self.number_of_cards = 0
        self.index = 0

    def organize_hand(self):
        count = 0  
        displacement = 600/len(self.deck)
        for card in self.deck:
            card = turtle_dictionary.get(card)
            card.goto(-475 + (displacement*count), 150)
            count +=1        


    def choosecard(self):
        pass


def flip_card_back(card):
    global turtle_dictionary, back
    x = turtle_dictionary.get(card)
    x.shape(back)


def flip_card_up(card):
    global turtle_dictionary
    x = turtle_dictionary.get(card)
    shape = card_dictionary.get(card)
    x.shape(shape)


def update_player_positions():
    if len(Asshole.player_list) == 2:
        y = -150
        x = 75
        for player in Asshole.player_list:
            player.card_positions = [[210, y], [-x + 210, y], [x + 210, y]]
            y = -(y)

    if len(Asshole.player_list) == 4:
        print("test")
        y = -150
        x = 75
        test = 0
        for player in Asshole.player_list:
            player.card_positions = [[0, y], [-x, y], [x, y]]
            y = -(y)
            test += 1
            if test == 2:
                break

        y = 75
        x = 300
        test = 0
        for player in Asshole.player_list:
            if test >= 2:
                player.card_positions = [[x, 0], [x, -y], [x, y]]
                x = -(x)
            test += 1


font_setup = ('Arial', 20, 'normal')


def scene_1():
    global player1, wn, header
    wn = trtl.Screen()
    wn.screensize()
    wn.setup(width=750, height=400)

    header = trtl.Turtle()
    header.penup()
    header.hideturtle()

    header.goto(0, 20)
    header.write(
        "Welcome to asshole.\nTo start the game, click\non the text box and \ntype your name",
        font=font_setup)

    #name = wn.textinput("Name", "What is your name?")
    name = 'Nathan'
    player1 = Player(name)
    wn.clear()


def scene_2():
    #card setup
    #pass
    global wn, back, card_dictionary, Asshole, turtle_dictionary
    Asshole = game()
    Asshole.create_deck()

    card_file = [
        'cards/ac.gif', 'cards/2c.gif', 'cards/3c.gif', 'cards/4c.gif',
        'cards/5c.gif', 'cards/6c.gif', 'cards/7c.gif', 'cards/8c.gif',
        'cards/9c.gif', 'cards/tc.gif', 'cards/jc.gif', 'cards/qc.gif',
        'cards/kc.gif', 'cards/ad.gif', 'cards/2d.gif', 'cards/3d.gif',
        'cards/4d.gif', 'cards/5d.gif', 'cards/6d.gif', 'cards/7d.gif',
        'cards/8d.gif', 'cards/9d.gif', 'cards/td.gif', 'cards/jd.gif',
        'cards/qd.gif', 'cards/kd.gif', 'cards/ah.gif', 'cards/2h.gif',
        'cards/3h.gif', 'cards/4h.gif', 'cards/5h.gif', 'cards/6h.gif',
        'cards/7h.gif', 'cards/8h.gif', 'cards/9h.gif', 'cards/th.gif',
        'cards/jh.gif', 'cards/qh.gif', 'cards/kh.gif', 'cards/as.gif',
        'cards/2s.gif', 'cards/3s.gif', 'cards/4s.gif', 'cards/5s.gif',
        'cards/6s.gif', 'cards/7s.gif', 'cards/8s.gif', 'cards/9s.gif',
        'cards/ts.gif', 'cards/js.gif', 'cards/qs.gif', 'cards/ks.gif'
    ]

    back = 'cards/b.gif'
    wn.addshape(back)
    card_dictionary = {}
    turtle_dictionary = {}
    for i in range(len(Asshole.deck)):
        card = card_file[i]
        wn.addshape(card)

        t = trtl.Turtle()
        t.shape(back)
        t.penup()
        t.showturtle()
        t.goto(100, 25)
        t.penup()

        card_dictionary.update({Asshole.deck[i]: card})
        turtle_dictionary.update({Asshole.deck[i]: t})

    Asshole.shuffle()


def scene_3():
    #game_setup

    global player2, player3, player4, player5, Asshole
    
    player2 = bot()
    player3 = bot()
    player4 = bot()
    player5 = bot()
    Asshole.player_list = [player1, player2]





def scene_4():
    global Asshole
    Asshole.setup()
    Asshole.start()


if __name__ == "__main__":
    global player1, Asshole, wn
    scene_1()
    scene_2()
    scene_3()

    
    scene_4()

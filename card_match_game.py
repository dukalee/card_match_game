#!usr/bin/python3

import random
import time
import os

class Player:

    def __init__(self, name): 

        self.hands = []
        self.name = name


class MatchGame: 

    def __init__(self):

        self.deck = self.deck()
        self.player = Player("Player")
        self.com1 = Player("Computer 1")
        self.com2 = Player("Computer 2")
        self.players = [self.player, self.com1, self.com2]


    def instructions(self): 

        os.system('clear')
        print("""
            Card Matching Game 

    Player will participate in a card-
    matching game with two other A.I. players.

    THe main goal of this game is to get
    rid of ALL your cards as fast as
    possible. 

    Every turn, you will get to choose 
    a card from either of the players 
    to match what you have in your hands.
    if two cards match, then you can throw
    them away. 

                Good Luck

        PRESS ENTER TO CONTINUE
            """)

        ans = input("""
            """)
        if ans == '': 
            self.distribute()


    def deck(self): 

        """
        function to build main deck of cards, with a JOKER 
        """

        suits = ["♦", "♣", "♥", "♠"]            #suits
        nums = []                               #list to hold all the numbers(1~10) + JKQA in.
        faces = ["J", "Q", "K", "A"]            #list of face cards
        deck_of_cards = []                      #final list of trump cards (deck of cards)
        for i in range(2,11):                   #add 1~10 to nums 
            nums.append(str(i)) 
        for face in faces:                      #add faces(JQKA) to nums
            nums.append(face)
        for suit in suits:                      #join the suits
            for num in nums:                    # with the numbers 
                deck_of_cards.append(suit+num)  # and add it to the final deck of cards            
        deck_of_cards.append("JOKER")
        return deck_of_cards


    def distribute(self): 

        """
        function to randomly distribute the cards to 3 players (1player, 2computers)
        """
        print("""
            Distributing Cards...
            """)
        time.sleep(2)
        random.shuffle(self.deck)
        random.shuffle(self.players)
        while len(self.deck) > 0: 
            try:  
                self.players[0].hands.append(self.deck.pop())
                self.players[1].hands.append(self.deck.pop())
                self.players[2].hands.append(self.deck.pop())
            except IndexError: 
                break
        os.system('clear')
        #reduce(throw away matching cards)
        self.player.hands = self.reduce_cards(self.player)      
        self.com1.hands = self.reduce_cards(self.com1)
        self.com2.hands = self.reduce_cards(self.com2)
        self.choose_turn()                      # choose who goes first


    def reduce_cards(self, cards): 

        """
        algorithm to throw away matching cards based on number only. 

        """

        print("""
            reducing {} cards...
            """.format(cards.name))
        time.sleep(1)
        tempdict = {}
        reduced_deck = []
        i = 0 
        while i < len(cards.hands): 
            if cards.hands[i][1:] in tempdict.keys(): 
                print("\t\t   Match: {} {}".format(cards.hands[i], str(tempdict[cards.hands[i][1:]])+str(cards.hands[i][1:])))
                del tempdict[cards.hands[i][1:]]
            else: 
                tempdict[cards.hands[i][1:]] = cards.hands[i][0]
            i+=1
        for key, value in tempdict.items(): 
            reduced_deck.append(value+key)
        time.sleep(1)
        return reduced_deck


    def show_player_deck(self):

        """
        function that shows what player has on his/her hands
        """

        print("\nPlayer Hands: {} cards".format(len(self.player.hands)))
        print(self.player.hands)


    def choose_turn(self):

        """
        function to choose who goes first.
        player with the most cards after first reducing goes first.
        """

        len_list = []
        for i in self.players: 
            len_list.append(len(i.hands))

        turn = self.players[len_list.index(max(len_list))]
        self.game(turn)


    def game(self, player): 

        """
        main game function.
        turn goes in cycle of: player -> com1 -> com2 -> player 
        """

        os.system('clear')                                      #clear console
        print("""
            \t  {} turn!                                        
            """.format(player.name))                          
        time.sleep(1)       
        if player == self.player:                               #if player's turn:
            self.show_player_deck()                             #show hands
            print("\nWho would you like to pick card from?: ") 
            print("1. com1: {}".format(len(self.com1.hands)))
            print("2. com2: {}".format(len(self.com2.hands)))
            target = int(input(">>> "))                         #choose target based on input
            if target == 1:
                target = self.com1
            elif target == 2:
                target = self.com2
            time.sleep(1)
            print("""
            choosing from: {}
                """.format(target.name))

            print("Which card do you wish to pick?: ")          #choose which card to pick based on index
            print(' '.join([str(target.hands.index(i) + 1) for i in target.hands]))
            ans = int(input(">>> "))                        
            card = target.hands[ans-1]                          #choices start with 1, so -1 when actually calling card
            time.sleep(1)
            os.system("clear")                                   

            print("""
                    picked: {}
                """.format(card))                               #show what card has been chosen 
            self.player.hands.append(card)                      #add chosen card to player's hands
            target.hands.remove(card)                           #remove card from the target
            self.check_winner(self.players)                     #first check for winner (if the target had 1 card - we have a winner)
            self.player.hands = self.reduce_cards(self.player)  #if no winner, reduce
            self.check_winner(self.players)                     #second check for winner (if player has 0 cards after reducing)
            self.show_player_deck()                              

            print("""
              Loading Next Player...
                """)
            time.sleep(3)
            enter = input("""
              PRESS ENTER TO CONTINUE
                """)                                            #a method for player to choose when to yield his/her turn
            if enter == '':
                os.system('clear')
                self.game(self.com1)                            #com1's turn

        elif player == self.com1:                               #if com1's turn:
            if (len(self.com2.hands) != 1 and len(self.player.hands) != 1 or
                len(self.com2.hands) == 1 and len(self.player.hands) == 1): #if opposing two players both have 1 cards or more than 1 cards:
                target = random.choice([self.player, self.com2])            #randomly choose who to pick from 
            else: 
                if len(self.com2.hands) != 1: 
                    target = self.com2                                      #if not, avoid player with 1 card left.
                else:
                    target = self.player
            print("""
              choosing from: {}
                """.format(target.name))
            time.sleep(1)
            card = random.choice(target.hands)                 
            self.com1.hands.append(card)                        #take card from target and add it in its hands
            target.hands.remove(card)                           #remove the card from the target
            if target == self.player:                           #if that target was player, show the process and what is left
                print("\t{} took {} from Player!".format(player.name, card))
                self.show_player_deck()
            self.check_winner(self.players)                     #first check for winner
            self.com1.hands = self.reduce_cards(self.com1)      #reduce
            self.check_winner(self.players)                     #second check for winner
            time.sleep(1)
            print(""" 
            {} has {} cards left.
                """.format(self.com1.name, len(self.com1.hands)))
            time.sleep(1)
            print("""
               Loading Next Player...
                """)
            time.sleep(3)
            enter = input("""
              PRESS ENTER TO CONTINUE
                """)
            if enter == '':
                os.system('clear')
                self.game(self.com2)                            #com2's turn

        elif player == self.com2:                               #com2's turn behaves the same way com1 does.
            if (len(self.com2.hands) != 1 and len(self.player.hands) != 1 or
                len(self.com2.hands) == 1 and len(self.player.hands) == 1):
                target = random.choice([self.player, self.com1])
                if len(self.com1.hands) != 1: 
                    target = self.com1
                else:
                    target = self.player
            print("""
              choosing from: {}
                """.format(target.name))
            time.sleep(1)
            card = random.choice(target.hands)
            self.com2.hands.append(card)
            target.hands.remove(card)
            if target == self.player: 
                print("\t{} took {} from Player!".format(player.name, card))
                self.show_player_deck()
            self.check_winner(self.players) 
            self.com2.hands = self.reduce_cards(self.com2)
            time.sleep(1)
            self.check_winner(self.players) 
            print(""" 
            {} has {} cards left.
                """.format(self.com2.name, len(self.com2.hands)))
            time.sleep(1)
            print("""
               Loading Next Player...
                """)
            time.sleep(3)
            enter = input("""
              PRESS ENTER TO CONTINUE
                """)
            if enter == '':
                os.system('clear')
                self.game(self.player)                          #back to player turn


    def check_winner(self, players): 

        """
        function to check for winner. 
        the player with no cards left is the winner.
        """

        for player in players:
            if len(player.hands) == 0: 
                if player == self.player: 
                    print("Congratulations, you win!")
                    self.replay()
                else:
                    print("{} wins!".format(player.name))
                    self.replay()


    def replay(self): 

        """
        prompt for replay
        """

        print("""
            Do you wish to play again? (Y/N)
            """)
        ans = input("""
            >>>""")

        if ans.lower() == 'y': 
            self.distribute() 
        else: 
            print("""
                Thanks for Playing!
                """)
            quit()

game = MatchGame() 
game.instructions()
from Shoe import Shoe
from Hand import Hand
from getFunctions import *
from RulesError import RulesError

class Table(object):
    def __init__(self, dealer, numberOfDecks=6):
        self.shoe = Shoe('CardList', numberOfDecks)
        self.dealer = dealer
        self.Players = []
        self.Bets = []

    def shuffle(self):
        self.shoe.shuffle()

    def take_bets(self):
        removePlayers = []
        for player in self.Players:
            print("""
Name:   {}
Money: ${}""".format(player.name, player.money))
            bet = player.bet_or_leave()
            if bet == None:
                removePlayers.append(player)
            else:
                self.Bets.append(int(bet))
                player.rake_out(int(bet))
        if len(removePlayers) > 0:
            for player in removePlayers:
                self.Players.remove(player)

    def deal(self):
        counter = 0
        while counter < len(self.Players):
            if self.Bets[counter] == 0:
                pass
            else:
                self.shuffle()
                card = self.shoe.draw()
                cardTwo = self.shoe.draw()
                player = self.Players[counter]
                player.add_hand(Hand(card, cardTwo, self.Bets[counter]))
            counter += 1
        card = self.shoe.draw()
        cardTwo = self.shoe.draw()
        self.dealer.add_hand(Hand(card, cardTwo, 0))


    def play_round(self):
        for player in self.Players:
            if len(player.hands) == 0:
                pass
            else:
                for hand in player.hands:
                    while hand.can_hit():
                            command = player.play(self.dealer.show_card(), hand)
                            if command in ['hit','h']:
                                card = self.shoe.draw()
                                hand.hit(card)
                            elif command in ['stand', 's']:
                                hand.stand()
                            elif command in ['double down', 'd']:
                                addBet = hand.bet
                                while addBet > hand.bet/2:
                                    addBet = get_integer("Please enter your additional bet: ")
                                card = self.shoe.draw()
                                hand.double_down(card, int(addBet))
                            elif command in ['split', 'p']:
                                if not hand.can_split():
                                    raise RulesError("Cannot Split this hand")
                                else:
                                    newHand = hand.split()
                                    card = self.shoe.draw()
                                    player.add_hand(Hand(newHand, card, hand.bet))
                            elif command in ['insurance','i']:
                                if not player.is_Insured():
                                    sideBet = hand.bet + 1
                                    while sideBet > hand.bet:
                                        sideBet = get_integer("Please enter your side bet: ")
                                    player.insurance(int(sideBet))
        while self.dealer.hands.hard < 17:
            card = self.shoe.draw()
            self.dealer.hands.hit(card)
            if self.dealer.hands.is_busted():
                print("Dealer Busts!")
            else:
                print("Dealer's Hand is {}".format(self.dealer.hands.value()))

    def payout(self):
        for player in self.Players:
            if len(player.hands) == 0:
                pass
            else:
                for hand in player.hands:
                    if hand.is_blackjack():
                        player.rake_in(hand.bet*2)
                    elif self.dealer.hands.is_busted():
                        bet = hand.bet*2
                        bet = bet/3
                        round(bet)
                        player.rake_in(bet)
                    else:
                        if 21 > hand.value() > self.dealer.hands.value():
                            bet = hand.bet * 2
                            bet = bet / 3
                            round(bet)
                            player.rake_in(bet)
                        else:
                            print("{} lost ${}".format(player.name, hand.bet))
            if player.money <= 0:
                self.Players.remove(player)
                print("{} ran out of money, and left!".format(player.name))
    def introduction(self):
        print("""
██████╗ ██╗      █████╗  ██████╗██╗  ██╗     ██╗ █████╗  ██████╗██╗  ██╗
██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝     ██║██╔══██╗██╔════╝██║ ██╔╝
██████╔╝██║     ███████║██║     █████╔╝      ██║███████║██║     █████╔╝ 
██╔══██╗██║     ██╔══██║██║     ██╔═██╗ ██   ██║██╔══██║██║     ██╔═██╗ 
██████╔╝███████╗██║  ██║╚██████╗██║  ██╗╚█████╔╝██║  ██║╚██████╗██║  ██╗
╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
============================================================================""")
        instructions = get_yes_no("Do you want to see instructions? ")
        if instructions == 'yes':
            print("""
--------Instructions-------
In this game you play 
BlackJack, the Card Game.
You keep playing until you 
either run out of money, or
choose to leave. Have Fun!
""")

    def outro(self):
        if __name__ == '__main__':
            print("""
Created By: Ian Kollipara
    
Thank you for playing...
██████╗ ██╗      █████╗  ██████╗██╗  ██╗     ██╗ █████╗  ██████╗██╗  ██╗
██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝     ██║██╔══██╗██╔════╝██║ ██╔╝
██████╔╝██║     ███████║██║     █████╔╝      ██║███████║██║     █████╔╝ 
██╔══██╗██║     ██╔══██║██║     ██╔═██╗ ██   ██║██╔══██║██║     ██╔═██╗ 
██████╔╝███████╗██║  ██║╚██████╗██║  ██╗╚█████╔╝██║  ██║╚██████╗██║  ██╗
╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
""")
#encoding: utf8
import card
import csv
from player import Player


class StudentPlayer(Player):
    def __init__(self, f, name="mantunes", money=0):
        with open(f, 'rb') as f:
            reader = csv.reader(f)
            self.matrix = list(reader)
        self.t = 12
        self.betmin = 0.02
        self.betmax = 0.05
        self.previous_bet = 0
        self.min_bet = 10
        self.can_double = True
        super(StudentPlayer, self).__init__(name, money)

    def play(self, dealer, players):
        if not self.can_double:
            action = 's'
        else:
            player = [x for x in players if x.player.name == self.name][0]
            dealer_value = card.value(dealer.hand)
            bot_value = card.value(player.hand)
            didx = 21 if dealer_value >= 21 else dealer_value - 1
            bidx = 21 if bot_value >= 21 else bot_value - 1
            action = self.matrix[bidx][didx]
            if action == 'd' and self.can_double:
                self.can_double = False
            if dealer_value > 21 or bot_value > 21:
                action = 's'
        return action

    def bet(self, dealer, players):
        if self.can_double:
            player = [x for x in players if x.player.name == self.name][0]
            dealer_value = card.value(dealer.hand)
            bot_value = card.value(player.hand)
            r = bot_value - dealer_value
            if r >= self.t:
                bet = int(self.pocket * self.betmax)
            else:
                bet = int(self.pocket * self.betmin)
            if bet <= 0:
                bet = self.min_bet
            self.previous_bet = bet
        else:
            bet = self.previous_bet
        return bet

    def payback(self, prize):
        self.can_double = True
        super(StudentPlayer, self).payback(prize)

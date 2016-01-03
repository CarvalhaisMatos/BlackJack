#encoding: utf8
__author__ = 'Diogo Gomes'
__email__ = 'dgomes@ua.pt'
__license__ = "GPL"
__version__ = "0.1"
import json
from player import Player
from json_utils import object_to_dict
from json_utils import dict_to_object
import zmq

class ProxyPlayer(Player):
    def __init__(self, socket, name="Player", money=0):
        self.name = name
        self.pocket = money #dont mess with pocket!
        self.table = 0
        self.socket = socket

    def show(self, players):
        print "show()"
        self.socket.send(json.dumps({'cmd':"SHOW", 'players':players}, default=object_to_dict))
        message = self.socket.recv()

    def want_to_play(self, rules):     
        print "want_to_play()"
        self.socket.send(json.dumps({'cmd':"WANT_TO_PLAY", 'rules':rules}, default=object_to_dict))
        message = self.socket.recv()
        return json.loads(message)

    def payback(self, prize):
        print "payback()"
        self.socket.send(json.dumps({'cmd':"PAYBACK", 'prize':prize}))
        message = self.socket.recv()

    def play(self, dealer, players):
        print "play()"
        self.debug_state(dealer, players)
        self.socket.send(json.dumps({'cmd':"PLAY", 'dealer':dealer, 'players':players}, default=object_to_dict))
        message = self.socket.recv()
        return json.loads(message)

    def bet(self, dealer, players):
        print "bet()"
        self.debug_state(dealer, players)
        self.socket.send(json.dumps({'cmd':"BET", 'dealer':dealer, 'players':players}, default=object_to_dict))
        message = self.socket.recv()
        return json.loads(message)

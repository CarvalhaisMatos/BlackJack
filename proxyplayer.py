#encoding: utf8
__author__ = 'Diogo Gomes'
__email__ = 'dgomes@ua.pt'
__license__ = "GPL"
__version__ = "0.1"
import json
from player import Player
import requests

def object_to_dict(obj):
    d = { '__class__':obj.__class__.__name__, 
          '__module__':obj.__module__,
        }
    d.update(obj.__dict__)
    if d['__class__'] == 'ProxyPlayer':
        d.pop('identity')
    return d

class ProxyPlayer(Player):
    def _issue_cmd(self, cmd):
        data = json.dumps(cmd, default=object_to_dict)
        headers = {'content-type': 'application/json'}
        r = requests.post("http://localhost:{}/post".format(self.identity), data = data, headers = headers)
        print "[{}] -> {}".format(self.identity, r.text)
        message = json.loads(r.text)
        return message

    def __init__(self, identity, name="Player", money=0):
        super(ProxyPlayer, self).__init__(name=name, money=money)
        self.identity = identity

    def new(self):
        self._issue_cmd({'cmd':"NEW", 'name':self.name, 'money':self.pocket})

    def show(self, players):
        print "show()"
        self._issue_cmd({'cmd':"SHOW", 'players':players})

    def want_to_play(self, rules):     
        print "want_to_play()"
        message = self._issue_cmd({'cmd':"WANT_TO_PLAY", 'rules':rules})
        print ">{}<".format(message)
        return message

    def payback(self, prize):
        print "payback()"
        message = self._issue_cmd({'cmd':"PAYBACK", 'prize':prize})
        self.pocket = message

    def play(self, dealer, players):
        print "play()"
        self.debug_state(dealer, players)
        message = self._issue_cmd({'cmd':"PLAY", 'dealer':dealer, 'players':players})
        return message

    def bet(self, dealer, players):
        print "bet()"
        self.debug_state(dealer, players)
        message = self._issue_cmd({'cmd':"BET", 'dealer':dealer, 'players':players})
        return message
    def bye(self):
        print "bye()"
        self._issue_cmd({'cmd':"BYE"})

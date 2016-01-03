from game import Game
from player import Player
from proxyplayer import ProxyPlayer
import sys 

if __name__ == '__main__':
    
    players = []

    for nmec in sys.argv[1:]:
        players += [ProxyPlayer(int(nmec), nmec, 100)]

    for p in players:
        p.new()

    if len(players):
        for i in range(2):
            print players
            g = Game(players, min_bet=1, max_bet=5) 
            #g = Game(players, debug=True)
            g.run()

    print "OVERALL: ", players

    for p in players:
        p.bye()

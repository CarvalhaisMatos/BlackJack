from game import Game
from player import Player
from randomplayer import RandomPlayer

if __name__ == '__main__':
    
    players = [Player(name="Human", money=3000)]
    
    for i in range(1000):
        print players
        g = Game(players, verbose=False)
        #g = Game(players, debug=True)
        g.run()

    print "OVERALL: ", players

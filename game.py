from tictactoe import TicTacToe
from agents import *
from util import *

AGENT = ExpectimaxAgent

def run(gameplay, agents_1):
    if(gameplay.gstate.T == 1):

        print("It is CPU's Turn: ")
        action = agents_1.getMove(gameplay.gstate, 0.95, 0.0, 4)
        gameplay.gstate = gameplay.transition(act)
        return

    print("It is Your Turn: ")
    cmd = getInput(gameplay)
    handleInput(gameplay, cmd)

if(__name__ == "__main__"):
    n = 0
    while(n < 3):
        try:
            n = int(input("Enter The Size of the board: "))
        except NameError1:
            print("ERROR: Please enter a numeric value")
            continue
        except SyntaxError1:
            print("ERROR: No input defined")
            continue
        if(n < 3):
            print("ERROR: You can't play with this this board size")
    k_1 = 0
    while(k_1 < 3 or k_1 > N):
        try:
            k_1 = int(input(" Pleae enter number of adjacent squares that you need to win gameplay : "))
        except NameError1:
            print("ERROR: It is Not a number")
            continue
        except SyntaxError1:
            print("ERROR: No input defined")
            continue
        if(k_1 > n):
            print("ERROR: Input can't be larger than the size of board")
        elif(k_1 < 3):
            print("ERROR: Input should be at least 3")
    gameplay = TicTacToe(n, k_1)
    print(gameplay)
    help(gameplay)
    agents_1 = AGENT(k_1)
    win, winners = False, None
    while(not(win) and sum(gameplay.gstate.acts) > 0):
        run(gameplay, agents_1)
        win, winners = agents_1.check(gameplay.gstate)
        print("CURRENT gameplay STATE\n%s"%gameplay)
    if(not win): #Tie
        print("Stale_mate.")
    elif(winners == 0): #Player win
        print("Victory is Yours!")
    else:              #CPU win
        print("BETTER LUCK NEXT TIME.")

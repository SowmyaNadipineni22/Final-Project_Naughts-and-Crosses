import numpy as np
from enum import Enum
import copy
from collections import namedtuple

MODE = "three"

N = 5                                     # N X N grid
P = 0.0                                   # P(Random)
W = 1000                                  # Win Score Reward
L = 0.95                                  # Decay
D = 3                                     # Max Depth of Search
T = 0                                     # 0 is Player, 1 is CPU
actions = [1] * (N * N)                   # Available Actions
players = {0: 'X', 1: 'O'}                # X is Player, O is CPU
board   = [[-1] * N for _ in range(N)]    # Board representation
qVals   = {}                              # Cache qVals
vals    = {}                              # Vals of states

def validCoord(coord):
    row, col = coord
    return(0 <= row < N and 0 <= col < N)

'''
Gets user input for player's turn
'''
def getAction(availableActions = actions):
    print("'X' can take these remaining boxes: ")
    print([i for i, action in enumerate(availableActions) if action])
    action = int(input("Enter the ID of a remaining box: "))
    while(availableActions[action] == 0):
        print("ERROR: Invalid action. Try again: ")
        action = int(input("Enter the ID of a remaining box: "))
    return action

'''
Gets coords from user inputted action
'''
def dcdAction(action):
    return Coord(int(action/N), action%N)

'''
Reward function for any action
'''
def reward(action):
    return 0

'''
Output messages
'''
def output(T, action, randAction=None):
    message = "Player " + str(players[T]) + " Selected Box #" + str(action)
    if(randAction):
        print(message + ", However a random box (Box #" + str(randAction) + ") was instead selected. The Probability of this happening during any move is: " + str(P))
    else:
        print(message)

'''
GameState Representation
'''
GameState = namedtuple('GameState', 'T board actions')

'''
Coord Representation
'''
Coord = namedtuple('Coord', 'Row Col')

'''
Game Functions
'''
class TicTacToe():
    def __init__(self):
        self.gameState = GameState(T, board, actions)
        self.states = [self.gameState]
        N = int(input("Enter Size of Tic-Tac-Toe Grid: "))
        while(N < 3):
            print("ERROR: Can't play Tic Tac Toe with board size less than 3")
            N = input("Enter Size of Tic-Tac-Toe Grid: ")

    def transition(self, action):
        T, board, actions = self.gameState
        newT, newBoard, newActions = (T+1)%2, copy.deepcopy(board), list(actions)
        randAction = None
        if(np.random.random() < P): #Random action selected
            randAction = np.random.choice([i for i in range(len(actions)) if actions[i]])
        output(T, action, randAction) #Display action with player
        if(randAction):
            action = randAction
        row, col = dcdAction(action)
        newBoard[row][col] = T
        newActions[action] = 0
        return GameState(newT, newBoard, newActions)

    def undo(self):
        if(len(states) == 1):
            raise("ERROR: Undo attempted but you have not taken any actions yet")
        self.gameState = self.states.pop()

    def run(self, agent):
        if(self.gameState.T == 1):
            print("CPU Turn: ")
            #agent.printVals(self.gameState)
            action = agent.getMove(self.gameState)
        else:
            print("Your Turn: ")
            action = getAction(self.gameState.actions)
        self.gameState = self.transition(action)

    def __str__(self): #Overwrites toString()
        s = ''
        for row in range(N):
            for col in range(N):
                try:
                    s += ('[' + str(players[self.gameState.board[row][col]]) + ']')
                except:
                    s += ('[' + str(row*N + col) + ']')
            s += ('\n')
        return s

'''
Abstract Computer Agent
'''
class Agent():
    def __init__(self):
        pass

    def checkBox(self, board): #Checks one sub-grid
        N = len(board)
        '''
        Horizontal Check
        '''
        for row in range(N):
            if(board[row][0] >= 0 and all(board[row][col] == board[row][col+1] for col in range(N-1))):
                return True, board[row][0]
        '''
        Vertical Check
        '''
        for col in range(N): 
            if board[0][col] >= 0 and all([board[row-1][col] == board[row][col] for row in range(1, N)]):
                return True, board[0][col]
        '''
        Diagonal 1 Check
        '''
        if board[0][0] >= 0 and all([board[row-1][row-1] == board[row][row] for row in range(1, N)]):
            return True, board[0][0]
        '''
        Diagonal 2 Check
        '''
        if board[0][-1] >= 0 and all([board[i-1][N-i] == board[i][N-i-1] for i in range(1, N)]):
            return True, board[0][-1]
        '''
        Default
        '''
        return False, None

    def check(self, gameState): #Cheks all 3X3 sub-grids of a gameState
        board = np.matrix(gameState.board)
        for row in range(N-3+1):
            for col in range(N-3+1):
                won, winner = self.checkBox(board[row:row+3,col:col+3].tolist())
                if(won):
                    return True, winner

        '''
        Default
        '''
        return False, None

    def qScore(self, gameState, action):
        pass

    def score(self, gameState):
        pass

    '''
    Agent gets its optimal move
    '''
    def getMove(self, gameState):
        minQ, optimalAction = float('inf'), None
        ties = []
        actions = gameState.actions
        for i, action in enumerate(actions):
            if(action):
                q = self.qScore(gameState, i)
                if(q < minQ):
                    minQ, optimalAction = q, i
                    ties = []
                elif(q == minQ):
                    ties.append(i)
        if(ties):
            return np.random.choice(ties)
        return optimalAction

    '''
    Returns next game state given a current state and an action
    '''
    def update(self, gameState, action):
        newT = (gameState.T+1)%2
        newBoard = copy.deepcopy(gameState.board)
        row, col = dcdAction(action)
        newBoard[row][col] = gameState.T
        newActions = list(gameState.actions)
        newActions[action] = 0
        newState = GameState(newT, newBoard, newActions)
        return newState

    '''
    Probability of all resulting states from an action
    '''
    def transition(self, gameState, action):
        newState = self.update(gameState, action)
        yield(newState, float(1-P))
        if(P > 0): #P is the chance of a random move being forced
            for randAction, possible in enumerate(actions):
                if(possible):
                    newState = self.update(gameState, randAction)
                    yield(newState, (float(P)/sum(actions))) #Random game state probabilities 

    '''
    Prints values of next possible states for the CPU
    '''
    def printVals(self, gameState):
        V = {}
        for i, action in enumerate(gameState.actions):
            if(action):
                for newState, _ in self.transition(gameState, i):
                    V[str(newState)] = L * self.score(newState)
        print(V)
        return V

    '''
    Prints qValues of (action, state) pairs
    '''
    def printQVals(self, gameState):
        pass

'''
Expectimax Computer Agent
'''
class ExpectimaxAgent(Agent):
    def __init__(self):
        Agent.__init__(self)

    def qScore(self, gameState, action):
        qState = str(gameState) + str(action)
        if qState in qVals:
            return qVals[qState]
        s = reward(action)
        for state, prob in self.transition(gameState, action):
            s += L * prob * self.score(state)
        qVals[qState] = s
        return s

    def score(self, gameState, d=0):
        '''
        If the score for a gameState has already been computed, fetch
        '''
        if(str(gameState) in vals):
            return vals[str(gameState)]

        '''
        Check if the game has been won, if so return appropriate value
        '''
        won, winner = self.check(gameState)
        if(won):
            vals[str(gameState)] = W if(winner==0) else -W #Win Score
            return vals[str(gameState)]

        '''
        Check if the depth search limit has been reached, or if there
        are no valid actions left. If so, return 0
        '''
        actions = gameState.actions
        if(sum(actions)==0 or d==D):
            vals[str(gameState)] = 0
            return 0

        '''
        Last resort: Compute the score of the Game State
        '''
        bestScore, optim = W, min
        if(gameState.T == 0):
            bestScore, optim = -bestScore, max
        accum = 0
        for i, action in enumerate(actions):
            if action:
                newState = self.update(gameState, i)
                newScore = reward(action) + L*self.score(newState, d+1)
                accum += newScore
                bestScore = optim(bestScore, newScore)
        totalScore = ((1.0-P)*bestScore + (P)*(accum/sum(actions)))
        vals[str(gameState)] = L*totalScore
        return totalScore

class MinimaxAgent(Agent):
    def __init__(self):
        pass


if(__name__ == "__main__"):
    game = TicTacToe()
    print(game)
    agent = ExpectimaxAgent()
    won, winner = False, None
    while(not(won) and sum(game.gameState.actions) > 0):
        game.run(agent)
        won, winner = agent.check(game.gameState)
        print(game)
    if(not won): #Tie
        print("Stalemate.")
    elif(winner == 0): #Player Won
        print("Victory is Yours!!!")
    else:              #CPU Won
        print("FOOLISH MORTAL. TRY HARDER NEXT TIME.")

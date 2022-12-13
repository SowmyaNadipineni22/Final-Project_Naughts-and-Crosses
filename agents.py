import os
import collections
import numpy as np
import random
import numpy as np
import pandas as pd
from util import *

values = {}
qvalues = {}
# overview  of system agent

class Agent():
    def __init__(self, A):
        self.A = A
    def check(self, gstate): #Cheking possible AxA for all sub-grids of gameStates
        Boards = np.matrix(gstate.Boards)
        l = len(Boards)
        A = self.A
        for i in range(l-A+1):
            for j in range(l-A+1):
                won, winner = self.checkBox(Boards[i:i+A,j:j+A].tolist())
                if(won):
                    return True, winner
        return False, None
    def checkBox(self, Boards): #Exploring 1 sub-grid
        l = len(Boards)
        for i in range(l): # Horizontal examine
            if(Boards[i][0] >= 0 and all(Boards[i][j] == Boards[i][j+1] for j in range(l-1))):
                return True, Boards[i][0]
        for j in range(l): # vertical examine
            if(Boards[0][j] >= 0 and all([Boards[i-1][j] == Boards[i][j] for i in range(1, l)])):
                return True, Boards[0][j]
        if Boards[0][0] >= 0 and all([Boards[i-1][i-1] == Boards[i][i] for i in range(1, l)]):#1st diagonal examine
            return True, Boards[0][0]
        if Boards[0][-1] >= 0 and all([Boards[i-1][l-i] == Boards[i][l-i-1] for i in range(1, l)]): #2nd diagonal examine
            return True, Boards[0][-1]
        return False, None
    def score(self, gstate, Le, p, d, w, de):
        if(str(gstate) in values):
            return values[str(gstate)]
        won, winner = self.check(gstate)
        if(won):
            values[str(gstate)] = w if(winner==0) else -w #Win Score to be shown
            return values[str(gstate)]
        actions = gstate.actions
        if(sum(actions)==0 or de==D):
            values[str(gstate)] = 0
            return 0
        return(self.computeScore_1(gstate, Le, p, d, w, de))
    def qScore(self, gstate, action, Le, p, d, w):
        qstate = str(gstate) + str(action)
        if qstate in qvalues:
            return qvalues[qstate]
        sc = reward(action)
        for s, p in self.transition(gstate, action, p):
            sc += Le * p * self.score(s, Le, p, d, w, 0)
        qvalues[qstate] = sc
        return sc
    def update(self, gstate, action):
        newT = (gstate.T+1)%2
        newBoards = copy.deepcopy(gstate.Boards)
        l = len(newBoards)
        r,c = dcdAction(action, l)
        newBoards[r][c] = gameState.T
        newActions = list(gameState.actions)
        newActions[action] = 0
        newState = GameState(newT, newBoards, newActions)
        return newState
    def getMove(self, gstate, Le=1, p=0, d=5, w=1000):
        minQ, optimalAction = float('inf'), None
        ties = []
        actions = gstate.actions
        for i, action in enumerate(actions):
            if(action):
                q = self.qScore(gstate, i, Le, p, d, w)
                if(q < minQ):
                    minQ, optimalAction = q, i
                    ties = []
                elif(q == minQ):
                    ties.append(i)
        if(ties):
            return np.random.choice(ties)
        return optimalAction
    def transition(self, gstate, action, P):
        newState = self.update(gameState, action)
        yield(newState, float(1-P))
        if(P > 0): #P is the chance of a random move being forced
            for randAction, possible in enumerate(actions):
                if(possible):
                    newState = self.update(gameState, randAction)
                    yield(newState, (float(P)/sum(actions))) #Random game state probabilities_
    def printVals(self, gstate):
        V = {}
        for i, action in enumerate(gstate.actions):
            if(action):
                for newState, _ in self.transition(gstate, i):
                    V[str(newState)] = L * self.score(newState)
        print(V)
        return V

class ExpectimaxAgent(Agent):
    def __init__(self, K):
        Agent.__init__(self, K)

    def computeScore_1(self, gstate, Le, p, d, w, de=0):
        bestScore, optim = w, min
        if(gameState.T == 0):
            bestScore, optim = -bestScore, max
        accum = 0
        actions = gameState.actions
        for i, action in enumerate(actions):
            if action:
                newState = self.update(gameState, i)
                newScore = reward(action) + Le*self.score(newState, Le, p, d, w, de+1)
                accum += newScore
                bestScore = optim(bestScore, newScore)
        totalScore = ((1.0-p)*bestScore + (p)*(accum/sum(actions)))
        vals[str(gameState)] = totalScore
        return totalScore

class MinimaxAgent(Agent):
    def __init__(self, A):
        Agent.__init__(self, A)

    def computeScore_1(self, gstate, Le, p, d, w, de=0):

        bestScore, optim = w, min
        if(gstate.T == 0):
            bestScore, optim = -bestScore, max
        actions = gstate.actions
        for i, action in enumerate(actions):
            if action:
                newState = self.update(gstate, i)
                newScore = reward(action) + L*self.score(newState, Le, p, d, w, de+1)
                bestScore = optim(bestScore, newScore)
        values[str(gstate)] = bestScore
        return bestScore

class MinimaxAlphaBeta(Agent):
    def __init__(self, A):
        Agent.__init__(self, A)

    def computeScore_1(self, gstate, Le, p, d, w, de, alpha=float('-inf'), beta=float('inf')):
        actions = gstate.actions
        if(de==d or sum(actions)==0): return 0
        if(gstate.T == 0): #Maximize the Agent
            bestScore = -w
            for i, action in enumerate(actions):
                if(action):
                    newState = self.update(gstate, i)
                    newScore = reward(action) + Le+self.computeScore_1(newState, Le, p, d, w, de+1, alpha, beta)
                    bestScore = max(bestScore, newScore)
                    alpha = max(alpha, newScore)
                    if(alpha > beta): break
        else: #Minimize the Agent
            bestScore = w
            for i, action in enumerate(actions):
                if(action):
                    newState = self.update(gstate, i)
                    newScore = reward(action) + Le*self.computeScore_1(nstate, Le, p, d, w, de+1, alpha, beta)
                    bestScore = min(bestScore, newScore)
                    beta = min(newScore, beta)
                    if(alpha > beta): break
        values[str(gstate)] = bestScore
        return bestScore



class Learner(A_B_C):

    def __init__(self, al, ga, eps, ep_decay=0.):
        # Agent parameter we are entering
        self.al = al
        self.ga = ga
        self.eps = eps
        self.ep_decay = ep_decay
        # Possible actions for x,y coordinate pairs
        self.actions = []
        for i in range(3):
            for j in range(3):
                self.actions.append((i,j))
        # Initializing 0 to Q for state-action.
        # Accessing action a, state s values via Q[a][s]
        self.Q = {}
        for action in self.actions:
            self.Q[action] = collections.defaultdict(int)
        # Keeping a list of reward 
        self.rewards = []

    def get_action(self, s):

        # Only allowed actions (empty space)
        possibleactions1 = [a for a in self.actions if s[a[0]*3 + a[1]] == '-']
        if random.random() < self.eps:
            # Random Choosing action.
            action_1 = possibleactions1[random.randint(0,len(possibleactions1)-1)]
        else:
            # Greedy choosing action.
            values_1 = np.array([self.Q[a][s] for a in possibleactions1])
            # Finding the maximum loc
            ix_max = np.where(values_1 == np.max(values_1))[0]
            if len(ix_max) > 1:
                # Sample when multiple actions are maximum
                ab_select = np.random.choice(ix_max, 1)[0]
            else:
                # If unique max action, select that one
                ab_select = ix_max[0]
            action_1 = possibleactions1[ab_select]

        # update epsilon; geometric decay
        self.eps *= (1.-self.ep_decay)

        return action_1

    def save(self, path):
        """ To save the state of agent we are Pickling the object instance . """
        if os.path.isfile(path):
            os.remove(path)
        f = open(path, 'wb')
        pickle.dump(self, f)
        f.close()

    @abstractmethod
    def update(self, s, s_, a, a_, r):
        pass

class Qlearner(agent):
    """
    Implementing Q-learner agent.
    """
    def _init_(self, al, ga, eps, ep_decay=0.):
        super()._init_(al, ga, eps, ep_decay)

    def update(self, s, s_, a, a_, r):

        # Updating the Q(s,a)
        if s_ is not None:
            # To hold the list of Q values of all a_,s_ pairs, we will later access the maximum
            possibleactions1 = [act for act in self.acts if s_[act[0]*3 + act[1]] == '-']
            Q_options = [self.Q[action][s_] for act in possibleactions1]
            # updatting Q
            self.Q[a][s] += self.al*(r + self.gamma*max(Q_options) - self.Q[a][s])
        else:
            # We update the terminal state
            self.Q[a][s] += self.al*(r - self.Q[a][s])

        # adding r to the list named as reward
        self.rewards.append(r)




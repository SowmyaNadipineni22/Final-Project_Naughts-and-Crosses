import pickle
import numpy as np

BRD_RWS = 3
BRD_CLS = 3


class State:
    def __init__(self, p1, p2):
        self.board = np.zeros((BRD_RWS, BRD_CLS))
        #For Player 1
        self.p1 = p1
        #For Player 2
        self.p2 = p2
        self.isEnd = False
        #Giving Conditions
        self.boardHash = None
        # Player 1's turn
        self.playerSymbol = 1

    # getting hash of board state which is unique
    def getHash(self):
        self.boardHash = str(self.board.reshape(BRD_CLS * BRD_RWS))
        return self.boardHash

    def winner(self):
        # Defining rows
        for i in range(BRD_RWS):
            if sum(self.board[i, :]) == 3:
                self.isEnd = True
                return 1
            if sum(self.board[i, :]) == -3:
                self.isEnd = True
                return -1
        # Defining Columns
        for i in range(BRD_CLS):
            if sum(self.board[:, i]) == 3:
                self.isEnd = True
                return 1
            if sum(self.board[:, i]) == -3:
                self.isEnd = True
                return -1
        # Defining Diagonal
        diag_sum1 = sum([self.board[i, i] for i in range(BRD_CLS)])
        diag_sum2 = sum([self.board[i, BRD_CLS - i - 1] for i in range(BRD_CLS)])
        diag_sum = max(abs(diag_sum1), abs(diag_sum2))
        if diag_sum == 3:
            self.isEnd = True
            if diag_sum1 == 3 or diag_sum2 == 3:
                return 1
            else:
                return -1

        # If there are no positions available
        if len(self.availablePositions()) == 0:
            self.isEnd = True
            return 0
        # not the end
        self.isEnd = False
        return None

    def availablePositions(self):
        positions = []
        for i in range(BRD_RWS):
            for j in range(BRD_CLS):
                if self.board[i, j] == 0:
                    positions.append((i, j))  # need to be tuple
        return positions

    def updateState(self, position):
        self.board[position] = self.playerSymbol
        # switching to a different player
        self.playerSymbol = -1 if self.playerSymbol == 1 else 1

    # Ending of the game
    def giveReward(self):
        result = self.winner()
        # Reward for backpropagation
        if result == 1:
            self.p1.feedReward(1)
            self.p2.feedReward(0)
        elif result == -1:
            self.p1.feedReward(0)
            self.p2.feedReward(1)
        else:
            self.p1.feedReward(0.1)
            self.p2.feedReward(0.5)

    # Reseting the board
    def reset(self):
        self.board = np.zeros((BRD_RWS, BRD_CLS))
        self.boardHash = None
        self.isEnd = False
        self.playerSymbol = 1

    def play(self, rounds=100):
        for i in range(rounds):
            if i % 1000 == 0:
                print("Rounds {}".format(i))
            while not self.isEnd:
                # For 1 Player
                positions = self.availablePositions()
                p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol)
                # taking action and upating the state of the board
                self.updateState(p1_action)
                boardhash2 = self.getHash()
                self.p1.addState(boardhash2)
                # To check the board status whether if it in end

                wins1 = self.winner()
                if wins1 is not None:
                    # self.showBoard()
                    # p1 ends either winning or draw
                    self.giveReward()
                    self.p1.reset()
                    self.p2.reset()
                    self.reset()
                    break

                else:
                    # For 2 Player
                    positions = self.availablePositions()
                    p2_action = self.p2.chooseAction(positions, self.board, self.playerSymbol)
                    self.updateState(p2_action)
                    boardhash2 = self.getHash()
                    self.p2.addState(boardhash2)

                    wins1 = self.winner()
                    if wins1 is not None:
                        # self.showBoard()
                        # p2 either wins or a draw
                        self.giveReward()
                        self.p1.reset()
                        self.p2.reset()
                        self.reset()
                        break

    # playing with a human
    def play2(self):
        while not self.isEnd:
            # For 1 Player 
            positions = self.availablePositions()
            p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol)
            # taking action and updating the board state
            self.updateState(p1_action)
            self.showBoard()
            # status if it is end
            wins1 = self.winner()
            if wins1 is not None:
                if wins1 == 1:
                    print(self.p1.name, "is a winner!")
                else:
                    print("It's a tie!")
                self.reset()
                break

            else:
                # For 2 Player
                positions = self.availablePositions()
                p2_action = self.p2.chooseAction(positions)

                self.updateState(p2_action)
                self.showBoard()
                wins1 = self.winner()
                if wins1 is not None:
                    if wins1 == -1:
                        print(self.p2.name, "is a winner!")
                    else:
                        print("It's a tie!")
                    self.reset()
                    break

    def showBoard(self):
        # p1: x  p2: o
        for i in range(0, BRD_RWS):
            print('-------------')
            out = '| '
            for j in range(0, BRD_CLS):
                if self.board[i, j] == 1:
                    token_1 = 'x'
                if self.board[i, j] == -1:
                    token_1 = 'o'
                if self.board[i, j] == 0:
                    token_1 = ' '
                out += token_1 + ' | '
            print(out)
        print('-------------')


class Player:
    def __init__(self, name, exp_rate=0.3):
        self.name = name
        self.states = []  # recording all possible taken positions
        self.lr = 0.2
        self.exp_rate = exp_rate
        self.decay_gamma = 0.9
        # state -> value
        self.states_value = {} 

    def getHash(self, board):
        boardHash = str(board.reshape(BRD_CLS * BRD_RWS))
        return boardHash

    def chooseAction(self, positions, current_board, symbol):
        if np.random.uniform(0, 1) <= self.exp_rate:
            # taking actions randomly
            idx = np.random.choice(len(positions))
            action = positions[idx]
        else:
            value_max = -999
            for p in positions:
                next_board = current_board.copy()
                next_board[p] = symbol
                next_boardHash = self.getHash(next_board)
                value = 0 if self.states_value.get(next_boardHash) is None else self.states_value.get(next_boardHash)
                # print("value", value)
                if value >= value_max:
                    value_max = value
                    action = p
        # print("{} takes action {}".format(self.name, action))
        return action

    # appending a hash rate
    def addState(self, state):
        self.states.append(state)

    # Backpropagating and updating the states value at the end of game
    def feedReward(self, reward):
        for st in reversed(self.states):
            if self.states_value.get(st) is None:
                self.states_value[st] = 0
            self.states_value[st] += self.lr * (self.decay_gamma * reward - self.states_value[st])
            reward = self.states_value[st]

    def reset(self):
        self.states = []

    def savePolicy(self):
        fw = open('policy_' + str(self.name), 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()

    def loadPolicy(self, file):
        fr = open(file, 'rb')
        self.states_value = pickle.load(fr)
        fr.close()


class HumanPlayer:
    def __init__(self, name):
        self.name = name

    def chooseAction(self, positions):
        while True:
            row = int(input("Input your choice of row:"))
            col = int(input("Input your choice of column:"))
            action = (row, col)
            if action in positions:
                return action

    # appending a hash rate
    def addState(self, state):
        pass

    # Backpropagation and updating the states value at the end of game
    def feedReward(self, reward):
        pass

    def reset(self):
        pass


if __name__ == "__main__":
    # training the players
    p1 = Player("p1")
    p2 = Player("p2")

    st = State(p1, p2)
    print("training......")
    st.play(5000)

    # playing with human
    p1 = Player("computer", exp_rate=0)
    p1.loadPolicy("policy_p1")

    p2 = HumanPlayer("human")

    st = State(p1, p2)
    st.play2()

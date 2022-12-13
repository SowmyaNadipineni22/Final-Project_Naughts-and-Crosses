from collections import namedtuple
players = {0: 'X', 1: 'O'} # X is Player, O is CPU
def help(g):
    print("Supported Commands: ")
    for cmd in cmds:
        print(cmd, cmds[cmd])
def undo(g):
    g.undo() # place in
def reset(g):
    g.reset() #place in 
cmds = {'h': help, 'u': undo, 'r': reset} # commands
def displayActions(aa):
    print("'X' can take  remaining boxes: ")
    print([j for j, action in enumerate(aa) if action])
def validCoord(csd, M):
    r, c = csd
    return(0 <= r < M and 0 <= c < M)
def dcdAction(act, M):
    return Coord(int(act/M), act%M)
def reward(act):
    return 0
def output(T, act, ract=None):
    mess = "Player " + str(players[T]) + " Selected Box #" + str(act)
    if(ract):
        print(mess + ", However a random box (Box #" + str(ract) + ")  instead selected. Probability  happening during any move is: " + str(T))
    else:
        print(mess)
def getInput(g):
    availableActions = g.gameState.actions
    displayActions(availableActions) #Output to terminal
    h, r, u = cmds['h'], cmds['r'], cmds['u']
    userInput = int(input("Enter a command or the ID of a remaining box: "))
    while(not validateInput(g, userInput)):
        print("ERROR: Invalid input. Try again: ")
        action = int(input("Enter the ID of a remaining box: "))
    return userInput
def validateInput(game, input):
    try:
        input = int(input) #Check if valid action
        N = game.N
        return(0 <= input < N*N and game.gameState.actions[input])
    except:
        return(input in cmds) #Check if valid command
def handleInput(game, validatedInput):
    try:
        game.gameState = game.transition(int(validatedInput))
    except:
        cmds[validatedInput](game)
def getGameState(N):
    T       = 0
    board   = [[-1] * N for _ in range(N)]
    actions = [1] * (N*N)
    return GameState(T, board, actions)
GameState = namedtuple('GameState', 'T board actions')
Coord = namedtuple('Coord', 'Row Col')

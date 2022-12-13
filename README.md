# Final-Project_NOUGHTS-and-CROSSES

# Noughts and crosses
The submitted file is for the Term Project for the course Introduction to Artificial Intelligence (CSCI-6660-02),Fall 2022. 
The group members for this project are Sowmya Nadipineni and Renuka Kakani

A Tic-Tac-Toe game is developed using different artificial intelligence agents.
We have implemented the game using the following four agents with their variations: Expectimax, Minimax, Alpha- Beta, Q learning and Approximate Q learning algorithms.

# Noughts and Crosses Game
A game having two players alternately opting X’s and O’s between two horizontal and vertical lines trying to get quickest pattern of three consecutive X’s or O’s

# Objectives
- Implementation of Noughts and crosses using multiple agents.
- Playing the game using the designed models.
- Agent forming the quickest sequence and remaining undefeated till the end is declared as our winner.

# Approach
- Designing a layout which is a 3x3 grid.
- Agent training about the game play atmosphere using Expectimax, Minimax, Alpha- Beta, Q learning and Approximate Q learning algorithms.
- Define the agent which minimizes our utility and develop a counter strategy for our self to maximize our utility
- The limitations of minimax can be overcomed by using expectimax which further expands our utility.
- Further, we add a choice node to study actions of the agent and use Q learning algorithm to get the maximum utility.

# Agents Used

### Expectimax Agent
- The Expectimax search algorithm uses game theory to maximize expected utility. It's a tweak on the Minimax algorithm. Expectimax does not assume that the adversary (the minimizer) is playing optimally. This is handy for simulating situations when opponent agents aren't ideal or their behaviors are random.

- The Expectimax algorithm aids in exploiting non-optimal opponents. Because opponents are unpredictable, Expectimax can 'take a chance' and end up in a state with a higher utility than Minimax (not optimal).

- The Chance nodes calculate the 'anticipated utility' by averaging all available utilities.

### Minimax Agent
- Minimax is a recursive technique for determining the best move for a player given that the opponent is also playing optimally. Its purpose, as the name implies, is to minimize the maximum loss (minimize the worst case scenario)

- The Minimax algorithm relies on a back-and-forth between the two players, with the player whose "turn it is" aiming for the highest score. In turn, the opposing player determines the scores for each of the available moves by determining which of its potential moves has the lowest score.

- This function uses minimax() to assess all available movements before returning the best move the maximizer can make.

### Alpha- Beta Agent

- Alpha-beta pruning is a common algorithm modification that uses a less strict criterion for deciding when to delete nodes from a tree. 

- It's a useful technique for the Minimax algorithm. As the depth of the tree grows, the number of game states the minimax search algorithm must examine grows exponentially. 

- Since we cannot eliminate the exponent, we can reduce it by half. 

- There is a technique by which we can compute the correct minimax decision without checking each node of the game tree, and this technique is called pruning. 

- This involves two parameters, Alpha and Beta, for future expansion. It's called alpha-beta pruning.

### Q learning Agent

- Whereas in general game theory methods, such as the min-max algorithm, the algorithm assumes a perfect opponent who is so rational that each step it takes is to maximize its reward and minimize our agent reward, reinforcement learning does not even assume a model of the opponent, and the result can be surprisingly good.

- The most important thing to remember while approaching this reinforcement learning problem is to understand the three primary components: state, action, and reward. To begin, teach two agents to compete against one another and save their policies for 5000 rounds. Second, make the agent play against humans by loading the policy.

- We need a player class that represents our agency and can do the following:
  - Choose actions depending on the current status estimation.
  - Keep track of the game's many states.
  - After each game, update the states-value estimation.
  - The policy should be saved and loaded.

# Requirements:
Python 3.7

# Execution Guidelines:
Execute the ticTacToe.py file to start the game.

# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # If I use korean in here, I can't compile.....I don't know why....
        # So I write down with English though I'm not good at this..Thank you

        food_pos = newFood.asList()
        
        # min_food/ghost_dis is the most closest object's distance.
        # we have to plot the minimum distance, so I plot the very large value at first.
        min_food_dis = 100000
        min_ghost_dis = 100000
        
        for food in food_pos:
            min_food_dis = min(manhattanDistance(food, newPos), min_food_dis)

        # In min_ghost_dis, I plus the 'ghost's scared time' because if ghost's scared time is bigger, our agent is more safety
        for ghost_state in newGhostStates:
            ghost_x, ghost_y = ghost_state.getPosition()
            min_ghost_dis = min(manhattanDistance((int(ghost_x), int(ghost_y)), newPos) + ghost_state.scaredTimer, min_ghost_dis)

        if len(food_pos) == 0:
            min_food_dis = 0

        # Bigger 'min_ghost_dis' and Smaller 'min_food_dis + len(food_pos)' are helpful to our agent.
        # '/10' is my suggestion for the greatest score  --> I did plenty of tests... 
        # '+ 0.1' is only for avoid ZeroDivisionError.
        return successorGameState.getScore() + (min_ghost_dis) / ((min_food_dis + len(food_pos) / 10 + 0.1))

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """                        
    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        return self.minimax(gameState, 0, self.depth)[1]

    def minimax(self, gameState, agentIndex, depth):
        # If Current State is end of the game or there is no depth for search, we don't have to start minimax at all.
        # Just return the score of the Current State.
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState), Directions.STOP

        # num_Agent = number of Agent in this game
        # max_V = very small value for max_search
        # min_V = very large value for min_search
        # M_Action = Final output for minimax
        # agent_actions = Input Agent's Legal actions in the Current State
        num_Agent = gameState.getNumAgents()
        max_V = -100000
        min_V = 100000
        M_Action = Directions.STOP
        agent_actions = gameState.getLegalActions(agentIndex)

        # If Input Agent is the last agent, we are going to deeper!
        # It is possible that no ghost in the game.....
        # Because of this... I spent so much time....., I thought there's a ghost at least one...
        # Anyway, we have to consider the 'No ghost in game'
        if agentIndex == num_Agent - 1:
            next_Index = 0
            next_depth = depth - 1
        
        else:
            next_Index = agentIndex + 1
            next_depth = depth

        # Pacman's turn
        if agentIndex == 0:
            for action in agent_actions:
                next_state = gameState.generateSuccessor(agentIndex, action)
                next_value, __ = self.minimax(next_state, next_Index, next_depth)
                if next_value > max_V:
                    max_V = next_value
                    M_Action = action
            return max_V, M_Action

        # Ghost's turn
        else:
            for action in agent_actions:
                next_state = gameState.generateSuccessor(agentIndex, action)
                next_value, __ = self.minimax(next_state, next_Index, next_depth)
                if next_value < min_V:
                    min_V = next_value
                    M_Action = action
            return min_V, M_Action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.AlphaBeta(gameState, 0, self.depth, -100000, 100000)[1]

    def AlphaBeta(self, gameState, agentIndex, depth, alpha, beta):
        # Similar to minimax.
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState), Directions.STOP

        num_Agent = gameState.getNumAgents()
        max_V = -100000
        min_V = 100000
        M_Action = Directions.STOP
        agent_actions = gameState.getLegalActions(agentIndex)

        if agentIndex == num_Agent - 1:
            next_Index = 0
            next_depth = depth - 1
        
        else:
            next_Index = agentIndex + 1
            next_depth = depth

        # Pacman's turn
        if agentIndex == 0:
            for action in agent_actions:
                next_state = gameState.generateSuccessor(agentIndex, action)
                next_value, __= self.AlphaBeta(next_state, next_Index, next_depth, alpha, beta)
                if next_value > max_V:
                    max_V = next_value
                    M_Action = action
                    # If max_V is bigger than beta, we don't have to search the whole loop.
                    if max_V > beta:
                        return max_V, M_Action
                    alpha = max(alpha, max_V)
            return max_V, M_Action

        # Ghost's turn
        else:
            for action in agent_actions:
                next_state = gameState.generateSuccessor(agentIndex, action)
                next_value, __= self.AlphaBeta(next_state, next_Index, next_depth, alpha, beta)
                if next_value < min_V:
                    min_V = next_value
                    M_Action = action
                    # If min_V is smaller than alpha, we don't have to search the whole loop.
                    if min_V < alpha:
                        return min_V, M_Action
                    beta = min(beta, min_V)
            return min_V, M_Action


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

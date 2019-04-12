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
import random
import sys
import util

from game import Agent
from util import manhattanDistance


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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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

        "*** YOUR CODE HERE ***"
        nearestGhostDistance = float('inf')
        nearestFoodDistance = float('inf')

        for ghostState in newGhostStates:
            nearestGhostDistance = min(manhattanDistance(newPos, ghostState.getPosition()), nearestGhostDistance)

        if nearestGhostDistance < 2:
            return -sys.maxint

        for food in newFood.asList():
            nearestFoodDistance = min(manhattanDistance(newPos, food), nearestFoodDistance)

        leftFoodScore = 0
        if successorGameState.getNumFood() < currentGameState.getNumFood():
            leftFoodScore += 100


        if successorGameState.isWin():
            return sys.maxint
        else:
            return successorGameState.getScore() - nearestFoodDistance + leftFoodScore


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
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
        """
        "*** YOUR CODE HERE ***"

        def maximizingAgent(gameState, currentDepth):

            if currentDepth == 0 or (gameState.isLose() or gameState.isWin()):
                return self.evaluationFunction(gameState)

            v = list()

            for action in gameState.getLegalActions(agentIndex=0):
                v.append(minimizingAgent(1, gameState.generateSuccessor(0, action), currentDepth))

            return max(v)

        def minimizingAgent(agentIndex, gameState, currentDepth):

            if currentDepth == 0 or (gameState.isLose() or gameState.isWin()):
                return self.evaluationFunction(gameState)

            v = list()

            for action in gameState.getLegalActions(agentIndex):

                if agentIndex == (gameState.getNumAgents() - 1):
                    v.append(maximizingAgent(gameState.generateSuccessor(agentIndex, action)
                                             , currentDepth - 1))
                else:
                    v.append(minimizingAgent(agentIndex + 1, gameState.generateSuccessor(agentIndex, action)
                                             , currentDepth))

            return min(v)

        score = list()

        for action in gameState.getLegalActions():
            score.append(minimizingAgent(1, gameState.generateSuccessor(0, action), currentDepth=self.depth))

        return (gameState.getLegalActions())[score.index(max(score))]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def maximizingAgent(gameState, currentDepth, alpha, beta):

            if currentDepth == 0 or (gameState.isLose() or gameState.isWin()):
                return self.evaluationFunction(gameState)

            v = -sys.maxint

            for action in gameState.getLegalActions(agentIndex=0):
                v = max(v, minimizingAgent(1, gameState.generateSuccessor(0, action), currentDepth, alpha, beta))
                if v > beta:
                    return v
                alpha = max(alpha, v)

            return v

        def minimizingAgent(agentIndex, gameState, currentDepth, alpha, beta):

            if currentDepth == 0 or (gameState.isLose() or gameState.isWin()):
                return self.evaluationFunction(gameState)

            v = sys.maxint

            for action in gameState.getLegalActions(agentIndex):

                if agentIndex == (gameState.getNumAgents() - 1):
                    v = min(v, maximizingAgent(gameState.generateSuccessor(agentIndex, action)
                                             , currentDepth - 1, alpha, beta))
                else:
                    v = min(v, minimizingAgent(agentIndex + 1, gameState.generateSuccessor(agentIndex, action)
                                             , currentDepth, alpha, beta))

                if v < alpha:
                    return v
                beta = min(beta, v)

            return v

        score = list()
        alpha = -sys.maxint

        for action in gameState.getLegalActions():
            score.append(minimizingAgent(1, gameState.generateSuccessor(0, action), currentDepth=self.depth
                                         , alpha=alpha, beta=float('inf')))
            alpha = max(alpha, max(score))

        return (gameState.getLegalActions())[score.index(max(score))]


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

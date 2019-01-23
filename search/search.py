# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    stack = util.Stack()
    visited = []

    start_state = problem.getStartState()
    moves = []

    current_state = [start_state, moves]

    while not problem.isGoalState(current_state[0]) :
        current_position, moves = current_state 
        successors_list = problem.getSuccessors(current_position)
        
        for successor in successors_list:
            stack.push((successor[0], moves + [successor[1]]) )
        
        while True:
            if stack.isEmpty() :
                return None
            
            successor = stack.pop() 
            
            if successor[0] not in visited :
                break

        current_state = successor
        visited.append(successor[0])
    
    #print current_state[1]
    return current_state[1]

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    queue = util.Queue()
    visited = []

    queue.push((problem.getStartState(), [], 0))
    (current_state, moves, cost) = queue.pop()

    visited.append(current_state)

    while not problem.isGoalState(current_state) :

        successors_list = problem.getSuccessors(current_state)

        for successor in successors_list :
            if successor[0] not in visited :
                next_state = successor[0]
                next_move = successor[1]
                next_cost = successor[2]

                queue.push((next_state, moves + [next_move], cost + next_cost))
                visited.append(next_state)
        
        (current_state, moves, cost) = queue.pop()

    return moves

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    priority_queue = util.PriorityQueue()
    visited = []

    priority_queue.push((problem.getStartState(), [], 0), 0)
    (current_state, moves, cost) = priority_queue.pop()

    visited.append((current_state, cost))

    while not problem.isGoalState(current_state) :
        successors_list = problem.getSuccessors(current_state)

        for successor in successors_list :
            is_visited = False

            next_state = successor[0]
            next_move = successor[1]
            total_cost = cost + successor[2]

            for (visited_state, visited_cost) in visited :
                if (next_state == visited_state) and (total_cost >= visited_cost) :
                    is_visited = True
                    break

            if not is_visited :
                priority_queue.push((next_state, moves + [next_move], total_cost), total_cost)
                visited.append((next_state, total_cost))
    
        (current_state, moves, cost) = priority_queue.pop()

    return moves


def iterativeDeepeningSearch(problem) :
    stack = util.Stack()
    limit = 1

    while True :
        visited = []
        stack.push((problem.getStartState(), [], 0))

        (current_state, moves, cost) = stack.pop()

        visited.append(current_state)

        while not problem.isGoalState(current_state) :
            successors_list = problem.getSuccessors(current_state)

            for successor in successors_list :
                next_state = successor[0]
                next_move = successor[1]
                next_cost = successor[2]

                if (not next_state in visited) and (cost + next_cost <= limit) :
                    stack.push((next_state, moves + [next_move], cost + next_cost))
                    visited.append(next_state)

            if stack.isEmpty() :
                break

            (current_state, moves, cost) = stack.pop()

        if problem.isGoalState(current_state) :
            return moves

        limit += 1


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
ids = iterativeDeepeningSearch
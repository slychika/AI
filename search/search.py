# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

# Edited by Heather Dykstra
# thanks to Hannah Thomas and Alex Ackerman for all the help

# WRITTEN QUESTIONS ARE ANSWERED AT THE BOTTOM

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    #"*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    #FIFO Stack
    #add start to frontier
    #loop! while stack has things in it
    #pop top
    #is goal?
        #Return directions
    #has been visited?
        #make it visited
    #append successors of top
        #dont forget to add the direction!
    #Thanks to Hannah Thomas for walking through this w/me
    
    frontier = util.Stack()
    visited = {}
 
    state = problem.getStartState()
    frontier.push([state, []])
 
    while not frontier.isEmpty():
        state, directions = frontier.pop()
        
        if (problem.isGoalState(state)):
            return directions
 
        if not (state in visited): #thanks to alex for helping me get this part...
            visited[state] = True
           
            for (kid, direction, cost) in problem.getSuccessors(state):
                frontier.push([kid, directions + [direction]])
 
    return None

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    #QUEUE for frontier.
    #otherwise, same as DFS

    frontier = util.Queue()
    visited = {}
    
    state = problem.getStartState()
    frontier.push([state, []])
 
    while not frontier.isEmpty():
        state, directions = frontier.pop()
        
        if (problem.isGoalState(state)):
            return directions
 
        if not (state in visited):
            visited[state] = True
           
            for (kid, direction, cost) in problem.getSuccessors(state):
                frontier.push([kid, directions + [direction]])
 
    return None
    

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    #PROPROTY QUEUE instead of a queue or stack!
    #take the sketch from above
    #add cost
    #flip the if goal to after checking the node
    #to make sure we add our cost correctly in the return of visited
    
    frontier = util.PriorityQueue()
    visited = {}
    cost = {}
    
    state = problem.getStartState()   
    frontier.push((state, None, None, 0), 0) #(currentState, previousState, action, stepCost), cost[state] + stepCost)

    while not frontier.isEmpty():
        state, prevNode, action, stepCost = frontier.pop()
        if state not in visited:
            #add the state and total cost
            if prevNode == None:
                visited[state] = []
            	cost[state] = 0
            if prevNode != None:
                #calulate the path we take, keeping track of prev. node
                path = list(visited[prevNode])
                path.append(action)
                visited[state] = path
		cost[state] = cost[prevNode] + stepCost
            #check for goal now
            if problem.isGoalState(state):
                return visited[state]
            #if not goal, push!
            kids = problem.getSuccessors(state)
            for kid, action, stepCost in kids:
                frontier.push((kid, state, action, stepCost), cost[state] + stepCost)

    return None

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    #Same code as ucf plus an added cost if we arent at our node
    #(the heuristic cost)
    frontier = util.PriorityQueue()
    visited = {}
    cost = {}
    
    state = problem.getStartState()   
    frontier.push((state, None, None, 0), 0) #(currentState, previousState, action, stepCost), cost[state] + stepCost + heuristic cost)

    while not frontier.isEmpty():
        state, prevNode, action, stepCost = frontier.pop()
        if state not in visited:
            #add the state and total cost
            if prevNode == None:
                visited[state] = []
            	cost[state] = 0
            if prevNode != None:
                #calulate the path we take, keeping track of prev. node
                path = list(visited[prevNode])
                path.append(action)
                visited[state] = path
		cost[state] = cost[prevNode] + stepCost
            #check for goal now
            if problem.isGoalState(state):
                return visited[state]
            #if not goal, push!
            kids = problem.getSuccessors(state)
            for kid, action, stepCost in kids:
                frontier.push((kid, state, action, stepCost), cost[state] + stepCost+ heuristic(kid, problem)) #add the extra heuristic value here!

    return None
    


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch



#-------------------------------------------------------------------------------
#Questions after DFS:
#1. Yes, after working throught the algorithm, this is the expected order
#2. No, he only goes to through the actions I gave him, which account for dead-
#   ends
#3. No, DFS only cares about the lowest depth, it does not factor in how much
#   getting to each node costs
#-------------------------------------------------------------------------------
#Questions after all search methods:
#1. DFS: Pacman doesn't do the best thing, he goes back and forth between edge
#       edge a lot. He does not explore nearly as many nodes as the other
#       algorithms, but does not score as well, because he spends lots of
#       time meandering
#   BFS: Pacman takes the optimal path to get to the dot as quick as possible
#       he explores all but one node
#   UCS: Pacman takes the optimal path to get to the dot as quick as possible
#       he explores all but one node
#   ASTAR: Pacman takes the optimal path to get to the dot as quick as possible
#       he explores all but one node
#-------------------------------------------------------------------------------



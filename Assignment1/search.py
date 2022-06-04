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

from re import search
import util
from util import Stack, Queue, PriorityQueue

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

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    
    # DFS에서 fringe는 LIFO STACK으로 정의함.
    fringe = Stack()
    # 이미 확장한 노드들은 cycle을 막기 위해 따로 set 선언.
    Expanded = set()
    # fringe에 시작 튜플 push
    fringe.push((problem.getStartState(),[]))

    

    # DFS starts!! 

    # fringe가 비어있는지 체크
    # fringe가 비어있지 않다면 시작! 
    while fringe.isEmpty() is not True:
        # state = '노드k' : str
        # path_to_state = ['시작노드1 -> 노드2', '노드2 -> 노드3', ... , '노드k-1 -> 노드k'] : list of str
        # stack.pop은 LIFO 방식
        state, path_to_state = fringe.pop()

        # '노드 k'가 'goal state'라면 [start state -> goal state]의 모든 경로를 리스트로 반환.
        if problem.isGoalState(state):
            return path_to_state

        # 이미 한번 접근했던 state는 재확장하지 않음.
        if state in Expanded:
            continue
        else:
            Expanded.add(state)
            # 자식 state의 '자식 노드', '경로'를 fringe에 ('자식 노드', ['시작 노드 -> 부모 노드', '부모 노드 -> 자식 노드']) 튜플로 push
            for new_state, edge, __ in problem.getSuccessors(state):
                fringe.push((new_state, path_to_state + [edge]))              
                
    



def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    # BFS에서 fringe는 FIFO QUEUE으로 정의함.
    fringe = Queue()
    # 이미 확장한 노드들은 cycle을 막기 위해 따로 set 선언.
    Expanded = set()
    # fringe에 시작 튜플 push
    fringe.push((problem.getStartState(),[]))

    

    # BFS starts!! 

    # fringe가 비어있는지 체크
    # fringe가 비어있지 않다면 시작! 
    while fringe.isEmpty() is not True:
        # state = '노드k' : str
        # path_to_state = ['시작노드1 -> 노드2', '노드2 -> 노드3', ... , '노드k-1 -> 노드k'] : list of str
        # queue.pop은 FIFO 방식
        state, path_to_state = fringe.pop()

        # '노드 k'가 'goal state'라면 [start state -> goal state]의 모든 경로를 리스트로 반환.
        if problem.isGoalState(state):
            return path_to_state

        # 이미 한번 접근했던 state는 재확장하지 않음.
        if state in Expanded:
            continue
        else:
            Expanded.add(state)
            # 자식 state의 '자식 노드', '경로'를 fringe에 ('자식 노드', ['시작 노드 -> 부모 노드', '부모 노드 -> 자식 노드']) 튜플로 push
            for new_state, edge, __ in problem.getSuccessors(state):
                fringe.push((new_state, path_to_state + [edge]))          


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # UCS에서 fringe는 PRIORITY QUEUE으로 정의함.
    fringe = PriorityQueue()
    # 이미 확장한 노드들은 cycle을 막기 위해 따로 set 선언.
    Expanded = set()
    # fringe에 '시작 튜플 + priority' push : ('노드' : str, path : list, cost : float), priority : float
    fringe.push((problem.getStartState(),[], 0), 0)

    

    # UCS starts!! 

    # fringe가 비어있는지 체크
    # fringe가 비어있지 않다면 시작! 
    while fringe.isEmpty() is not True:
        # state = '노드k' : str
        # path_to_state = ['시작노드1 -> 노드2', '노드2 -> 노드3', ... , '노드k-1 -> 노드k'] : list of str
        # cost_to_state = cost for (start 노드 -> 노드 k) : float
        state, path_to_state, cost_to_state = fringe.pop()

        # '노드 k'가 'goal state'라면 [start state -> goal state]의 모든 경로를 리스트로 반환.
        if problem.isGoalState(state):
            return path_to_state

        # 이미 한번 접근했던 state는 재확장하지 않음.
        if state in Expanded:
            continue
        else:
            Expanded.add(state)
            # 자식 state의 '자식 노드', '경로', 비용을 fringe에 ('자식 노드', ['시작 노드 -> 부모 노드', '부모 노드 -> 자식 노드'], 비용) 튜플로 push
            # '우선순위 = 비용' 으로 하여 최소 비용을 가진 튜플이 가장 먼저 선택되도록 함.
            for new_state, edge, cost in problem.getSuccessors(state):
                fringe.push((new_state, path_to_state + [edge], cost_to_state + cost), cost_to_state + cost)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # A*에서 fringe는 PRIORITY QUEUE으로 정의함.
    fringe = PriorityQueue()
    # 이미 확장한 노드들은 cycle을 막기 위해 따로 set 선언.
    Expanded = set()
    # fringe에 '시작 튜플 + priority' push : ('노드' : str, path : list, cost : float), priority : float
    fringe.push((problem.getStartState(),[], 0), 0)

    

    # A* starts!! 

    # fringe가 비어있는지 체크
    # fringe가 비어있지 않다면 시작! 
    while fringe.isEmpty() is not True:
        # state = '노드k' : str
        # path_to_state = ['시작노드1 -> 노드2', '노드2 -> 노드3', ... , '노드k-1 -> 노드k'] : list of str
        # cost_to_state = cost for (start 노드 -> 노드 k) : float
        state, path_to_state, cost_to_state = fringe.pop()

        # '노드 k'가 'goal state'라면 [start state -> goal state]의 모든 경로를 리스트로 반환.
        if problem.isGoalState(state):
            return path_to_state

        # 이미 한번 접근했던 state는 재확장하지 않음.
        if state in Expanded:
            continue
        else:
            Expanded.add(state)
            # 자식 state의 '자식 노드', '경로', 비용을 fringe에 ('자식 노드', ['시작 노드 -> 부모 노드', '부모 노드 -> 자식 노드'], 비용) 튜플로 push
            # '우선순위 = 비용 + 휴리스틱 값' 으로 하여 최소 비용을 가진 튜플이 가장 먼저 선택되도록 함.
            for new_state, edge, cost in problem.getSuccessors(state):
                fringe.push((new_state, path_to_state + [edge], cost_to_state + cost), cost_to_state + cost + heuristic(new_state, problem))



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

# myAgents.py
# ---------------
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

from game import Agent
from searchProblems import PositionSearchProblem

import util
import time
import search

"""
IMPORTANT
`agent` defines which agent you will use. By default, it is set to ClosestDotAgent,
but when you're ready to test your own agent, replace it with MyAgent
"""
def createAgents(num_pacmen, agent='MyAgent'):
    return [eval(agent)(index=i) for i in range(num_pacmen)]

class MyAgent(Agent):

    def findMyPath(self, gameState):
        # 맵의 맨 오른쪽, 맨 위의 좌표
            # x 좌표 = E_X
            # y 좌표 = E_Y
        E_X = gameState.getWidth() - 1
        E_Y = gameState.getHeight() - 1

        # 맵의 중심 좌표
            # x 좌표 = C_X
            # y 좌표 = C_Y
        C_X = E_X/2 - 1
        C_Y = E_Y/2 - 1
        
        # self.Area가 할당되지 않은 경우에만 돌아감 (Agent 생성 시에 딱 한번)
        # 각 Agent가 맡게될 Area 할당
        if self.Area == 0: 
            pacmanpositions = gameState.getPacmanPositions()

            IndexAgent = [-1, -1, -1, -1]
            Area1 = []
            Area2 = []
            Area3 = []
            Area4 = []

            closest_1 = 10000000
            closest_2 = 10000000
            closest_3 = 10000000
            closest_4 = 10000000

            for i in range(0,4):
                x,y = pacmanpositions[i]

                if x+y < closest_1:
                    closest_1 = x+y
                    Area1.append(i) 

                if (E_X-x)+y < closest_2:
                    closest_2 = (E_X-x)+y
                    Area2.append(i) 
                
                if (E_X-x)+(E_Y-y) < closest_3:
                    closest_3 = (E_X-x)+(E_Y-y)
                    Area3.append(i) 

                if x+(E_Y-y) < closest_4:
                    closest_3 = x+(E_Y-y)
                    Area4.append(i) 
            
            while (IndexAgent[0] == -1):
                if Area1[-1] not in IndexAgent:
                    IndexAgent[0] = Area1[-1]
                else:
                    del Area1[-1]
            
            while (IndexAgent[1] == -1):
                if Area2[-1] not in IndexAgent:
                  IndexAgent[1] = Area2[-1]
                else:
                    del Area2[-1]

            while (IndexAgent[2] == -1):
                if Area3[-1] not in IndexAgent:
                    IndexAgent[2] = Area3[-1]
                else:
                    del Area3[-1]

            while (IndexAgent[3] == -1):
                if Area4[-1] not in IndexAgent:
                    IndexAgent[3] = Area4[-1]
                else:
                    del Area4[-1]

            for i in range(0,4):
                if IndexAgent[i] == self.index:
                    self.Area = i+1


        # 각 영역에 해당하는 food 리스트 생성 --> Areafood = []
        food = gameState.getFood().asList()
        Areafood = []

        for x,y in food:

            if self.Area == 1:
                if x < C_X and y < C_Y:
                    Areafood.append((x,y))

            elif self.Area == 2:
                if x >= C_X and y < C_Y:
                    Areafood.append((x,y))

            elif self.Area == 3:
                if x >= C_X and y >= C_Y:
                    Areafood.append((x,y))

            else:
                if x < C_X and y >= C_Y:
                    Areafood.append((x,y))


        # 만약, 자신의 영역에 더 이상 남은 food가 없다면, 반시계 방향의 영역으로 넘어감
        if len(Areafood) == 0:
            Areafood = food
            self.Area = self.Area % 4 + 1

        # 자신의 영역에 해당하는 food 리스트로 findPathToClosestDot 실시!!
        problem = AnyFoodSearchProblem(gameState, self.index)
        pos = gameState.getPacmanPosition(self.index)
        pacmanCurrent = [pos, [], 0]
        visitedPosition = set()
        fringe = util.PriorityQueue()
        fringe.push(pacmanCurrent, pacmanCurrent[2])

        while not fringe.isEmpty():
            pacmanCurrent = fringe.pop()
            if pacmanCurrent[0] in visitedPosition:
                continue
            else:
                visitedPosition.add(pacmanCurrent[0])
            if pacmanCurrent[0] in Areafood:
                return pacmanCurrent[1]
            else:
                pacmanSuccessors = problem.getSuccessors(pacmanCurrent[0])
            Successor = []
            for item in pacmanSuccessors:  # item: [(x,y), 'direction', cost]
                if item[0] not in visitedPosition:
                    pacmanRoute = pacmanCurrent[1].copy()
                    pacmanRoute.append(item[1])
                    sumCost = pacmanCurrent[2]


                    # 일종의 휴리스틱 함수
                        # 각 Area의 기준점에 대하여 멀어지는 방향은 가중치를 받는다.
                        # 멀어짐의 기준은 맨해튼 거리의 개념을 활용
                        
                    ix,iy = item[0]
                    if self.Area == 1:
                        if ix >= C_X:
                            sumCost += (ix)*2
                        if iy >= C_Y:
                            sumCost += (iy)*2

                    elif self.Area == 2:
                        if ix < C_X:
                            sumCost += (E_X - ix)*2
                        if iy >= C_Y:
                            sumCost += (iy)*2

                    elif self.Area == 3:
                        if ix < C_X:
                            sumCost += (E_X - ix)*2
                        if iy < C_Y:
                            sumCost += (E_Y - iy)*2
                
                    else:
                        if ix >= C_X:
                            sumCost += (ix)*2
                        if iy < C_Y:
                            sumCost += (E_Y - iy)*2
                
                    Successor.append([item[0], pacmanRoute, sumCost + item[2]])
            for item in Successor:
                fringe.push(item, item[2])

        return pacmanCurrent[1]

    def getAction(self, state):
        
        return self.findMyPath(state)[0]

    def initialize(self):
        """
        Intialize anything you want to here. This function is called
        when the agent is first created. If you don't need to use it, then
        leave it blank
        """

        "*** YOUR CODE HERE ***"
        self.Area = 0


"""
Put any other SearchProblems or search methods below. You may also import classes/methods in
search.py and searchProblems.py. (ClosestDotAgent as an example below)
"""

class ClosestDotAgent(Agent):

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """
        # Here are some useful elements of the startState
        startPosition = gameState.getPacmanPosition(self.index)
        food = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState, self.index)


        "*** YOUR CODE HERE ***"

        pacmanCurrent = [problem.getStartState(), [], 0]
        visitedPosition = set()
        # visitedPosition.add(problem.getStartState())
        fringe = util.PriorityQueue()
        fringe.push(pacmanCurrent, pacmanCurrent[2])
        while not fringe.isEmpty():
            pacmanCurrent = fringe.pop()
            if pacmanCurrent[0] in visitedPosition:
                continue
            else:
                visitedPosition.add(pacmanCurrent[0])
            if problem.isGoalState(pacmanCurrent[0]):
                return pacmanCurrent[1]
            else:
                pacmanSuccessors = problem.getSuccessors(pacmanCurrent[0])
            Successor = []
            for item in pacmanSuccessors:  # item: [(x,y), 'direction', cost]
                if item[0] not in visitedPosition:
                    pacmanRoute = pacmanCurrent[1].copy()
                    pacmanRoute.append(item[1])
                    sumCost = pacmanCurrent[2]
                    Successor.append([item[0], pacmanRoute, sumCost + item[2]])
            for item in Successor:
                fringe.push(item, item[2])
        return pacmanCurrent[1]

    def getAction(self, state):
        return self.findPathToClosestDot(state)[0]

class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem, but has a
    different goal test, which you need to fill in below.  The state space and
    successor function do not need to be changed.

    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.

    You can use this search problem to help you fill in the findPathToClosestDot
    method.
    """

    def __init__(self, gameState, agentIndex):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition(agentIndex)
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x,y = state
        if self.food[x][y] == True:
            return True
        return False

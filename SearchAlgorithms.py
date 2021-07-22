import operator
class Node:
    id = None  # Unique value for each node.
    up = None  # Represents value of neighbors (up, down, left, right).
    down = None
    left = None
    right = None
    previousNode = None  # Represents value of neighbors.
    edgeCost = None  # Represents the cost on the edge from any parent to this node.
    gOfN = None  # Represents the total edge cost
    hOfN = None  # Represents the heuristic value
    heuristicFn = None  # Represents the value of heuristic function
    previousNode2 = None # Represents the value of neighbors in BDS from back

    def __init__(self, value):
        self.value = value


class SearchAlgorithms:
    ''' * DON'T change Class, Function or Parameters Names and Order
        * You can add ANY extra functions,
          classes you need as long as the main
          structure is left as is '''
    path = []  # Represents the correct path from start node to the goal node.
    fullPath = []  # Represents all visited nodes from the start node to the goal node.
    totalCost = -1  # Represents the total cost in case using UCS, AStar (Euclidean or Manhattan)
    board=[];
    def __init__(self, mazeStr, heristicValue=None):
        ''' mazeStr contains the full board
         The board is read row wise,
        the nodes are numbered 0-based starting
        the leftmost node'''
        self.board=str.split(mazeStr," ")
        x= len(self.board)
        for i in range(x):
            self.board[i]=str.split(self.board[i],",")
        self.Fill_Board(x,1,heristicValue)
        self.Fill_Board(x,2,heristicValue)

    def state(self,board):
        maze = ""
        x = len(board)
        for i in range(x):
            y = len(board[i])
            for j in range(y):
                maze += str(board[i][j].value)
                if (j != y - 1):
                    maze += ","
            if (i != x - 1):
                maze += " "
        return maze
    def Fill_Board(self,x,iter,heristicValue=None):
        count=0
        for i in range(x):
            y=len(self.board[i])
            for j in range(y):
                if (iter==1):
                    node=Node(self.board[i][j])
                elif (iter==2):
                    node=Node(self.board[i][j])
                    node.value=node.value.value
                node.id=count
                if (i==0 and j==0):
                    node.right=self.board[i][j+1]
                    node.down=self.board[i+1][j]
                elif(i==0 and j==y-1):
                    node.left=self.board[i][j-1]
                    node.down=self.board[i+1][j]
                elif(i==x-1 and j==0):
                    node.up = self.board[i - 1][j]
                    node.right = self.board[i][j + 1]
                elif (i==x-1 and j==y-1):
                    node.up = self.board[i - 1][j]
                    node.left = self.board[i][j - 1]
                elif(i==0):
                    node.right = self.board[i][j + 1]
                    node.left = self.board[i][j - 1]
                    node.down = self.board[i + 1][j]
                elif(j==0):
                    node.right = self.board[i][j + 1]
                    node.down = self.board[i + 1][j]
                    node.up=self.board[i-1][j]
                elif(i==x-1):
                    node.right = self.board[i][j + 1]
                    node.left = self.board[i][j - 1]
                    node.up = self.board[i - 1][j]
                elif(j==y-1):
                    node.left = self.board[i][j - 1]
                    node.up = self.board[i - 1][j]
                    node.down = self.board[i + 1][j]
                else:
                    node.right = self.board[i][j + 1]
                    node.left = self.board[i][j - 1]
                    node.up = self.board[i - 1][j]
                    node.down = self.board[i + 1][j]
                if (heristicValue != None):
                    node.hOfN=heristicValue[count]
                count+=1
                self.board[i][j]=node

    def getMoves(self, node):
        moves = [];
        if (node.up != None and node.previousNode != node.up):
            row = int(node.up.id / (len(self.board[0])))
            col = node.up.id - row * (len(self.board[0]))
            moves.append(self.board[row][col])
        if (node.down != None and node.previousNode != node.down):
            row = int(node.down.id / (len(self.board[0])))
            col = node.down.id - row * (len(self.board[0]))
            moves.append(self.board[row][col])
        if (node.left != None and node.previousNode != node.left):
            row = int(node.left.id / (len(self.board[0])))
            col = node.left.id - row * (len(self.board[0]))
            moves.append(self.board[row][col])
        if (node.right != None and node.previousNode != node.right):
            row = int(node.right.id / (len(self.board[0])))
            col = node.right.id - row * (len(self.board[0]))
            moves.append(self.board[row][col])

        return moves

    def find_start(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j].value == "S":
                    return i, j

    def find_end(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j].value == "E":
                    return i, j

    def Rec_dls(self, node, limit, myQueue, visited):
        while myQueue:
            currentNode = myQueue.pop(0)
            visited.add(currentNode)
            if currentNode.value == 'E':
                row = int(currentNode.id / (len(self.board[0])))
                col = currentNode.id - row * (len(self.board[0]))
                return row,col
            if limit == 0:
                return -1,-1
            for child in self.getMoves(currentNode):
                if child not in visited and child not in myQueue and child.value!="#":
                    child.previousNode = currentNode
                    myQueue.insert(0, child)
                    row1,col1=self.Rec_dls(child, limit - 1, myQueue, visited)
                    if row1 !=-1 and col1!=-1:
                        return row1,col1
        return -1,-1



    def DLS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        self.path=[]
        self.fullPath=[]
        row, col = self.find_start()
        startNode = self.board[row][col]
        myQueue = [startNode]
        visited = set()
        row,col=-1,-1
        row,col=self.Rec_dls(startNode, 50, myQueue, visited)

        if (row!=-1 and col!=-1):
            while True:
                nodePath=self.board[row][col]
                self.path.insert(0,nodePath)
                if (nodePath.value=='S'):
                    break
                prevID=nodePath.previousNode.id
                row = int(prevID / (len(self.board[0])))
                col = prevID - row * (len(self.board[0]))

            for i in range(len(self.board)):
                for j in range(len(self.board[0])):
                    if self.board[i][j] not in visited:
                        self.board[i][j].value='#'


            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    self.fullPath.append(self.board[i][j].value)
                if i != len(self.board) - 1:
                    self.fullPath.append(" ")

            for i in range(len(self.board)):
                for j in range(len(self.board[0])):
                    if self.board[i][j] not in self.path:
                        self.board[i][j].value='#'

        # self.path=self.board
            self.path=[]
            for i in range(len(self.board)):
                for j in range(len(self.board[0])):
                    self.path.append(self.board[i][j].value)
                if i != len(self.board) - 1:
                    self.path.append(" ")
        else:
            self.path="NO SOLUTION"
            self.fullPath="NO SOLUTION"
        return self.path, self.fullPath

    def BDS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        self.path=[]
        self.fullPath=[]
        row1, col1 = self.find_start()
        startNode = self.board[row1][col1]
        row2, col2 = self.find_end()
        endNode = self.board[row2][col2]
        myQueue1 = [startNode]
        myQueue2 = [endNode]
        visited = set()
        id=-1
        while myQueue1 and myQueue2:
            if len(myQueue1) != 0:
                current = myQueue1.pop(0)
                visited.add(current)
                if current.value == 'E' or current in myQueue2:
                    id=current.id
                    row = int(id / (len(self.board[0])))
                    col = id - row * (len(self.board[0]))
                    break

            for next_move1 in self.getMoves(current):
                if next_move1 not in visited and next_move1.value!="#":
                    next_move1.previousNode=current
                    myQueue1.append(next_move1)

            if len(myQueue2) != 0:
                current2 = myQueue2.pop(0)
                visited.add(current2)
                if current2.value == 'S' or current2 in myQueue1:
                    id=current2.id
                    row = int(id / (len(self.board[0])))
                    col = id - row * (len(self.board[0]))
                    break
            for next_move2 in self.getMoves(current2):
                if next_move2 not in visited and next_move2.value!="#":
                    next_move2.previousNode2 = current2
                    myQueue2.append(next_move2)

        row2=row
        col2=col
        if id!=-1:
            while True:
                nodePath = self.board[row][col]
                self.path.insert(0, nodePath)
                if (nodePath.value == 'S'):
                    break
                prevID = nodePath.previousNode.id
                row = int(prevID / (len(self.board[0])))
                col = prevID - row * (len(self.board[0]))

            while True:
                nodePath = self.board[row2][col2]
                self.path.insert(0, nodePath)
                if (nodePath.value == 'E'):
                    break
                prevID = nodePath.previousNode2.id
                row2 = int(prevID / (len(self.board[0])))
                col2 = prevID - row2 * (len(self.board[0]))

            for i in range(len(self.board)):
                for j in range(len(self.board[0])):
                    if self.board[i][j] not in visited:
                        self.board[i][j].value = '#'

            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    self.fullPath.append(self.board[i][j].value)
                if i != len(self.board) - 1:
                    self.fullPath.append(" ")

            for i in range(len(self.board)):
                for j in range(len(self.board[0])):
                    if self.board[i][j] not in self.path:
                        self.board[i][j].value = '#'

            # self.path=self.board
            self.path = []
            for i in range(len(self.board)):
                for j in range(len(self.board[0])):
                    self.path.append(self.board[i][j].value)
                if i!=len(self.board)-1:
                    self.path.append(" ")
        else:
            self.path = "NO SOLUTION"
            self.fullPath = "NO SOLUTION"
        return self.path, self.fullPath

    def BFS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        self.path=[]
        self.fullPath=[]
        row,col=self.find_start()
        startNode = self.board[row][col]
        myQueue =[startNode]
        visited = set()
        row,col=-1,-1
        while myQueue:
            currentNode = myQueue.pop(0)
            visited.add(currentNode)
            if currentNode.value=='E':
                row = int(currentNode.id / (len(self.board[0])))
                col = currentNode.id - row * (len(self.board[0]))
                break
            for child in self.getMoves(currentNode):
                if child not in visited and child not in myQueue:
                    child.previousNode=currentNode
                    myQueue.append(child)
            myQueue.sort(key=operator.attrgetter('hOfN'))

        if (row!=-1 and col!=-1):
            self.totalCost=0
            while True:
                nodePath=self.board[row][col]
                self.path.insert(0,nodePath)
                self.totalCost+=nodePath.hOfN
                if (nodePath.value=='S'):
                    break
                prevID=nodePath.previousNode.id
                row = int(prevID / (len(self.board[0])))
                col = prevID - row * (len(self.board[0]))

            for i in range(len(self.board)):
                for j in range(len(self.board[0])):
                    if self.board[i][j] not in visited:
                        self.board[i][j].value='#'


            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    self.fullPath.append(self.board[i][j].value)
                if i != len(self.board) - 1:
                    self.fullPath.append(" ")

            for i in range(len(self.board)):
                for j in range(len(self.board[0])):
                    if self.board[i][j] not in self.path:
                        self.board[i][j].value='#'

        # self.path=self.board
            self.path=[]
            for i in range(len(self.board)):
                for j in range(len(self.board[0])):
                    self.path.append(self.board[i][j].value)
                if i != len(self.board) - 1:
                    self.path.append(" ")
        else:
            self.path = "NO SOLUTION"
            self.fullPath = "NO SOLUTION"


        return self.path, self.fullPath, self.totalCost



def main():
    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.')
    path, fullPath = searchAlgo.DLS()
    print('**DLS**\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\n\n')

                #######################################################################################

    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.')
    path, fullPath = searchAlgo.BDS()
    print('**BDS**\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\n\n')
                #######################################################################################

    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.', [0, 15, 2, 100, 60, 35, 30, 3
                                                                                                             , 100, 2, 15, 60, 100, 30, 2
                                                                                                             , 100, 2, 2, 2, 40, 30, 2, 2
                                                                                                             , 100, 100, 3, 15, 30, 100, 2
                                                                                                             , 100, 0, 2, 100, 30])
    path, fullPath, TotalCost = searchAlgo.BFS()
    print('** BFS **\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\nTotal Cost: ' + str(
        TotalCost) + '\n\n')
               #######################################################################################




main()

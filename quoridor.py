import time
import random
from graph import Graph

class QuoridorGraph(Graph):
    def __init__(self):
        graph_dict = {}
        numSquares = 9
        for x in range(numSquares):
            for y in range(numSquares):
                graph_dict[(x,y)] = []

                if x!=0:
                    graph_dict[(x,y)].append((x-1,y))
                if x!=numSquares-1:
                    graph_dict[(x,y)].append((x+1,y))

                if y!=0:
                    graph_dict[(x,y)].append((x,y-1))
                if y!=numSquares-1:
                    graph_dict[(x,y)].append((x,y+1))

        Graph.__init__(self,graph_dict)
        self.walker_positions = {'a':(4,0),'b':(4,8)}

    def isLegalPlankPlacement(self,position,direction):
        x,y = position
        assert(direction in ["h","v"]), "Direction should be horizontal or vertical"
        assert(x>=0 and x<=8 and y>0 and y<=8), "Position should be on board"

        # if direction not in ["h","v"]:
        #     print("Direction must be h or v")
        #     return False
        # if x<0 or x>8 or y<=0 or y>8:
        #     print("Position not on board for planks")
        #     return False

        if direction=='v':
            isLegal = (self.areAdjacent((x,y),(x,y+1)) or self.areAdjacent((x+1,y),(x+1,y+1))) and (self.areAdjacent((x,y),(x+1,y)) and self.areAdjacent((x,y+1),(x+1,y+1)))
        if direction=='h':
            isLegal = (self.areAdjacent((x,y),(x+1,y)) or self.areAdjacent((x,y+1),(x+1,y+1))) and (self.areAdjacent((x,y),(x,y+1)) and self.areAdjacent((x+1,y),(x+1,y+1)))

        isLegal = isLegal and self.walkerPathExists('a',self.walker_positions['a']) and self.walkerPathExists('b',self.walker_positions['b'])

        return isLegal


    def isLegalMove(self,old_position,new_position):

        if new_position in self.graph[old_position]:
            return True
        else:
            return False


    def walkerPathExists(self,walker,position):
        x,y = position
        connected = False
        x2 = 0
        while not connected and x2<9:
            if walker=="a" and self.arePathConnected(position,(x2,8)):
                return True
            if walker=='b' and self.arePathConnected(position,(x2,0)):
                return True
            x2 += 1
        return False

    def placePlank(self,position,direction):
        x,y = position

        if not self.isLegalPlankPlacement(position,direction):
            print("That move is not valid.")
            raise ValueError

        if direction=='v':
            self.deleteEdge((x,y),(x+1,y))
            self.deleteEdge((x,y+1),(x+1,y+1))
        if direction=='h':
            self.deleteEdge((x,y),(x,y+1))
            self.deleteEdge((x+1,y),(x+1,y+1))

    def show(self,positionA,positionB,orientation='a'):
        print(" --" * 9)
        direction = [i for i in range(9)]

        if orientation=='a':
            direction = direction[::-1]
        else:
            direction = direction

        for j in direction:
            row, col = ["|  "], []
            for i in direction:
                if i<8 and not self.areAdjacent((i,j),(i+1,j)):
                    row.append("*  ")
                else:
                    row.append("|  ")
                if j<8 and not self.areAdjacent((i,j),(i,j+1)):
                    col.append(" **")
                else:
                    col.append(" --")


            if positionA[1]==j:
                if orientation=='a':
                    row[positionA[0]] = "|A"+u'\u2659' if row[positionA[0]][0]=="|" else "*A"+u'\u2659'
                else:
                    row[8-positionA[0]] = "|A"+u'\u2659' if row[8-positionA[0]][0]=="|" else "*A"+u'\u2659'

            if positionB[1]==j:
                if orientation=='a':
                    row[positionB[0]] = "|B"+u'\u265F' if row[positionB[0]][0]=="|" else "*B"+u'\u265F'
                else:
                    row[8-positionB[0]] = "|B"+u'\u265F' if row[8-positionB[0]][0]=="|" else "*B"+u'\u265F'


            print(''.join(row))
            print(''.join(col))



class Game:
    def __init__(self):
        self.board = QuoridorGraph()
        self.positions = {"a":(4,0),"b":(4,8)}
        self.turn = 'start'

    def showBoard(self,orientation='a'):
        self.board.show(self.positions['a'],self.positions['b'],orientation)

    def move(self,piece,new_position=None,direction=None):
        if piece not in ["a","b"]:
            raise ValueError("Piece should be either a or b")

        if piece=="a":
            direction_dict = {"u":(0,1),"d":(0,-1),"l":(-1,0),"r":(1,0)}
        elif piece=="b":
            direction_dict = {"u":(0,-1),"d":(0,1),"l":(1,0),"r":(-1,0)}

        if direction is not None:
            x,y = self.positions[piece]
            dx,dy = direction_dict[direction]
            new_position = (x+dx,y+dy)

        xx = new_position[0]
        yy = new_position[1]

        if xx<0 or xx>8 or yy<0 or yy>8:
            raise ValueError("New position is off board")

        if piece=='a' and new_position==self.positions["b"]:
            raise ValueError("Pieces are overlapping")
        if piece=='b' and new_position==self.positions["a"]:
            raise ValueError("Pieces are overlapping")

        self.positions[piece] = new_position


    def placePlank(self,position,direction):
        self.board.placePlank(position,direction)


    def isNotOver(self):
        if self.positions["a"]==8:
            print("Player 1 wins")
            return False
        elif self.positions["b"]==0:
            print("Player 2 wins")
            return False
        elif self.positions["a"]==8 and self.positions["b"]==0:
            print("Something went wrong")
            return True
        else:
            return True

    def play(self):

        # beginning = 'Beginning the game...'+' q u o r i d o r'
        # timelags = [0.25*random.random() for i in range(len(beginning))]
        # for i in range(len(beginning)):
        #         print(beginning[i],sep=" ",end=" ", flush=True); time.sleep(timelags[i])
        # print(" ")

        player1 = input("Player 1's Name? \n")[:10]
        player2 = input("Player 2's Name? \n")[:15]

        while player2==player1:
            player2 = input("Enter different name Player 2 \n")[:15]

        print("Starting! \n")
        playerdict = {player1:"a",player2:"b"}

        player = player1
        while self.isNotOver():
            print("Player "+player+", it is your turn! \n")


            # Need to FIX THIS!!

            self.showBoard()#orientation=playerdict[player])
            print(self.positions)
            #print("Orientation = ",playerdict[player])
            x = input("Press p to place a plank or m to move piece\n")
            while True:
                if x=='P' or x=='p':
                    try:
                        positionx = int(input("x-position? e.g. 0 \n"))
                        positiony = int(input("y-position? e.g. 0 \n"))
                    except:
                        continue
                    direction = input("Direction? v or h? \n")
                    if direction in ["v","h"] and positionx<9 and positiony<9:
                        try:
                            self.placePlank((int(positionx),int(positiony)),direction)
                            break
                        except ValueError:
                            continue

                elif x=='M' or x=='m':
                    direction = input("Direction? u, d, l, or r? \n")
                    if direction not in ["u","d",'l','r']:
                        continue

                    try:
                        self.move(playerdict[player],new_position=None,direction=direction)
                        print("Moved",playerdict[player])
                    except ValueError:
                        continue

                    break

                else:
                    x = input("Error. Press p to place a plank or m to move piece\n")

            if player==player1:
                player = player2
            else:
                player = player1





qgame = Game()
qgame.play()
#qgame.move("a",direction="u")
#qgame.move("a",direction="l")
#print(qgame.board.graph[(4,4)])

#qgame.showBoard()

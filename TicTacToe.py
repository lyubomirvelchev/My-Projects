class MorskiShah:
    def __init__(self, side=3):
        self.board=[]
        self.turn = 0
        self.game_state = 0
        self.X = "X"
        self.O = "0"
        self.side = side
        self.createEmptyBoard()

    def createEmptyBoard(self):
        for i in range(0,self.side):
            buff=[]
            for j in range(0,self.side):
                buff.append(" ")
            self.board.append(buff)

    def displayHorizontalLine(self):
        str = " "
        for i in range(0,self.side):
            str +="--- "
        print(str)

    def displayRow(self,p):
        str="|"
        for i in range(0,self.side):
            str+= " " + self.board[p][i] +" |"
        print(str)

    def displayBoard(self):
        self.displayHorizontalLine()
        # print("|")
        for i in range(0,self.side):
            self.displayRow(i)
            self.displayHorizontalLine()


    def startGame(self):
        self.displayBoard()
        while self.turn in range(0, self.side * self.side):
            self.userInput()

    def userInput(self):
        while True:
            try:
                first_number = int(input("Choose a row: "))
                second_number = int(input("Choose a column: "))
                break
            except:
                print("That's not a valid option!")
        if first_number < 1 or first_number > self.side or second_number < 1 or second_number > self.side:
            print("Invalid row/column !!! ")
            print("                      ")
            self.userInput()  # recurrsion is overkill
            return
        if self.board[first_number - 1][second_number - 1] != " ":
            print("Space already taken")
            print("                      ")
            self.userInput()
            return
        if self.turn % 2 == 0:
            self.board[first_number - 1][second_number - 1] = self.X
        else:
            self.board[first_number - 1][second_number - 1] = self.O
        self.displayBoard()
        self.checkGame()
        self.turn += 1
        if self.turn == (self.side * self.side) and all([x != " " for x in self.board]):
            print("Tie")
            exit()

    def printWinner(self):
        if self.turn % 2 == 0:
            print("The winner is X !!!")
        else:
            print("The winner is 0 !!!")

    def checkGame(self):
        for i in range(0, self.side):  # no indexation needed
            if self.board[i][0] != " ":
                if all([x == self.board[i][0] for x in self.board[i]]):
                    self.printWinner()
                    exit()
        for j in range(0, self.side):
            if self.board[0][j] != " ":
                b = [self.board[s][j] for s in range(0, self.side)]
                if all([x == b[0] for x in b]):
                    self.printWinner()
                    exit()
        if self.board[0][0] != " ":
            d = [self.board[f][f] for f in range(0, self.side)]
            if all([x == d[0] for x in d]):
                self.printWinner()
                exit()
        if self.board[self.side - 1][0] != " ":
            c = [self.board[(self.side - 1) - counter][0 + counter] for counter in range(0, self.side)]
            if all([x == c[0] for x in c]):
                self.printWinner()
                exit()


igra2 = MorskiShah()

igra2.startGame()

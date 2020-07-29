import random


class Game:
    def __init__(self, n=4):
        self.board = []
        self.row = []
        self.size = n
        self.full_list = []
        for _i in range(0, n * n):  # list ot 0 do (n*n - 1)
            self.full_list.append(_i) # pzp: Use list comprehansion - self.full_list = [x for x in range(0, n * n)]
        self.check_list = []
        for _i in range(0, n * n):  # full_list stava prazen i si pravim copy kato retardi
            self.check_list.append(_i) # pzp: Make copy of list.
        self.zero = (0, 0)
        self.counter = 1
        self.height = n
        self.commands = []
        self.turns = 0
        self.the_mighty_algorithm_used =False

    # Създава почти подреден борд с цел проверка на някои функции
    def create_ordered_board(self):
        counter = 1
        for row in range(0, self.size):
            for elem in range(0, self.size):
                if row == self.size - 1 and elem == self.size - 2:
                    self.row.append(self.full_list[0])
                    self.zero = (row, elem)
                else:
                    self.row.append(self.full_list[counter])
                    counter += 1
            self.board.append(self.row)
            self.row = []

    def create_board(self):  # generate board and random shuffle na vsichki chisla
        for row in range(0, self.size):
            for column in range(0, self.size):
                a = random.choice(self.full_list)
                self.row.append(a)
                if a == 0:
                    self.zero = (row, column)  # zapazvame koordinatite na nulata(praznoto pole)
                self.full_list.pop(self.full_list.index(a))
            self.board.append(self.row)
            self.row = []
        #1 [x for x in range(0, self.size * self.size)] ; random.shuffle(); n X n -> [[0:n], [n+1: 2*n], [2n+1, 3*n]]
        #2 list comprehansion can involve IF statement last element -> 0
        #3* [1 .. n**2 - 1, 0] -> method shuffle board. all boards can be solved!

    def create_beautiful_board(self):  # oformqme hubav bord i go printim vseki pyt
        # for elem in range(0, self.size):
        hor_sep = " -----"*self.size
        print(hor_sep, end="")  # продължаваме на същият ред
            # print(" -----"*self.size, end="")
        print("")  # nov red
        for row in range(0, self.size):
            print("|", end="")
            for column in range(0, self.size):
                if self.board[row][column] < 10:
                    print("  " + str(self.board[row][column]) + "  |", end="")  # krasivo oformlenie za chislata pod 10
                elif self.board[row][column] > 99:
                    print(" " + str(self.board[row][column]) + " |", end="")  # krasivo oformlenie za chislata nad 100
                else:
                    print(" " + str(self.board[row][column]) + "  |", end="")  # krasivo oformlenie za dvucifrenite
            print("")
            print(hor_sep)
        # time.sleep(0.5)

    def swap(self, a, b, c, d):  # swap beibe
        buff = self.board[a][b]  # buff beibe
        self.board[a][b] = self.board[c][d]
        self.board[c][d] = buff

    def left_arrow(self):
        if self.zero[1] == 0:  # ako e v nai lqvata kolona nqma kak da se premesti nalqvo
            print("Invalid move")
        else:
            self.swap(self.zero[0], self.zero[1], self.zero[0], self.zero[1] - 1)
            self.zero = (self.zero[0], self.zero[1] - 1)  # promenqme koordinatite na nulata
            self.create_beautiful_board()  # printim novite promeni на борда
            self.commands.append("left")
            self.turns += 1

    def right_arrow(self):  # аналогично с left_arrow
        if self.zero[1] == self.size - 1:
            print("Invalid move")
        else:
            self.swap(self.zero[0], self.zero[1], self.zero[0], self.zero[1] + 1)
            self.zero = (self.zero[0], self.zero[1] + 1)
            self.create_beautiful_board()
            self.commands.append("right")
            self.turns += 1

    def upper_arrow(self):  # аналогично с left_arrow
        if self.zero[0] == 0:
            print("Invalid move")
        else:
            self.swap(self.zero[0], self.zero[1], self.zero[0] - 1, self.zero[1])
            self.zero = (self.zero[0] - 1, self.zero[1])
            self.create_beautiful_board()
            self.commands.append("up")
            self.turns += 1

    def down_arrow(self):  # аналогично с left_arrow
        if self.zero[0] == self.size - 1:
            print("Invalid move")
        else:
            self.swap(self.zero[0], self.zero[1], self.zero[0] + 1, self.zero[1])
            self.zero = (self.zero[0] + 1, self.zero[1])
            self.create_beautiful_board()
            self.commands.append("down")
            self.turns += 1

    def single_turn(self):  # user избира посоката
        inp = input("Choose a direction: 'right', 'left', 'up', 'down' or press 0 to use THE MIGHTY ALGORITHM: ")
        if inp == "left":
            self.left_arrow()
        elif inp == "right":
            self.right_arrow()
        elif inp == "up":
            self.upper_arrow()
        elif inp == "down":
            self.down_arrow()
        elif inp == "0":
            self.the_mighty_algorithm()
        else:
            print("Invalid direction")  # нема такава посока

    def multiple_turns_from_array(self, arr):  # Взима лист с команди 'right', 'left', 'up' or 'down' и ги изпълнява
        # self.create_ordered_board()
        self.create_board()
        self.create_beautiful_board()
        for elem in arr:  # minavame prez vsichki komandi
            if self.check_board():
                print("Congratulations")
                exit()
            else:  # izpylnqvame vsichki komandi
                if elem == "left":
                    self.left_arrow()
                elif elem == "right":
                    self.right_arrow()
                elif elem == "up":
                    self.upper_arrow()
                elif elem == "down":
                    self.down_arrow()
                else:  # v sluchai na greshna komanda prodyljavame napred
                    continue

    def check_board(self):
        for element in self.check_list:  # проверяваме всеки елемент дали си е на мястото
            if self.search_number(element) != self.find_correct_place_better(element):
                return False
        return True

    def player_game(self):
        self.create_board()
        # self.create_ordered_board() # v sluchai che iskame podredena duska ctr+? tuk i na gorniq red
        self.create_beautiful_board()
        while not self.check_board() and not self.the_mighty_algorithm_used:  # Играем догато не е подреден борда
            self.single_turn()
        if not self.the_mighty_algorithm_used:
            print("Cоngratulations!!! You won after {} turn(s)".format(self.turns))
            print(self.commands)

    def search_number(self, number):  # копи пейст от нета, щот не успях сам да го измисля
        for i, x in enumerate(self.board):
            if number in x:
                return (i, x.index(number))  # nz kak bachka :'(

    def find_correct_x(self, number):
        return int(number / self.size)

    def find_correct_y(self, number):
        return self.size - 1 if number % self.size == 0 else number % self.size - 1

    def find_correct_place(self, number):  # namirame pravilnoto mqsto na number
        if number == 0:  # ako e nula to pravilnto mqsto e poslednoto
            return (self.size - 1, self.size - 1)
        return (self.find_correct_x(number), self.find_correct_y(number))  #

    def find_correct_x_better(self, number):  # long story short - bla bla
        return int(number / self.size) if number % self.size != 0 else int(number / self.size - 1)

    def find_correct_place_better(self, number):
        if number == 0:
            return (self.size - 1, self.size - 1)
        return (self.find_correct_x_better(number), self.find_correct_y(number))

    def move_zero(self, target, number):
        while not self.zero == target:  # mestim nulata do target kato zaobikalqme daden number za da nqma razmestvane
            if self.zero[0] == target[0]:
                self.if_zero_target_same_row(target, number)
            if self.zero[0] > target[0]:
                self.if_zero_below_target(target, number)
            if self.zero[0] < target[0]:
                self.if_zero_above_target(target, number)

    def if_zero_target_same_row(self, target, number):
        if self.zero[1] < target[1]:  # ako zero e otlqvo
            for _i in range(0, target[1] - self.zero[1]):
                if self.zero[0] == number[0] and self.zero[1] == number[1] - 1:
                    self.go_around_number(number)  # ako sledvashto chislo e number go zaobukalqme
                    return
                else:
                    self.right_arrow()  # mestim zero nadqsno
        if self.zero[1] > target[1]:  # ako zero e otdqsno
            for _j in range(0, self.zero[1] - target[1]):
                if self.zero[0] == number[0] and self.zero[1] == number[1] + 1:
                    self.go_around_number(number)  # zaobikalqme
                    return
                else:
                    self.left_arrow()  # mestim zero nalqvo

    def if_zero_below_target(self, target, number):
        for _i in range(0, self.size - 1 - self.zero[1]):
            if self.zero[0] == number[0] and self.zero[1] == number[1] - 1:
                self.go_around_number(number)
                return
            else:
                self.right_arrow()  # nadqsno dokato dokarame nulata v posledna kolona
        for _j in range(0, self.zero[0] - target[0]):
            if self.zero[0] == number[0] + 1 and self.zero[1] == number[1]:
                self.go_around_number(number)
                return
            else:
                self.upper_arrow()  # nagore dokato dokarame nulata do reda na target
        for _k in range(0, self.size - 1 - target[1]):
            if self.zero[0] == number[0] and self.zero[1] == number[1] + 1:
                self.go_around_number(number)
                return
            else:
                self.left_arrow()  # nalqvo dokato stignem target

    def if_zero_above_target(self, target, number):
        for _i in range(0, self.size - 1 - self.zero[1]):
            if self.zero[0] == number[0] and self.zero[1] == number[1] - 1:
                self.go_around_number(number)
                return
            else:
                self.right_arrow()  # nadqsno dokato dokarame nulata v posledna kolona
        for _j in range(0, target[0] - self.zero[0]):
            if self.zero[0] == number[0] - 1 and self.zero[1] == number[1]:
                self.go_around_number(number)
                return
            else:
                self.down_arrow()  # nadolu dokato dokarame nulata do reda na target
        for _k in range(0, self.size - 1 - target[1]):
            if self.zero[0] == number[0] and self.zero[1] == number[1] + 1:
                self.go_around_number(number)
                return
            else:
                self.left_arrow()  # nalqvo dokato stignem target

    def go_around_number_rightside(self, number):  # zaobikalqme chilvo koeto se namira otdqsno na nulata
        if self.zero[0] == number[0] and self.zero[1] == number[1] - 1:  # ako number e otdqsno na nulata
            if number[0] == self.size - self.height and number[1] == self.size - 1:  # ako number e v goren desen ygyl
                self.down_arrow()  # self.height zapochva ot n i se namalqvo s edno sled vseki podreden red
                self.right_arrow()
            elif number[0] == self.size - 1:  # ako number e na posleden red
                if number[1] != self.size - 1:  # ako number ne e v kornera
                    self.upper_arrow()
                    self.right_arrow()
                    self.right_arrow()
                    self.down_arrow()
                else:  # ako number e v dolen desen korner
                    self.upper_arrow()
                    self.right_arrow()
            elif number[1] == self.size - 1 and number[0] != (
                    self.size - self.height or self.size - 1):  # ako number e v dqsnata kolona i ne e korner
                self.upper_arrow()
                self.right_arrow()
            else:  # v obshtiqt sluchai ili ako number e na pyrvi red
                self.down_arrow()
                self.right_arrow()
                self.right_arrow()
                self.upper_arrow()

    def go_around_number_leftside(self, number):  # analogochno tuk i za ostanalite 2 funkcii
        if self.zero[0] == number[0] and self.zero[1] == number[1] + 1:  # ako number e otlqvo na nulata
            if number[0] == self.size - self.height and number[1] == 0:  # ako number e v goren lqv ygyl
                self.down_arrow()
                self.left_arrow()
            elif number[0] == self.size - 1:  # ako number e na posleden red
                if number[1] != self.size - 1:  # ako number ne e v kornera
                    self.upper_arrow()
                    self.left_arrow()
                    self.left_arrow()
                    self.down_arrow()
                else:  # ako number e v dolen lqv korner
                    self.upper_arrow()
                    self.left_arrow()
            elif number[1] == 0 and number[0] != (
                    self.size - self.height or self.size - 1):  # ako number e v lqvata kolona i ne e korner
                self.upper_arrow()
                self.left_arrow()
            else:  # v obshtiqt sluchai ili ako number e na pyrvi red
                self.down_arrow()
                self.left_arrow()
                self.left_arrow()
                self.upper_arrow()

    def go_around_number_above(self, number):
        if self.zero[0] == number[0] + 1 and self.zero[1] == number[1]:  # ako number e otgore na nulata
            if number[1] == 0 and number[0] == self.size - self.height:  # ako number e v goren lqv ygyl
                self.right_arrow()
                self.upper_arrow()
            elif number[1] == self.size - 1:  # ako number e na posledna kolona
                if number[0] != self.size - self.height:  # ako number ne e v kornera
                    self.left_arrow()
                    self.upper_arrow()
                    self.upper_arrow()
                    self.right_arrow()
                else:  # ako number e v goren desen korner
                    self.left_arrow()
                    self.upper_arrow()
            elif number[0] == self.size - self.height and number[1] != (
                    0 or self.size - 1):  # ako number e v 1vi red in ne e korner
                self.left_arrow()
                self.upper_arrow()
            else:  # v obshtiqt sluchai ili ako number e na pyrva kolona
                self.right_arrow()
                self.upper_arrow()
                self.upper_arrow()
                self.left_arrow()

    def go_around_number_below(self, number):
        if self.zero[0] == number[0] - 1 and self.zero[1] == number[1]:  # ako number e pod nulata
            if number[1] == 0 and number[0] == self.size - 1:  # ako number e v dolen lqv ygyl
                self.right_arrow()
                self.down_arrow()
            elif number[1] == self.size - 1:  # ako number e na posledna kolona
                if number[0] != self.size - 1:  # ako number ne e v kornera
                    self.left_arrow()
                    self.down_arrow()
                    self.down_arrow()
                    self.right_arrow()
                else:  # ako number e v dolen desen korner
                    self.left_arrow()
                    self.down_arrow()
            elif number[0] == self.size - 1 and number[1] != (
                    0 or self.size - 1):  # ako number e v posleden red in ne e korner
                self.right_arrow()
                self.down_arrow()
            else:  # v obshtiqt sluchai ili ako number e na pyrva kolona
                self.right_arrow()
                self.down_arrow()
                self.down_arrow()
                self.left_arrow()

    def go_around_number(self, number):
        if self.zero[0] == number[0] and self.zero[1] == number[1] - 1:  # ako number e otdqsno na nulata
            self.go_around_number_rightside(number)
            return
        if self.zero[0] == number[0] and self.zero[1] == number[1] + 1:  # ako number e otlqvo na nulata
            self.go_around_number_leftside(number)
            return
        if self.zero[0] == number[0] - 1 and self.zero[1] == number[1]:  # ako number e pod nulata
            self.go_around_number_below(number)
            return
        if self.zero[0] == number[0] + 1 and self.zero[1] == number[1]:  # ako number e nad nulata
            self.go_around_number_above(number)
            return

    def place_single_row(self):  # podrejdame ot pyrvi red do n-2 ri red
        while self.counter % self.size != self.size - 1:  # dokato ne podredim vsichki elementi bez poslednite dva
            while self.search_number(self.counter) != self.find_correct_place(self.counter):
                b = self.search_number(self.counter)
                if b[0] == self.find_correct_place(self.counter)[0]:  # ako e na syshtiqt red
                    self.move_zero((b[0], b[1] - 1), b)  # mestim nulata otlqvo na b bez da mestim b
                    self.right_arrow()  # posle razmenqme b i nulata
                if b[0] != self.find_correct_place(self.counter)[0] and b[1] >= self.find_correct_place(self.counter)[
                    1]:
                    self.move_zero((b[0] - 1, b[1]), b)  # mestim b nagore dokato go dokarame do pravilniqt red
                    self.down_arrow()
                if b[0] != self.find_correct_place(self.counter)[0] and b[1] < self.find_correct_place(self.counter)[1]:
                    self.move_zero((b[0], b[1] + 1), b)
                    self.left_arrow()  # mestim b nalqvo do tyrsenata kolona predi da go mestim nagore za da nqma fal
            self.counter += 1  # povtarqmeza sledvashtoto chislo
        while self.search_number(self.counter + 1) != self.find_correct_place(self.counter):
            c = self.search_number(self.counter + 1)  # tuk dokarvame posledniqt element ot reda na predposledno mqsto
            if c[0] == self.find_correct_place(self.counter)[0]:
                self.move_zero((c[0], c[1] - 1), c)
                self.right_arrow()  # ako e na syshtiqt red znachi ena posledno mqsto i samo mestim edno mesto nalqvo
            if c[0] != self.find_correct_place(self.counter)[0]:
                while c[1] != self.size - 1:  # dokarvame c do posledna kolona
                    self.move_zero((c[0], c[1] + 1), c)
                    self.left_arrow()
                    c = self.search_number(self.counter + 1)
                while c[0] != self.find_correct_place(self.counter)[0]:  # dokarvame c do pyrvi red
                    self.move_zero((c[0] - 1, c[1]), c)
                    self.down_arrow()
                    c = self.search_number(self.counter + 1)
        self.counter += 1  # sledvashtoto chislo
        while self.search_number(self.counter - 1) != self.find_correct_place(self.counter - 1 + self.size):
            d = self.search_number(self.counter - 1)  # dokarvame predposledniqt element pod posledniqt element
            print("")
            print("")
            print("")
            print("SMQTAYYY")
            print("")
            print("")
            print("")
            if d[0] == self.find_correct_place(self.counter - 1 + self.size)[0] and d[1] != self.size - 1:
                self.move_zero((d[0], d[1] + 1), d)
                self.left_arrow()
                print("")
                print("")
                print("")
                print("hui1")
                print("")
                print("")
                print("")
            elif d[0] == self.find_correct_place(self.counter - 1 + self.size)[0] and d[1] == self.size - 1:
                self.left_arrow()
                self.down_arrow()
                self.right_arrow()
                self.down_arrow()
                self.left_arrow()
                self.upper_arrow()
                self.right_arrow()
                self.upper_arrow()
                self.left_arrow()
                self.down_arrow()
                self.right_arrow()
                self.upper_arrow()
                self.left_arrow()
                self.down_arrow()
                self.down_arrow()
                self.right_arrow()
                self.upper_arrow()
                self.upper_arrow()  # chasten sluchai ako elementa e na dolniqt red posledna kolona
                print("")
                print("")
                print("")
                print("hui2")
                print("")
                print("")
                print("")
            elif d[0] == self.find_correct_place(self.counter - 1 + self.size)[0] + 1 and d[1] == self.size - 1:
                self.down_arrow()
                self.left_arrow()
                self.down_arrow()
                self.right_arrow()
                self.upper_arrow()
                self.left_arrow()
                self.down_arrow()
                self.right_arrow()
                self.upper_arrow()
                self.upper_arrow()  # drug chasten sluchai
                print("")
                print("")
                print("")
                print("")
                print("hui3")
                print("")
                print("")
                print("")
            else:  # vsichki ostanali sluchai
                while d[1] != self.size - 2:  # tr dokarame elementa do predposledna kolona
                    if d[1] == self.size - 1:  # ako e v posledna kolona
                        self.move_zero((d[0], d[1] - 1), d)
                        self.right_arrow()
                        print("")
                        print("")
                        print("")
                        print("hui4")
                        print("")
                        print("")
                        print("")
                    else:  # ako ne e
                        self.move_zero((d[0], d[1] + 1), d)
                        self.left_arrow()
                        print("")
                        print("")
                        print("")
                        print("hui5")
                        print("")
                        print("")
                        print("")
                    d = self.search_number(self.counter - 1)
                while d[0] != self.find_correct_place(self.counter - 1 + self.size)[0]:  #
                    self.move_zero((d[0] - 1, d[1]), d)
                    self.down_arrow()
                    d = self.search_number(self.counter - 1)
                    print("")
                    print("")
                    print("")
                    print("hui6")
                    print("")
                    print("")
                    print("")
        self.move_zero((self.find_correct_place_better(self.counter)), (self.find_correct_place(self.counter - 1 +self.size)))
        """"Veche ca podredeni taka:  [1,2,......,self.size,neshto si],[neshto si,.......,self.size - 1,0]"""
        # self.upper_arrow()
        self.left_arrow()
        self.down_arrow()
        self.counter += 1
        """"Veche dadeniqt red e podreden"""

    def place_last_two_rows(self):  # podrejdame poslednite dva reda bezposlednoto 2 x 2 kvadretche
        while self.search_number(self.counter + self.size) != self.find_correct_place(self.counter):
            a = self.search_number(self.counter + self.size)
            if a[0] == self.find_correct_place(self.counter)[0]:
                self.move_zero((a[0], a[1] - 1), a)
                self.right_arrow()
            else:
                self.move_zero((a[0] - 1, a[1]), a)
                self.down_arrow()
        self.counter += 1
        while self.search_number(self.counter - 1) != self.find_correct_place(self.counter):
            b = self.search_number(self.counter - 1)
            if b[0] == self.find_correct_place(self.counter)[0]:
                self.move_zero((b[0], b[1] - 1), b)
                self.right_arrow()
            elif b == self.find_correct_place(self.counter - 1 + self.size):
                self.down_arrow()
                self.left_arrow()
                self.upper_arrow()
                self.right_arrow()
                self.right_arrow()
                self.down_arrow()
                self.left_arrow()
                self.left_arrow()
                self.upper_arrow()
                self.right_arrow()
                self.down_arrow()
                self.left_arrow()
                self.upper_arrow()
                self.right_arrow()
                self.right_arrow()
                self.down_arrow()
                self.left_arrow()
                self.upper_arrow()
                self.right_arrow()  # chasten sluchai
            else:
                self.move_zero((b[0] - 1, b[1]), b)
                self.down_arrow()
        self.move_zero((self.find_correct_place(self.counter - 1 + self.size)), self.find_correct_place((self.counter)))
        self.upper_arrow()
        self.right_arrow()

    """"Myrzi me da obqsnqvam kak gi podrejdam"""

    # its magic

    def check_last_two_rows(self): #ponqkoga ne gi podrejda pravilno zatowa proverka i ako sa nepravilno podredeni
        # gi odrejda pak dokato ne se podredqt kato horata
        check_numbers = []
        for _number in range(0, self.size - 2):
            check_numbers.append(self.counter - 1)
            check_numbers.append(self.counter - 1+ self.size)
            self.counter -= 1
        print(check_numbers)
        for element in check_numbers:
            if self.search_number(element) != self.find_correct_place(element):
                self.counter = self.size*(self.size - 2) + 1
                for _anothernumber in range(0, self.size - 2):
                    self.place_last_two_rows()
                self.check_last_two_rows()

    def move_last_three_elements(self):  # mestim nai malkiqt ot trite element na mqstoto mu
        s = self.search_number(self.counter)
        if s[0] == self.find_correct_place(self.counter)[0]:  # ako e na pravilni red
            self.right_arrow()
            self.down_arrow()
            self.solvable_or_unsolvable()  # proverka dali e solvable
        else:  # ako ne e na pravilniqt red
            if s[1] == self.size - 1:  # ako e dolu vdqsno
                self.right_arrow()
                self.down_arrow()
                self.left_arrow()
                self.upper_arrow()
                self.right_arrow()
                self.down_arrow()
                self.solvable_or_unsolvable()
            else:  # ako ne e
                self.down_arrow()
                self.right_arrow()
                self.solvable_or_unsolvable()

    def solvable_or_unsolvable(self):
        if self.search_number(self.counter + self.size) == self.find_correct_place(self.counter + self.size):
            print("The puzzle is solved in {} turn(s)".format(self.turns))  # ako posledniqt element e na mqstoto sinachi e solved
        else:
            print("The puzzle is unsolvable. This useless riddle took us {} turn(s)".format(self.turns))

    def the_mighty_algorithm(self):  # the name speaks for itself
        for _number in range(0, self.size - 2):  # podrejdame pyrvite n - 2 reda
            self.place_single_row()
            print("bash hui")
            self.height -= 1  # visochinata pada s edno za da ne hodi nulata tam kydeto ne i e rabota
        for _anothernumber in range(0, self.size - 2):
            self.place_last_two_rows()  # podrejdame poslednite dva reda bez 2 x 2 kvadrata
        self.check_last_two_rows()
        self.counter = self.size*self.size - self.size - 1
        self.move_last_three_elements()
        print("All used commands:")
        print(self.commands)
        self.the_mighty_algorithm_used = True



c = Game()
c.player_game()
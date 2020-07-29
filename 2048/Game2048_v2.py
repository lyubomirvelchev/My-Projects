import random


class GameClass:
    does_print = True

    def __init__(self, *args, size=4, **kwargs):
        self.size = size
        self.board = []
        self.empty_field_coord = []
        self.direction = 0
        """Create new game and spawn random number."""
        self.create_board()
        self.spawn_new_number()

        super(GameClass, self).__init__(*args, **kwargs)

    def create_board(self):  # fill board with zeros
        self.board = [[0 for _ in range(0, self.size)] for _ in range(0, self.size)]

    def print_pretty_board(self):
        if not self.does_print:
            return
        hor_sep = " -----" * self.size
        print(hor_sep, end="")  # same line
        print("")  # new line
        for row in range(0, self.size):
            print("|", end="")
            for column in range(0, self.size):
                if self.board[row][column] < 10:
                    print("  " + str(self.board[row][column]) + "  |", end="")  # beautify 1 digit numbers
                elif self.board[row][column] > 99 and self.board[row][column] < 1000:
                    print(" " + str(self.board[row][column]) + " |", end="")  # beautify 3 digit numbers
                elif self.board[row][column] > 999:
                    print(" " + str(self.board[row][column]) + "|", end="")  # beautify 4 digit numbers
                else:
                    print(" " + str(self.board[row][column]) + "  |", end="")  # beautify 2 digit numbers
            print("")
            print(hor_sep)

    def spawn_new_number(self):
        self.refresh_empty_fields()
        number = random.choice(self.empty_field_coord)  # choose a zero
        self.board[number[0]][number[1]] = self.add_two_or_four()  # and replace it with 2 or 4
        self.print_pretty_board()

    def refresh_empty_fields(self):  # find coordinates of all zeros on the board
        self.empty_field_coord = []
        for row in range(0, self.size):
            for column in range(0, self.size):
                if self.board[row][column] == 0:
                    self.empty_field_coord.append((row, column))

    def add_two_or_four(self):
        return random.choices(
            population=[2, 4],
            weights=[0.8, 0.2]  # 80% chance to return 2 and 20% to return 4
        )[0]

    def all_same_1d(self, list): # return True if list has no zeros
        return all(x != 0 for x in list)

    def game_over(self):
        if all(self.all_same_1d(element) for element in self.board): # if board has no zeros
            for row in self.board:
                if self.check_if_summable(row):
                    return True
            for column in range(0, self.size):
                new_column = [item[column] for item in self.board]
                if self.check_if_summable(new_column):
                    return True
            return False # if no zeros and no same elements next to eachother
        return True

    def sort_list(self, list): # applies a single turn to a single row/column
        # moved_list = [0]*self.size # [0,0,0,0]
        # point_index = 0
        # for elem in inp_list:
        #     if elem !=0:
        #         moved_list[point_index] = elem
        #         point_index +=1      
        moved_elements = self.move_elements(list)
        summed_elements = self.sum_elements(moved_elements)
        return self.move_elements(summed_elements) # after elements get summed they need to be moved again

    def move_elements(self, list):   # pp: use predefined list and insert
        sorted_list = self.append_non_zero_values(list)
        for _ in range(len(sorted_list), self.size):
            sorted_list.append(0) # append zeros behind the non zero values
        return sorted_list

    def append_non_zero_values(self, list):  # pp: Don't use _ for iterator variables if they are actually in usage.
        non_zero_values = []
        for _ in range(0, len(list)):
            if list[_] != 0:
                non_zero_values.append(list[_])
        return non_zero_values

    def sum_elements(self, list):  # pp: Don't use _ for iterator variables if they are actually in usage.
        for _ in range(0, self.size - 1):
            if list[_] != 0 and list[_] == list[_ + 1]: # if two same elements are next to eachother
                list[_] = list[_] * 2   # double the first element
                list[_ + 1] = 0 # nulify the second
        return list

    def move_sideways(self, direction):
        row_number = 0
        for row in self.board:
            row_buff = row[:] # buffer row cuz otherwise the change will change the whole board
            if direction == "d":
                row_buff.reverse() # reverse for direction "right"
            sorted_row = self.sort_list(row_buff)  # move elements and sum the row
            if direction == "d":
                for column in range(0, self.size):
                    self.board[row_number][self.size - 1 - column] = sorted_row[column] # apply changes to board
            else:
                for column in range(0, self.size):
                    self.board[row_number][column] = sorted_row[column] # apply changes to board
            row_number += 1
        self.spawn_new_number() # spawn new number and print the board

    def move_vertically(self, direction): # same as above funtion
        for column in range(0, self.size):
            new_column = [item[column] for item in self.board]
            if direction == "s":
                new_column.reverse()
            sorted_column = self.sort_list(new_column)
            if direction == "s":
                for row in range(0, self.size):
                    self.board[self.size - 1 - row][column] = sorted_column[row]
            else:
                for row in range(0, self.size):
                    self.board[row][column] = sorted_column[row]
        self.spawn_new_number()

    def check_if_summable(self, list): # check if two same elements exist next to eachother
        for _ in range(0, len(list) - 1):
            if list[_] != 0 and list[_] == list[_ + 1]:
                return True
        else:
            return False

    def check_list_state(self, list): # check if all elements are on the right and all zeros on the left
        zero_exist = False
        for element in list:
            if element == 0:
                zero_exist = True
            else:
                if zero_exist: # check is there is a element != 0 that is behind the zero
                    return True
        return False

    def valid_move_direction(self, list):
        if self.check_list_state(list):
            return True
        if self.check_if_summable(list):
            return True

    def check_possible_move_horizontally(self, direction):
        for row in self.board: # goes through all rows to see if at least one can apply the direction
            row_buff = row[:]
            if direction == "d": # takes the row backwards
                row_buff.reverse()
            if self.valid_move_direction(row_buff):
                return True
        return False

    def check_possible_move_vertically(self, direction): #identical to the function above
        for column in range(0, self.size):
            new_column = [item[column] for item in self.board]
            if direction == "s":
                new_column.reverse()
            if self.valid_move_direction(new_column):
                return True
        return False

    def execute_turn_if_possible(self, direction):
        if direction == "a" or direction == "d":
            if self.check_possible_move_horizontally(direction):
                self.move_sideways(direction)
            else:
                print("Move not possible")
        else:
            if self.check_possible_move_vertically(direction):
                self.move_vertically(direction)
            else:
                print("Move not possible")

    def single_turn(self):
        direction = input("Choose direction: ")
        if direction == "a" or direction == "w" or direction == "s" or direction == "d":
            self.execute_turn_if_possible(direction)
        else:
            print("Invalid direction!")

    def play_game(self):

        while self.game_over():
            self.single_turn()
        print("Game over") #gg


if __name__ == "__main__":
    a = GameClass(4)
    a.play_game()

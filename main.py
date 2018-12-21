# -*- coding: utf-8 -*-
import random
from collections import defaultdict


class Cell:

    def __init__(self, cell_id: str, row: int, column: int, view: str, value: int, state: bool, mine: bool,
                 flag: bool) -> None:
        """
        Constructor

        :param cell_id: (str)
        :param row: (int)
        :param column: (int)
        :param view: (str)
        :param value: (int)
        :param state: (bool)
        :param mine: (bool)
        :param flag: (bool)
        """
        self.cell_id = cell_id
        self.row = row
        self.col = column
        self.view = view
        self.value = value
        self.state = state
        self.mine = mine
        self.flag = flag


class Game:

    def __init__(self, rows: int, columns: int, mines_count: int) -> None:
        """
        Constructor

        :param rows: (int)
        :param columns: (int)
        :param mines_count: (int)
        """
        self.rows = rows
        self.columns = columns
        self.mines_count = mines_count
        self.flags_count = mines_count
        self.cells_list = self.generate_cells()
        self.mines_list = []

    def generate_cells(self) -> defaultdict:
        """
        Generation of all cells in the field

        :return: (defaultdict(list))
        """
        data = defaultdict(list)
        for row in range(self.rows):
            for col in range(self.columns):
                data[row].append(Cell('r' + str(row) + 'c' + str(col), row, col, '■ ', 0, False, False, False))
        return data

    def generate_mines(self, row: int, column: int) -> bool:
        """
        Random generation of all mines in the field

        :param row: (int)
        :param column: (int)
        :return: (bool)
        """
        while True:
            rand_cell = random.choice(random.choice(self.cells_list))
            if rand_cell.row < row - 1 or rand_cell.row > row + 1 or rand_cell.col < column - 1 or rand_cell.col > column + 1:
                if rand_cell not in self.mines_list and len(self.mines_list) <= self.mines_count:
                    self.mines_list.append(rand_cell)
                    rand_cell.value = 0
                    rand_cell.mine = True
                if len(self.mines_list) == self.mines_count:
                    return True

    def incrmt_cell_value(self, row: int, col: int) -> bool:
        """
        Increase the value of the cell if the mine is near

        :param row: (int)
        :param col: (int)
        :return: (bool)
        """
        if self.cells_list[row][col].mine == False:
            self.cells_list[row][col].value += 1
            return True
        return False

    def generate_cells_values(self) -> None:
        """
        Increase the value of all cells if the mine is near

        :return: (None)
        """

        for cell in self.mines_list:
            # the top cells check:
            if cell.row - 1 >= 0 and cell.col - 1 >= 0:
                self.incrmt_cell_value(cell.row - 1, cell.col - 1)

            if cell.row - 1 >= 0:
                self.incrmt_cell_value(cell.row - 1, cell.col)

            if cell.row - 1 >= 0 and cell.col + 1 < self.columns:
                self.incrmt_cell_value(cell.row - 1, cell.col + 1)

            # the same line cells check:
            if cell.col - 1 >= 0:
                self.incrmt_cell_value(cell.row, cell.col - 1)
            if cell.col + 1 < self.columns:
                self.incrmt_cell_value(cell.row, cell.col + 1)

            # the bottom cells check:
            if cell.row + 1 < self.rows and cell.col - 1 >= 0:
                self.incrmt_cell_value(cell.row + 1, cell.col - 1)

            if cell.row + 1 < self.rows:
                self.incrmt_cell_value(cell.row + 1, cell.col)

            if cell.row + 1 < self.rows and cell.col + 1 < self.columns:
                self.incrmt_cell_value(cell.row + 1, cell.col + 1)

    def create_check_range_horiz_cells_cond(self, column: int) -> bool:
        """
        Condition creation when the position isn`t out of range

        :param column: (int)
        :return: (bool)

        ■ ■ ■
        V C V
        ■ ■ ■
        Verification adjacent cells (V) against current (C) iterable cell.
        """
        return column - 1 >= 0 and column + 1 < self.columns

    def create_check_range_vert_cells_cond(self, row: int) -> bool:
        """
        Condition creation when the position isn`t out of range

        :param row: (int)
        :return: (bool)

        ■ V ■
        ■ C ■
        ■ V ■
        Verification adjacent cells (V) against current (C) iterable cell.
        """
        return row - 1 >= 0 and row + 1 < self.rows

    def create_check_range_cross_top_cells_cond(self, row: int, col: int) -> bool:
        """
        Condition creation when the position isn`t out of range

        :param row: (int)
        :param col: (int)
        :return: (bool)

        V ■ V
        ■ C ■
        ■ ■ ■
        Verification adjacent cells (V) against current (C) iterable cell.
        """
        return row - 1 >= 0 and col - 1 >= 0 and col + 1 < self.columns

    def create_check_range_cross_bottom_cells_cond(self, row: int, col: int) -> bool:
        """
        Condition creation when the position isn`t out of range

        :param row: (int)
        :param col: (int)
        :return: (bool)

        ■ ■ ■
        ■ C ■
        V ■ V
        Verification adjacent cells (V) against current (C) iterable cell.
        """
        return row + 1 < self.rows and col - 1 >= 0 and col + 1 < self.columns

    def create_open_empty_cells_cond(self, row: int, col: int) -> bool:
        """
        Condition creation when the cell could be opened

        :param row: (int)
        :param col: (int)
        :return: (bool)
        """
        return self.cells_list[row][col].flag == False and \
               self.cells_list[row][col].mine == False and \
               self.cells_list[row][col].value == 0 and \
               self.cells_list[row][col].state == False

    def open_empty_cells(self, row: int, column: int) -> None:
        """
        Opening empty cells

        :param row: (int)
        :param column: (int)
        :return: (None)
        """

        self.cells_list[row][column].state = True
        self.cells_list[row][column].view = '· '

        if self.create_check_range_horiz_cells_cond(column):

            if self.create_open_empty_cells_cond(row, column - 1):
                self.open_empty_cells(row, column - 1)
            if self.create_open_empty_cells_cond(row, column + 1):
                self.open_empty_cells(row, column + 1)

        if self.create_check_range_vert_cells_cond(row):

            if self.create_open_empty_cells_cond(row - 1, column):
                self.open_empty_cells(row - 1, column)
            if self.create_open_empty_cells_cond(row + 1, column):
                self.open_empty_cells(row + 1, column)

        if self.create_check_range_cross_top_cells_cond(row, column):

            if self.create_open_empty_cells_cond(row - 1, column - 1):
                self.open_empty_cells(row - 1, column - 1)
            if self.create_open_empty_cells_cond(row - 1, column + 1):
                self.open_empty_cells(row - 1, column + 1)

        if self.create_check_range_cross_bottom_cells_cond(row, column):

            if self.create_open_empty_cells_cond(row + 1, column - 1):
                self.open_empty_cells(row + 1, column - 1)
            if self.create_open_empty_cells_cond(row + 1, column + 1):
                self.open_empty_cells(row + 1, column + 1)

    def create_open_value_border_cells_cond(self, row: int, col: int) -> bool:
        """
        Condition creation when the value of cells that border with mines could be opened

        :param row: (int)
        :param col: (int)
        :return: (bool)
        """
        return self.cells_list[row][col].value == 0 and \
               self.cells_list[row][col].state == True and \
               self.cells_list[row][col].mine == False

    def open_value_border_cell(self, row: int, col: int) -> None:
        """
        Opening the value of cell that border with mines

        :param row: (int)
        :param col: (int)
        :return: (None)
        """
        self.cells_list[row][col].state = True
        self.cells_list[row][col].view = str(self.cells_list[row][col].value) + ' '

    def open_value_border_cells(self) -> None:
        """
        Opening the value of all cells that border with mines

        :return: (None)
        """

        for row in range(self.rows):
            for col in range(self.columns):

                # boolean condition variables:
                cond_if_cell_isnt_opnd = self.cells_list[row][col].value > 0 and \
                                         self.cells_list[row][col].state == False

                if self.create_check_range_horiz_cells_cond(col):

                    if cond_if_cell_isnt_opnd and \
                            (
                                    self.create_open_value_border_cells_cond(row, col - 1)
                                    or
                                    self.create_open_value_border_cells_cond(row, col + 1)
                            ):
                        self.open_value_border_cell(row, col)

                if self.create_check_range_vert_cells_cond(row):

                    if cond_if_cell_isnt_opnd and \
                            (
                                    self.create_open_value_border_cells_cond(row - 1, col)
                                    or
                                    self.create_open_value_border_cells_cond(row + 1, col)
                            ):
                        self.open_value_border_cell(row, col)

                if self.create_check_range_cross_top_cells_cond(row, col):

                    if cond_if_cell_isnt_opnd and \
                            (
                                    self.create_open_value_border_cells_cond(row - 1, col - 1)
                                    or
                                    self.create_open_value_border_cells_cond(row - 1, col + 1)
                            ):
                        self.open_value_border_cell(row, col)

                if self.create_check_range_cross_bottom_cells_cond(row, col):

                    if cond_if_cell_isnt_opnd and \
                            (
                                    self.create_open_value_border_cells_cond(row + 1, col - 1)
                                    or
                                    self.create_open_value_border_cells_cond(row + 1, col + 1)
                            ):
                        self.open_value_border_cell(row, col)

    def set_unset_flag(self, row: int, col: int) -> bool:
        """
        Setting and unsetting flags in the field

        :param row: (int)
        :param col: (int)
        :return: (bool)
        """
        cell = self.cells_list[row][col]
        if cell.state == False:
            if cell.flag:
                cell.flag = False
                cell.view = '■ '
                self.flags_count += 1
                return False
            else:
                if self.flags_count > 0:
                    cell.flag = True
                    cell.view = '# '

                    self.flags_count -= 1
                return True

    def open_cell(self, row: int, col: int) -> bool:
        """
        Opening the cell by position

        :param row: (int)
        :param col: (int)
        :return: (bool)
        """
        self.cells_list[row][col].state = True

        if self.cells_list[row][col].mine == True:
            print("*" * 30)
            print("You opened the mine! Game over!")
            print("*" * 30)
            for mine in self.mines_list:
                mine.view = '@ '
                mine.state = True
            return False

        else:
            if self.cells_list[row][col].value > 0:
                self.cells_list[row][col].view = str(self.cells_list[row][col].value) + ' '
            else:
                self.open_empty_cells(row, col)
                self.open_value_border_cells()
            return True

    def draw_game_field(self) -> None:
        """
        Drawing game field

        :return: (None)
        """
        print(end="  ")
        for col in range(self.columns):
            if col < 10 and col % 2 == 0:
                print(col, end="   ")
            elif col >= 10 and col % 2 == 0:
                print(col, end="  ")
        print("> > > X pos")

        for row in self.cells_list:
            if row < 10 and row % 2 == 0:
                print(row, end=" ")
            elif row >= 10 and row % 2 == 0:
                print(row, end="")
            else:
                print(end="  ")
            for cell in self.cells_list[row]:
                if cell.state == True and cell.value > 0:
                    print(str(cell.view), end="")
                elif cell.state == True and cell.value == 0:
                    print(str(cell.view), end="")
                else:
                    print(str(cell.view), end="")
            print()
        print("v")
        print("v")
        print("v Y pos\n")

    def check_game_win_status(self) -> bool:
        """
        Checks the game for win or lose

        :return: (bool)
        """
        if self.flags_count == 0:
            for mine in self.mines_list:
                if mine.state == False and mine.flag == True:
                    continue
                else:
                    return True
            print("*" * 30)
            print("Congratulations! You won!")
            print("*" * 30)
            return False
        else:
            return True


class UserInterface:

    def start_game(self) -> None:
        """
        Starts the game

        :return: (None)
        """

        step = 1
        game_isnt_over_flag = True

        while game_isnt_over_flag:
            if step == 1:
                print("*" * 30)
                print("Welcome to 'MINESWEEPER' game")
                print("*" * 30)
                row = int(input("Input height of game field: "))
                col = int(input("Input width of game field: "))
                mines_count = int(input("Input count of mines: "))
                game = Game(row, col, mines_count)
                print("*" * 30)
                game.draw_game_field()
                print("*" * 30)
                print("Select cell position. Step-{}".format(step))
                col = int(input("Input X position: "))
                row = int(input("Input Y position: "))
                print("*" * 30)
                game.generate_mines(row, col)
                game.generate_cells_values()
                game.open_empty_cells(row, col)
                game.open_value_border_cells()
                game.draw_game_field()
                step += 1
            else:
                print("*" * 30)
                print("Game data:")
                print("Mines(@) count: {}".format(game.mines_count))
                print("Flags(#) count: {}".format(game.flags_count))
                print("*" * 30)
                print("Select action with cell:")
                print("Open cell :        input 'c'")
                print("Set & unset flag : input 'f'")
                print("Quit game :        input 'q'")
                print("*" * 30)
                char = input("Input please: ")

                if char == 'c':
                    game.draw_game_field()
                    print("*" * 30)
                    print("Select cell position. Step-{}".format(step))
                    col = int(input("Input X position: "))
                    row = int(input("Input Y position: "))
                    print("*" * 30)
                    game_isnt_over_flag = game.open_cell(row, col)
                    game.draw_game_field()
                    step += 1
                if char == 'f':
                    game.draw_game_field()
                    print("*" * 30)
                    print("Select flag position. Step-{}".format(step))
                    col = int(input("Input X position: "))
                    row = int(input("Input Y position: "))
                    print("*" * 30)
                    game.set_unset_flag(row, col)
                    game_isnt_over_flag = game.check_game_win_status()
                    game.draw_game_field()
                    step += 1
                if char == 'q':
                    break


def main():
    ui = UserInterface()
    ui.start_game()


if __name__ == "__main__":
    main()

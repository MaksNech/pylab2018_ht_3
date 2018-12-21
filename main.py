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


class Cell:
    next_cell_0 = None
    next_cell_0_cost = None
    next_cell_1 = None
    next_cell_1_cost = None
    previous_cell = None
    x = None
    y = None

    def __init__(self, code, bit_length):
        self.code = code
        self.bit_length = bit_length

    def __str__(self):
        return 'C: {}, NC: {} {} C:{} {}'.format(
            bin(self.code),
            bin(self.next_cell_0.code) if self.next_cell_0 else None,
            bin(self.next_cell_1.code) if self.next_cell_1 else None,
            bin(self.next_cell_0_cost) if self.next_cell_0 else None,
            bin(self.next_cell_1_cost) if self.next_cell_1 else None,
        )

    def __repr__(self):
        return '{:0{}b}'.format(
            self.code, self.bit_length,
            # self.addr()
        )

    def shift_0(self, functions):
        return get_cost( self.code, functions)

    def shift_1(self, functions):
        return get_cost(((2 ** self.bit_length) | self.code), functions)

    def create_next_cells(self, functions):
        self.next_cell_0 = Cell(self.code >> 1, self.bit_length)
        self.next_cell_0_cost = self.shift_0(functions)
        self.next_cell_1 = Cell((2 ** (self.bit_length - 1)) | (self.code >> 1), self.bit_length)
        self.next_cell_1_cost = self.shift_1(functions)

    def addr(self):
        return hex(id(self))

def get_cost(code, functions):
    number = 0
    for function in functions:
        number = number << 1
        number += odd_or_even(code & int(function, 2))
    return number


def odd_or_even(number):
    return bin(number).count('1') % 2
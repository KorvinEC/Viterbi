from Cell import Cell
import matplotlib.pyplot as plt


class Graph:

    def __init__(self, steps, functions):
        self.steps = steps
        self.function_bit_length = len(functions[0][2:])
        self.functions = functions
        self.graph = self.create_table()
        self.fig, self.ax = plt.subplots()

    def create_table(self):
        cell = Cell(0, self.function_bit_length - 1)
        result = []
        for step in range(self.steps):
            if step == 0:
                result.append([cell])
                next_cells = [cell]
            else:
                new_next_cells = []
                for cell in next_cells:
                    cell.create_next_cells(self.functions)
                    flag = 0
                    for new_cell in new_next_cells:
                        if cell.next_cell_0.code == new_cell.code:
                            del(cell.next_cell_0)
                            cell.next_cell_0 = new_cell
                            flag = 1
                            continue
                        if cell.next_cell_1.code == new_cell.code:
                            del(cell.next_cell_1)
                            cell.next_cell_1 = new_cell
                            flag = 1
                            continue
                    if not flag:
                        new_next_cells.append(cell.next_cell_0)
                        new_next_cells.append(cell.next_cell_1)
                next_cells = new_next_cells
                result.append(new_next_cells)
        return result

    def graph_plot(self):
        for layer, x in zip(self.graph, range(len(self.graph))):
            for cell, y in zip(layer, range(len(layer))):
                plt.plot([x], [y], 'k.')
                cell.x = x
                cell.y = y
                if cell.next_cell_0 or cell.next_cell_1:
                    self.ax.text(x + 0.1, y - 0.1, int_to_bin(cell.next_cell_0_cost, len(self.functions)), fontsize=6, color='black')
                    self.ax.text(x + 0.1, y + 0.1, int_to_bin(cell.next_cell_1_cost, len(self.functions)), fontsize=6, color='red')
                    for next_cell, next_y in zip(self.graph[x + 1], range(len(self.graph[x + 1]))):
                        if cell.next_cell_0 == next_cell:
                            plt.plot([x, x + 1], [y, next_y], '--k', linewidth=0.3)
                        if cell.next_cell_1 == next_cell:
                            plt.plot([x, x + 1], [y, next_y], '-r', linewidth=0.3)
        for i in range(len(self.graph[-1])):
            self.ax.text(-1.5, i, int_to_bin(self.graph[-1][i].code, self.function_bit_length - 1), fontsize=11)

    def decode(self, code, show=None, result_show=None):
        if show:
            self.graph_plot()
        splitted_code = split_code(code, len(self.functions))
        print()
        if len(splitted_code) >= len(self.graph):
            return None
        result = []

        '''Deploy costs'''
        for layer, sp_code in zip(self.graph, splitted_code):
            cell_ncell_cost = []
            for cell in layer:
                cp = compare(
                    cell.next_cell_0_cost,
                    sp_code,
                    self.function_bit_length - 1
                )
                cell_ncell_cost.append([cell, cell.next_cell_0, cp])
                cp = compare(
                    cell.next_cell_1_cost,
                    sp_code,
                    self.function_bit_length - 1
                )
                # if show:
                #     self.ax.text(cell.x, -1, '{:0{}b}'.format(sp_code, len(self.functions)), color='blue')
                cell_ncell_cost.append([cell, cell.next_cell_1, cp])
            result.append(cell_ncell_cost)
        '''Create all paths'''
        for layer, iter in zip(result[1::], range(len(result))):
            diff = float('inf')
            for cell in layer:
                for prev_cell in result[iter]:
                    if cell[0] == prev_cell[1]:
                        cell[2] += prev_cell[2]
            new_layer = []
            if iter >= self.function_bit_length - 2:
                len_l = int(len(layer) / 2)
                for i in range(len_l):
                    if layer[i][2] < layer[i + len_l][2]:
                        new_layer.append(layer[i])
                    elif layer[i][2] > layer[i + len_l][2]:
                        new_layer.append(layer[i + len_l])
                    else:
                        new_layer.append(layer[i])
                result[iter + 1] = new_layer
        '''Show'''
        if show == 1:
            for layer in result[::-1]:
                for stroke in layer:
                    plt.plot([stroke[0].x, stroke[1].x], [stroke[0].y, stroke[1].y], '-b', linewidth=1)
                    self.ax.text(stroke[1].x - 0.3, stroke[1].y + 0.01, stroke[2], color='blue')
        elif show == 2:
            next_cell = [None, None, float('inf')]
            return_vec = []
            for cell in result[-1]:
                if cell[2] < next_cell[2]:
                    next_cell = cell
            return_vec.insert(0, next_cell)
            plt.plot(
                [next_cell[0].x, next_cell[1].x],
                [next_cell[0].y, next_cell[1].y],
                '-g'
            )
            self.ax.text(next_cell[1].x - 0.35, next_cell[1].y + 0.01, next_cell[2], color='green')
            for layer in result[len(result) - 2:: - 1]:
                for cell in layer:
                    if cell[1] == next_cell[0]:
                        buff = cell
                next_cell = buff
                return_vec.insert(0, next_cell)
                plt.plot([next_cell[0].x, next_cell[1].x], [next_cell[0].y, next_cell[1].y], '-g')
                self.ax.text(next_cell[1].x - 0.35, next_cell[1].y + 0.01, next_cell[2], color='green')
            return return_vec
        else:
            next_cell = [None, None, float('inf')]
            return_vec = []
            for cell in result[-1]:
                if cell[2] < next_cell[2]:
                    next_cell = cell
            return_vec.insert(0, next_cell)
            for layer in result[len(result) - 2:: - 1]:
                for cell in layer:
                    if cell[1] == next_cell[0]:
                        buff = cell
                next_cell = buff
                return_vec.insert(0, next_cell)
            rreturn_vec = []
            for cell in return_vec:
                rreturn_vec.append(get_cost(cell[0], cell[1]))
            if not result_show:
                return_str = ''
                for i in rreturn_vec:
                    return_str += str(i[1])
                return return_str
            else:
                return rreturn_vec

    def show(self):
        plt.axis('off')
        plt.show()


def encode(code, functions, result_show=None):
    code_list = list(code)
    bit_length = len(functions[0][2:])
    buffer = 0
    encoded_word = []
    for word in code_list:
        buffer = buffer >> 1
        buffer = ((2 ** (bit_length - 1)) * int(word)) | buffer
        result = 0
        for func in functions:
            result = result << 1
            result += odd_or_even(int(func, 2) & buffer)
        encoded_word.append([result, int(word)])
    if not result_show:
        return_str = ''
        for i in encoded_word:
            return_str += '{:0{}b}'.format(i[0], len(functions))
        return return_str
    else:
        return encoded_word


def odd_or_even(number):
    return bin(number).count('1') % 2


def int_to_bin(number, bit_length):
    return '{:0{}b}'.format(
        number,
        bit_length
    )


def split_code(code, split_len):
    code_list = []
    for i in range(0, len(code), split_len):
        code_list.append(int(code[i:i+split_len], 2))
    return code_list


def compare(number_1, number_2, bit_length):
    result = 0
    for i in range(bit_length):
        if not bin(number_1)[-1] == bin(number_2)[-1]:
            result += 1
        number_1 = number_1 >> 1
        number_2 = number_2 >> 1
    return result

def get_cost(cell_1, cell_2):
    if cell_1.next_cell_0 == cell_2:
        return [cell_1.next_cell_0_cost, 0]
    elif cell_1.next_cell_1 == cell_2:
        return [cell_1.next_cell_1_cost, 1]
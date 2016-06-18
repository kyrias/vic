from copy import deepcopy

from .util import invert_index, lpop, group_by_n
from .rotation import rotate_left


def first_transposition(message_list, key):
    key = list(map(int, key))
    width = len(key)

    indexes = invert_index(key)

    dimensional_array = []
    while message_list:
        line = message_list[:width]
        if len(line) < width:
            line += [None] * (width - len(line))
        message_list = message_list[width:]

        dimensional_array.append(line)

    rotated = rotate_left(dimensional_array)

    result = []
    for index in indexes:
        for char in rotated[-(index + 1)]:
            if char is not None:
                result += [char]

    return result


def undo_first_transposition(message_list, key):
    key = list(map(int, key))

    message_list = deepcopy(message_list)
    message_length = len(message_list)
    width = len(key)
    height = message_length // width

    indexes = invert_index(key)

    table = []
    for i in range(0, height):
        table.append([None] * width)

    last_width = message_length % width
    last_row = []
    last_row += [None] * last_width
    last_row += ['-'] * (width - last_width)
    table.append(last_row)


    row_i = 0
    row = table[row_i]
    column_i, indexes = lpop(indexes)
    column = row[column_i]

    while True:
        row = table[row_i]
        column = table[row_i][column_i]

        if column == '-':
            row_i = 0
            column_i, indexes = lpop(indexes)

        else:
            digit, message_list = lpop(message_list)
            row[column_i] = digit
            row_i += 1

        if row_i > height:
            row_i = 0
            if indexes:
                column_i, indexes = lpop(indexes)
            else:
                break

    res = []
    for row in table:
        for column in row:
            if column == '-':
                continue
            res.append(column)

    return res


def second_transposition(message_list, key):
    message_length = len(message_list)
    key = list(map(int, key))
    key_length = len(key)

    disruption_table = build_disruption_table(key, message_length)

    for row in disruption_table:
        for i, digit in enumerate(row):
            if digit is None:
                digit, message_list = lpop(message_list)
                row[i] = digit

    last = message_length % key_length
    last_row = []
    while last:
        digit, message_list = lpop(message_list)
        last_row.append(digit)
        last -= 1

    if last_row:
        disruption_table.append(last_row)

    # Fill in disruptions:
    for row in disruption_table:
        for i, digit in enumerate(row):
            if digit == '*':
                digit, message_list = lpop(message_list)
                row[i] = digit
        if len(row) != key_length:
            row += [None] * (key_length - len(row))

    # Rotate left so we can read row-by-row
    left = rotate_left(disruption_table)

    key_indexes = invert_index(key)
    result = []
    for key_index in key_indexes:
        for digit in left[-(key_index + 1)]:
            if digit is not None:
                result.append(digit)

    return result


def undo_second_transposition(message_list, key):
    from math import ceil

    message_length = len(message_list)
    key = list(map(int, key))
    key_length = len(key)
    indexes = invert_index(key)

    height = ceil(message_length / key_length)

    disruption_table = build_disruption_table(key, message_length)

    # Add last line

    last_width = message_length % key_length
    last_row = []
    last_row += [None] * last_width
    last_row += ['-'] * (key_length - last_width)

    if last_row:
        disruption_table.append(last_row)

    full_table = deepcopy(disruption_table)

    row_i = 0
    column_i, indexes = lpop(indexes)
    while True:
        row = full_table[row_i]
        column = row[column_i]

        if column == '-':
            row_i = 0
            column_i, indexes = lpop(indexes)

        else:
            digit, message_list = lpop(message_list)
            row[column_i] = digit
            row_i += 1

        if row_i == height:
            row_i = 0
            if indexes:
                column_i, indexes = lpop(indexes)
            else:
                break

    res = []
    res_last = []
    for row_i, row in enumerate(full_table):
        for column_i, column in enumerate(row):
            if disruption_table[row_i][column_i] == '*':
                res_last.append(column)
            elif disruption_table[row_i][column_i] == '-':
                continue
            else:
                res.append(column)

    res.extend(res_last)
    return res


def build_disruption_table(key, message_length):
    width = len(key)
    height = message_length // width

    table = []

    key_indexes = invert_index(key)
    key_index, key_indexes = lpop(key_indexes)

    while height:
        table.append(([None] * key_index) + (['*'] * (width - key_index)))

        key_index += 1

        if key_index > width:
            key_index, key_indexes = lpop(key_indexes)

        height -= 1

    return table

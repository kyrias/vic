from math import ceil
from string import ascii_uppercase
from itertools import count, cycle

from .utils import modular_addition, modular_subtraction, take, chunk, pad_to_multiple, \
        inverted_list_index


def sequentialize(inputs):
    """The sequentialization process turns a list of N letters or digits into
    an N numbered sequence of the input characters labeled in alphanumerical
    order.

    Example:
        AABCD
     -> 01234

        DCBAA
     -> 43201

        TENLETTERS
     -> 7043189256

    """

    # First get sorted list of unique characters in the input
    unique_chars = sorted(set(inputs))

    # Generate the result list that we can fill in with values as we go
    result = [None] * len(inputs)

    counter = count()
    for unique_char in unique_chars:
        current_chars = filter(lambda x: x[1] == unique_char, enumerate(inputs))
        for index, _ in current_chars:
            # Assign the next available number to the current index
            result[index] = next(counter)

    return result


def lagged_fibonacci(initial):
    """A lagged Fibonacci generator takes a number of starting digits, then
    adds the first two digits mod 10 appends that to the list, then continue
    with the second and third digits, and so on."""

    chain = list(initial)

    # First we yield all numbers in the initial list
    for i in initial:
        yield i

    # Then on each additional yield we calculate an additional digit
    while len(chain) > 1:
        first_digit = chain.pop(0)
        second_digit = chain[0]
        new = (first_digit + second_digit) % 10
        chain.append(new)
        yield new


def calculate_transposition_offsets(U):
    """Select the last two non-equal digits of the U block"""
    rev_U = list(reversed(U))
    second_offset = rev_U.pop(0)
    first_offset = next(filter(lambda x: x != second_offset, rev_U))
    return (first_offset, second_offset)


def calculate_transposition_key_seed(seq_kp_1, seq_kp_2, message_id, date):
    # First we subtract the date from the message ID to get the initial list of numbers
    initialization = modular_subtraction(message_id, date)

    # Then we expand the initialization list to 10 digits
    expanded = take(lagged_fibonacci(initialization), 10)

    # And add that together with the sequentialized first part of the keyphrase
    G = modular_addition(expanded, seq_kp_1)

    # Then we use each resulting digit as an index into the second sequentialized part of the keyphrase
    T = list(map(lambda idx: seq_kp_2[idx], G))
    return T


def permute_transposition_key_block(expanded_seed, sequentialized_seed):
    # Matrix right-rotate expanded seed
    rotated = zip(*reversed(expanded_seed))

    # Reverse each resulting row
    reversed_rows = map(lambda l: reversed(l), rotated)

    # Sort key rows according to the sequentialized seed
    key_rows = map(lambda r: r[1], sorted(zip(sequentialized_seed, reversed_rows), key=lambda k: k[0]))

    return [ digit for row in key_rows for digit in row ]


def generate_keys(checkerboard_key, keyphrase, personal_id, message_id, date):
    # First we divide the keyphrase into two parts, and sequentialize them individually
    seq_kp_1 = sequentialize(list(keyphrase[:10]))
    seq_kp_2 = sequentialize(list(keyphrase[10:20]))

    # Calculate the initial transposition key seed and sequentialize it
    transp_key_seed = calculate_transposition_key_seed(seq_kp_1, seq_kp_2, message_id, date)
    seq_transp_key_seed = sequentialize(transp_key_seed)

    # And then expand that seed to 60 digits, take the last 50 digits, and split that into chunks of
    # 10 digits
    expanded_transp_key_seed = list(chunk(take(lagged_fibonacci(transp_key_seed), 60)[10:], 10))

    # Permute the expanded transposition key seed to get the final key block
    transp_key_block = permute_transposition_key_block(expanded_transp_key_seed, seq_transp_key_seed)

    # Calculate the widths of the two transposition key chunks
    (offset_1, offset_2) = calculate_transposition_offsets(transp_key_block)
    key_width_1 = personal_id + offset_1
    key_width_2 = personal_id + offset_2

    transp_key_1 = sequentialize(transp_key_block[:key_width_1])
    transp_key_2 = sequentialize(transp_key_block[key_width_1:key_width_1+key_width_2])

    # The last row of the expanded transposition key seed is used as the order in which the
    # checkerboard columns will be numbered
    checkerboard_column_order = sequentialize(expanded_transp_key_seed[-1])

    return (checkerboard_column_order, transp_key_1, transp_key_2)


def build_checkerboard(checkerboard_key, column_order):
    alphabet = ascii_uppercase + './'
    remaining_chars = list(filter(lambda c: c not in checkerboard_key, alphabet))

    layer_1 = checkerboard_key
    layer_2 = remaining_chars[:10]
    layer_3 = remaining_chars[10:20]

    table = {}
    for idx, char in filter(lambda c: c[1] != ' ', enumerate(layer_1)):
        table[char] = str(column_order[idx])

    hole_1 = checkerboard_key.index(' ')
    hole_2 = checkerboard_key.index(' ', hole_1 + 1)

    for hole, layer in [(hole_1, layer_2), (hole_2, layer_3)]:
        for idx, char in enumerate(layer):
            table[char] = '{:02}'.format(column_order[hole]*10 + idx)

    return table


def checkerboard_lookup(message, checkerboard):
    result = []
    for char in message:
        value = checkerboard[char]
        if len(value) > 1:
            result.extend(list(value))
        else:
            result.append(value)

    return pad_to_multiple(result, '0',  5)


def first_transposition(key, message):
    """The first VIC transposition is a simple column transposition consisting of just reading
    out the message columns in the order specified by the key.
    """

    # Pad message with Nones for the matrix left rotation to work
    padded = pad_to_multiple(message, None, len(key))
    chunked = list(chunk(message, len(key)))

    # Zip the chunk rows together to form the new columns and map the result to lists instead of
    # tuples, then reverse the list of rows
    rotated_rows = list(map(lambda c: list(c), zip(*chunked)))

    # Sort the rows according to the key
    sorted_rows = sorted(zip(key, rotated_rows), key=lambda r: r[0])
    # Then map away the key from the row tuple
    rows = map(lambda r: r[1], sorted_rows)

    # Filter out the padded Nones again
    filtered = [ filter(lambda c: c != None, row) for row in rows ]

    # Flatten the list of lists into a single list
    flattened = [ digit for row in filtered for digit in row ]

    return flattened


def build_disruption_table(key, message_length):
    width = len(key)
    height = message_length // width

    # Get the indexes into the key that gives the values in order
    key_index = inverted_list_index(key)
    index_generator = cycle(key_index)
    index = next(index_generator)

    table = []
    while height:
        table.append(([None] * index) + (['*'] * (width - index)))
        index += 1

        # If we filled the whole line with Nones, get the next lowest key value index
        if index > width:
            index = next(index_generator)

        height -= 1

    return table


def second_transposition(key, message):
    """The second transposition is a disrupted transposition, where the disruption pattern is
    determined by the width of the transposition table and the key.
    """
    message_length = len(message)
    disruption_table = build_disruption_table(key, message_length)

    # Fill in the left portion of the disruption table
    for row in disruption_table:
        for idx, _ in filter(lambda r: r[1] is None, enumerate(row)):
            row[idx] = message.pop(0)

    # Fill in the last row, if message isn't a multiple of the key
    last_row_length = (message_length % len(key))
    last_row = []
    while last_row_length:
        last_row.append(message.pop(0))
        last_row_length -= 1
    if last_row:
        last_row.extend([None] * (len(key) - len(last_row)))
        disruption_table.append(last_row)

    # Fill in the right portion of the disruption table
    for row in disruption_table:
        for idx, _ in filter(lambda r: r[1] == '*', enumerate(row)):
            if message:
                row[idx] = message.pop(0)
            else:
                row[idx] = '!'

    # Zip the chunk rows together to form the new columns and map the result to lists instead of
    # tuples
    rotated_rows = list(map(lambda c: list(c), zip(*disruption_table)))

    # Sort the rows according to the key
    sorted_rows = sorted(zip(key, rotated_rows), key=lambda r: r[0])
    # Then map away the key from the row tuple
    rows = map(lambda r: r[1], sorted_rows)

    # Filter out the padded Nones again
    filtered = [ filter(lambda c: c != None, row) for row in rows ]

    # Flatten the list of lists into a single list
    flattened = [ digit for row in filtered for digit in row ]

    return list(chunk(flattened, 5))

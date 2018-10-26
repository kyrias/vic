from .primitives import generate_keys, build_checkerboard, invert_checkerboard, \
                        checkerboard_lookup, first_transposition, second_transposition, \
                        undo_second_transposition, undo_first_transposition, inverted_checkerboard_lookup
from .utils import chunk


# The VIC cipher requires the following pieces of input:
# 1) Checkerboard key, 8 characters + 2 spaces
# 2) Key phrase, 20 characters
# 3) Date, 6-digits
# 4) Personal identifier, 2-digits
# 5) Random and unique message identifier, 5-digits

def encrypt(checkerboard_key, keyphrase, personal_id, date, message_id, message):
    (column_order, transp_key_1, transp_key_2) = generate_keys(checkerboard_key, keyphrase, personal_id, date, message_id)
    checkerboard = build_checkerboard(checkerboard_key, column_order)

    # Look up the plaintext in the checkerboard
    checkered = checkerboard_lookup(checkerboard, message)

    # Transpose the checkered ciphertext
    transposed = first_transposition(transp_key_1, checkered)
    transposed = second_transposition(transp_key_2, transposed)

    message_id = list(map(str, message_id))

    # Last digit of the date says where to insert the message identifier into the ciphertext
    index = date[-1] % len(transposed)
    if index == 0:
        # If the index is 1, we need to append rather than insert
        transposed.append(message_id)
    else:
        transposed.insert(-index, message_id)

    print(' '.join(map(lambda l: ''.join(l), transposed)))


def decrypt(checkerboard_key, keyphrase, personal_id, date, ciphertext):
    # Split the ciphertext into groups of five digits
    ciphertext = list(chunk(list(filter(lambda c: c != ' ', ciphertext)), 5))

    # Extract the message identifier from the ciphertext
    index = date[-1] % (len(ciphertext) - 1)
    message_id = ciphertext.pop(-(index+1))
    message_id = list(map(lambda d: int(d), list(message_id)))

    (column_order, transp_key_1, transp_key_2) = generate_keys(checkerboard_key, keyphrase, personal_id, date, message_id)

    # Untranspose the ciphertext
    untransposed_once = undo_second_transposition(transp_key_2, ciphertext)
    untransposed_twice = undo_first_transposition(transp_key_1, untransposed_once)

    # Uncheckerboard the untransposed ciphertext
    checkerboard = build_checkerboard(checkerboard_key, column_order)
    inverted_checkerboard = invert_checkerboard(checkerboard)
    plaintext = inverted_checkerboard_lookup(inverted_checkerboard, untransposed_twice)

    print(''.join(plaintext))

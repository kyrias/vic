from .primitives import generate_keys, build_checkerboard, checkerboard_lookup, first_transposition, second_transposition


# The VIC cipher requires the following pieces of input:
# 1) Checkerboard key, 8 characters + 2 spaces
# 2) Key phrase, 20 characters
# 3) Date, 6-digits
# 4) Personal identifier, 2-digits
# 5) Random and unique message identifier, 5-digits

def encrypt(checkerboard_key, keyphrase, personal_id, message_id, date, message):
    (column_order, transp_key_1, transp_key_2) = generate_keys(checkerboard_key, keyphrase, personal_id, message_id, date)
    checkerboard = build_checkerboard(checkerboard_key, column_order)

    # Look up the plaintext in the checkerboard
    checkered = checkerboard_lookup(checkerboard, message)

    # Transpose the checkered ciphertext
    transposed = first_transposition(transp_key_1, checkered)
    transposed = second_transposition(transp_key_2, transposed)

    message_id = list(map(str, message_id))

    # Last digit of the date says where to insert the message identifier into the ciphertext
    index = date[-1]
    if date[-1] == 0:
        # if the digit is 0, treat it as 10
        index = 10
    if index == 1:
        # If the index is 1, we need to append rather than insert
        transposed.append(message_id)
    else:
        transposed.insert(1 - index, message_id)

    print(' '.join(map(lambda l: ''.join(l), transposed)))

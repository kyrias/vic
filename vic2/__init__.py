from .primitives import generate_keys, build_checkerboard, checkerboard_lookup, first_transposition


# The VIC cipher requires the following pieces of input:
# 1) Checkerboard key, 8 characters + 2 spaces
# 2) Key phrase, 20 characters
# 3) Date, 6-digits
# 4) Personal identifier, 2-digits
# 5) Random and unique message identifier, 5-digits

def encrypt(checkerboard_key, keyphrase, personal_id, message_id, date, message):
    (column_order, transp_key_1, transp_key_2) = generate_keys(checkerboard_key, keyphrase, personal_id, message_id, date)
    checkerboard = build_checkerboard(checkerboard_key, column_order)
    checkered = checkerboard_lookup(message, checkerboard)
    transposed = first_transposition(transp_key_1, checkered)

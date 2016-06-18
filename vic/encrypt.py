from .ik import (generate_ik)
from .checkerboard import (build_checkerboard, lookup)
from .transposition import (first_transposition, second_transposition)
from .message_indicator import (insert_message_indicator)


def encrypt(args):
    # Uppercase and replace spaces
    plaintext = args.plaintext.replace(' ', '.')
    plaintext = plaintext.upper()

    keys = generate_ik(args.passphrase, args.message_id, args.date, args.personal_id)

    checkerboard = build_checkerboard(args.checkerboard_key, keys['checkerboard_header'])
    checkered = lookup(plaintext, checkerboard)

    transposed_once = first_transposition(checkered, keys['key_one'])
    transposed_twice = second_transposition(transposed_once, keys['key_two'])

    ciphertext = insert_message_indicator(transposed_twice,
                                          list(args.message_id),
                                          list(args.date))

    print(' '.join(list(map(''.join, ciphertext))))

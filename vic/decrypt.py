from .ik import (generate_ik)
from .message_indicator import (pop_message_indicator)
from .transposition import (undo_first_transposition, undo_second_transposition)
from .checkerboard import (build_inverted_checkerboard, inverted_lookup)


def decrypt(args):
    # Allow grouped ciphertext input
    ciphertext = args.ciphertext.replace(' ', '')

    # Pop the message ID from the ciphertext
    message_id, ciphertext = pop_message_indicator(ciphertext, list(args.date))

    keys = generate_ik(args.passphrase, message_id, args.date, args.personal_id)

    untransposed_once = undo_second_transposition(ciphertext, keys['key_two'])
    untransposed_twice = undo_first_transposition(untransposed_once, keys['key_one'])

    checkerboard = build_inverted_checkerboard(args.checkerboard_key, keys['checkerboard_header'])
    uncheckered = inverted_lookup(untransposed_twice, checkerboard)

    print(''.join(uncheckered))

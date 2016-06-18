#!/usr/bin/env python3

import argparse

from ik import derive_s, derive_g, derive_t, derive_u, derive_w, derive_k, derive_c
from message_indicator import pop_message_indicator
from transposition import undo_first_transposition, undo_second_transposition
from checkerboard import build_inverted_checkerboard, inverted_lookup


def pa(a):
    for row in a:
        print('\t'.join([str(x) for x in row]))


def main(checkerboard_key, passphrase,
         date, personal_id,
         ciphertext):

    # Allow grouped ciphertext input
    ciphertext = ciphertext.replace(' ', '')

    # Pop the message ID from the ciphertext
    message_id, ciphertext = pop_message_indicator(ciphertext, date)

    s_one, s_two = derive_s(passphrase)
    g = derive_g(message_id, date, s_one)
    t = derive_t(g, s_two)
    u = derive_u(t)
    checkerboard_header = derive_c(u)

    width_one, width_two = derive_w(personal_id, u)
    key_one, key_two = derive_k(t, u, width_one, width_two)

    untransposed_once = undo_second_transposition(ciphertext, key_two)
    untransposed_twice = undo_first_transposition(untransposed_once, key_one)

    checkerboard = build_inverted_checkerboard(checkerboard_key, checkerboard_header)
    uncheckered = inverted_lookup(untransposed_twice, checkerboard)

    print(''.join(uncheckered))


parser = argparse.ArgumentParser(description='VIC cipher decrypter')

parser.add_argument('-m', '--message',
                    dest='ciphertext',
                    action='store',
                    required=True,
                    help='Ciphertext to decrypt')

parser.add_argument('-c', '--checkerboard-key',
                    dest='checkerboard_key',
                    action='store',
                    required=True,
                    help='Key for the straddling checkerboard')

parser.add_argument('-p', '--passphrase',
                    dest='passphrase',
                    action='store',
                    required=True,
                    help='Passphrase used to derive keys')

parser.add_argument('-d', '--date',
                    dest='date',
                    action='store',
                    required=True,
                    help='Date used to derive keys and to insert the message ID group')

parser.add_argument('-i', '--personal-id',
                    dest='personal_id',
                    action='store',
                    required=True,
                    help='Personal ID for generating transposition tables')


if __name__ == '__main__':
    args = parser.parse_args()

    main(args.checkerboard_key,
         args.passphrase,
         args.date,
         args.personal_id,
         args.ciphertext)

#!/usr/bin/env python3

import argparse

from ik import derive_s, derive_g, derive_t, derive_u, derive_w, derive_k, derive_c
from checkerboard import build_checkerboard, lookup
from transposition import first_transposition, second_transposition
from message_indicator import insert_message_indicator


def main(checkerboard_key, passphrase,
         message_id, date, personal_id,
         message):

    s_one, s_two = derive_s(passphrase)
    g = derive_g(message_id, date, s_one)
    t = derive_t(g, s_two)
    u = derive_u(t)

    width_one, width_two = derive_w(personal_id, u)
    key_one, key_two = derive_k(t, u, width_one, width_two)
    checkerboard_header = derive_c(u)

    checkerboard = build_checkerboard(checkerboard_key, checkerboard_header)
    checkered = lookup(message, checkerboard)

    transposed_once = first_transposition(checkered, key_one)
    transposed_twice = second_transposition(transposed_once, key_two)

    ciphertext = insert_message_indicator(transposed_twice,
                                          list(message_id),
                                          list(date))

    print(' '.join(list(map(''.join, ciphertext))))


parser = argparse.ArgumentParser(description='VIC cipher encrypter')

parser.add_argument('-m', '--message',
                    dest='message',
                    action='store',
                    required=True,
                    help='Message to be encrypted')

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

parser.add_argument('-M', '--message-id',
                    dest='message_id',
                    action='store',
                    required=True,
                    help='Unique and random message ID')

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
         args.message_id,
         args.date,
         args.personal_id,
         args.message)

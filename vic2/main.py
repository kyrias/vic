import sys
import argparse

from . import encrypt, decrypt


def argparser():
    parser = argparse.ArgumentParser(prog='vic')
    subparsers = parser.add_subparsers(dest='subparser',
                                       help='action sub-commands')

    parser_encrypt = subparsers.add_parser('encrypt', description='VIC cipher encrypter')
    parser_encrypt.add_argument('-c', '--checkerboard-key',
                                dest='checkerboard_key',
                                action='store',
                                required=True,
                                help='Straddling checkerboard key. (8 characters + 2 spaces)')
    parser_encrypt.add_argument('-k', '--keyphrase',
                                dest='keyphrase',
                                action='store',
                                required=True,
                                help='Keyphrase used to derive transposition table keys. (20 characters)')
    parser_encrypt.add_argument('-p', '--personal-id',
                                dest='personal_id',
                                action='store',
                                required=True,
                                help='Personal ID used to derive transposition tables. (2 digits)')
    parser_encrypt.add_argument('-i', '--message-id',
                                dest='message_id',
                                action='store',
                                required=True,
                                help='Unique and random message ID. (5 digits)')
    parser_encrypt.add_argument('-d', '--date',
                                dest='date',
                                action='store',
                                required=True,
                                help='Date used to derive keys and inserted into message ID group. (6 digits)')
    parser_encrypt.add_argument('-t', '--plaintext',
                                dest='message',
                                action='store',
                                required=True,
                                help='Plaintext to encrypt')


    parser_decrypt = subparsers.add_parser('decrypt', description='VIC cipher decrypter')
    parser_decrypt.add_argument('-c', '--checkerboard-key',
                                dest='checkerboard_key',
                                action='store',
                                required=True,
                                help='Straddling checkerboard key. (8 characters + 2 spaces)')
    parser_decrypt.add_argument('-k', '--keyphrase',
                                dest='keyphrase',
                                action='store',
                                required=True,
                                help='Keyphrase used to derive transposition table keys. (20 characters)')
    parser_decrypt.add_argument('-p', '--personal-id',
                                dest='personal_id',
                                action='store',
                                required=True,
                                help='Personal ID used to derive transposition tables. (2 digits)')
    parser_decrypt.add_argument('-d', '--date',
                                dest='date',
                                action='store',
                                required=True,
                                help='Date used to derive keys and inserted into message ID group. (6 digits)')
    parser_decrypt.add_argument('-t', '--ciphertext',
                                dest='message',
                                action='store',
                                required=True,
                                help='Ciphertext to decrypt')

    return parser


def validate_arguments(args):
    error = False

    # Checkerboard key
    if len(args.checkerboard_key) != 10:
        print('Error: Specified checkerboard key has a length of {}, length of 10 required'.format(len(args.checkerboard_key)), file=sys.stderr)
        error = True

    num_spaces = len(list(filter(lambda c: c == ' ', args.checkerboard_key)))
    if num_spaces != 2:
        print('Error: Specified checkerboard key contains {} spaces, 2 required'.format(num_spaces), file=sys.stderr)
        error = True

    num_non_spaces = len(list(filter(lambda c: c != ' ', args.checkerboard_key)))
    if num_non_spaces != 8:
        print('Error: Specified checkerboard key contains {} non-space characters, 8 required'.format(num_non_spaces), file=sys.stderr)
        error = True


    # Keyphrase
    if len(args.keyphrase) != 20:
        print('Error: Specified keyphrase has a length of {}, length of 20 required'.format(len(args.keyphrase)), file=sys.stderr)
        error = True


    # Personal ID
    if len(args.personal_id) != 2:
        print('Error: Specified personal ID has a length of {}, length of 2 required'.format(len(args.personal_id)), file=sys.stderr)
        error = True


    if args.subparser == 'encrypt':
        # Message ID
        if len(args.message_id) != 5:
            print('Error: Specified message ID has a length of {}, length of 5 required'.format(len(args.message_id)), file=sys.stderr)
            error = True


    # Date
    if len(args.date) != 6:
        print('Error: Specified date has a length of {}, length of 6 required'.format(len(args.date)), file=sys.stderr)
        error = True

    if error:
        sys.exit(1)


def main():
    parser = argparser()
    args = parser.parse_args()
    if args.subparser == 'encrypt':
        validate_arguments(args)

        checkerboard_key = args.checkerboard_key
        keyphrase = args.keyphrase
        personal_id = int(args.personal_id)
        message_id = list(map(lambda d: int(d), list(args.message_id)))
        date = list(map(lambda d: int(d), list(args.date)))
        message = args.message

        encrypt(checkerboard_key, keyphrase, personal_id, message_id, date, message)

    elif args.subparser == 'decrypt':
        validate_arguments(args)

        checkerboard_key = args.checkerboard_key
        keyphrase = args.keyphrase
        personal_id = int(args.personal_id)
        date = list(map(lambda d: int(d), list(args.date)))
        message = args.message

        decrypt(checkerboard_key, keyphrase, personal_id, date, message)

    else:
        sys.exit(parser.parse_args(['--help']))

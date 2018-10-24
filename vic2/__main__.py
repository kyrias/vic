import sys
import argparse

from . import encrypt


def validate_arguments(args):
    # Checkerboard key
    if len(args.checkerboard_key) != 10:
        print('Error: Specified checkerboard key has a length of {}, length of 10 required'.format(len(args.checkerboard_key)), file=sys.stderr)
        sys.exit(1)

    num_spaces = len(list(filter(lambda c: c == ' ', args.checkerboard_key)))
    if num_spaces != 2:
        print('Error: Specified checkerboard key contains {} spaces, 2 required'.format(num_spaces), file=sys.stderr)
        sys.exit(1)

    num_non_spaces = len(list(filter(lambda c: c != ' ', args.checkerboard_key)))
    if num_non_spaces != 8:
        print('Error: Specified checkerboard key contains {} non-space characters, 8 required'.format(num_non_spaces), file=sys.stderr)
        sys.exit(1)

    # Keyphrase
    if len(args.keyphrase) != 20:
        print('Error: Specified keyphrase has a length of {}, length of 20 required'.format(len(args.keyphrase)), file=sys.stderr)
        sys.exit(1)

    # Personal ID
    if len(args.personal_id) != 2:
        print('Error: Specified personal ID has a length of {}, length of 2 required'.format(len(args.personal_id)), file=sys.stderr)
        sys.exit(1)

    # Message ID
    if len(args.message_id) != 5:
        print('Error: Specified message ID has a length of {}, length of 5 required'.format(len(args.message_id)), file=sys.stderr)
        sys.exit(1)

    # Date
    if len(args.date) != 6:
        print('Error: Specified date has a length of {}, length of 6 required'.format(len(args.date)), file=sys.stderr)
        sys.exit(1)




def main():
    parser = argparse.ArgumentParser(prog='vic')
    subparsers = parser.add_subparsers(dest='subparser',
                                       help='action sub-commands')

    parser_encrypt = subparsers.add_parser('encrypt', description='VIC cipher encrypter')
    parser_encrypt.add_argument('-c', '--checkerboard-key',
                                dest='checkerboard_key',
                                action='store',
                                required=True,
                                help='Key for the straddling checkerboard. (8 characters + 2 spaces)')
    parser_encrypt.add_argument('-k', '--keyphrase',
                                dest='keyphrase',
                                action='store',
                                required=True,
                                help='eyphrase used to derive keys. (20 characters)')
    parser_encrypt.add_argument('-p', '--personal-id',
                                dest='personal_id',
                                action='store',
                                required=True,
                                help='Personal ID used for generating transposition tables. (2 digits)')
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
    parser_encrypt.add_argument('-m', '--message',
                                dest='message',
                                action='store',
                                required=True,
                                help='Message to be encrypted')

    args = parser.parse_args()
    if not args.subparser:
        sys.exit(parser.parse_args(['--help']))

    if args.subparser == 'encrypt':
        validate_arguments(args)

        checkerboard_key = args.checkerboard_key
        keyphrase = args.keyphrase
        personal_id = int(args.personal_id)
        message_id = list(map(lambda d: int(d), list(args.message_id)))
        date = list(map(lambda d: int(d), list(args.date)))
        message = args.message

        encrypt(checkerboard_key, keyphrase, personal_id, message_id, date, message)

main()
sys.exit(1)


checkerboard_key = "A SIN TOER"
keyphrase = 'ALLTHEPEOPLEAREDEADB'.strip()
message_identifier = [6, 0, 1, 1, 5]
date = [3, 9, 1, 7, 5, 2]
personal_number = 15


encrypt(checkerboard_key, keyphrase, message_identifier, date, personal_number)

import argparse
from sys import exit

from .encrypt import encrypt
from .decrypt import decrypt


def main():
    parser = argparse.ArgumentParser(prog='vic')
    subparsers = parser.add_subparsers(dest='subparser',
                                       help='sub-command help')

    # Encryption subparser

    parser_encrypt = subparsers.add_parser('encrypt', description='VIC cipher encrypter')
    parser_encrypt.set_defaults(func=encrypt)

    parser_encrypt.add_argument('-m', '--message',
                                dest='plaintext',
                                action='store',
                                required=True,
                                help='Message to be encrypted')

    parser_encrypt.add_argument('-c', '--checkerboard-key',
                                dest='checkerboard_key',
                                action='store',
                                required=True,
                                help='Key for the straddling checkerboard')

    parser_encrypt.add_argument('-p', '--passphrase',
                                dest='passphrase',
                                action='store',
                                required=True,
                                help='Passphrase used to derive keys')

    parser_encrypt.add_argument('-M', '--message-id',
                                dest='message_id',
                                action='store',
                                required=True,
                                help='Unique and random message ID')

    parser_encrypt.add_argument('-d', '--date',
                                dest='date',
                                action='store',
                                required=True,
                                help='Date used to derive keys and to insert the message ID group')

    parser_encrypt.add_argument('-i', '--personal-id',
                                dest='personal_id',
                                action='store',
                                required=True,
                                help='Personal ID for generating transposition tables')

    # Decryption subparser

    parser_decrypt = subparsers.add_parser('decrypt', description='VIC cipher decrypter')
    parser_decrypt.set_defaults(func=decrypt)

    parser_decrypt.add_argument('-m', '--message',
                                dest='ciphertext',
                                action='store',
                                required=True,
                                help='Ciphertext to decrypt')

    parser_decrypt.add_argument('-c', '--checkerboard-key',
                                dest='checkerboard_key',
                                action='store',
                                required=True,
                                help='Key for the straddling checkerboard')

    parser_decrypt.add_argument('-p', '--passphrase',
                                dest='passphrase',
                                action='store',
                                required=True,
                                help='Passphrase used to derive keys')

    parser_decrypt.add_argument('-d', '--date',
                                dest='date',
                                action='store',
                                required=True,
                                help='Date used to derive keys and to insert the message ID group')

    parser_decrypt.add_argument('-i', '--personal-id',
                                dest='personal_id',
                                action='store',
                                required=True,
                                help='Personal ID for generating transposition tables')

    args = parser.parse_args()
    if not args.subparser:
        exit(parser.parse_args(['--help']))

    exit(args.func(args))


if __name__ == '__main__':
    main()

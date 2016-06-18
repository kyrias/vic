=====
 VIC
=====

This is a Python 3 implementation of the pen-and-paper cipher used by the Soviet spy Reino Häyhänen, codenamed "VICTOR", in the 1950s.

If you have 3to2 from the PyPI installed you can just run ``make 3to2`` and you will end up with a copy of the cipher implementation in the ``3to2/`` subdirectory converted to run under Python 2.


Usage
=====

The ``vic`` entrypoint has two subcommands, ``encrypt`` and ``decrypt``.  To encrypt something you have to pass the following as arguments to the ``encrypt`` subcommand:

1. A 10 character key for the straddling checkerboard, with two of those characters being spaces that are used for the second and third layer of the checkerboard.
2. A 5 digit unique and random message ID.
3. A 20 character passphrase used to derive keys.
4. A date used to derive keys and to insert the message ID into the ciphertext. (``DDMMYYYY``)
5. A 1 or 2 digit personal identifier, unique per person.
6. A cleartext message to encrypt.


To decrypt a message you have to pass the following as arguments to the ``decrypt`` subcommand:

1. A 10 character key for the straddling checkerboard, with two of those characters being spaces that are used for the second and third layer of the checkerboard.
2. A 20 character passphrase used to derive keys.
3. A date used to derive keys and to insert the message ID into the ciphertext. (``DDMMYYYY``)
4. A 1 or 2 digit personal identifier, unique per person.
5. A cleartext message to encrypt.

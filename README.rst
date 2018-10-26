=====
 VIC
=====

This is a Python 3 implementation of the pen-and-paper cipher used by the Soviet spy Reino Häyhänen, codenamed "VICTOR", in the 1950s.


Usage
=====

The ``vic`` entrypoint has two subcommands, ``encrypt`` and ``decrypt``.  To encrypt something you have to pass the following as arguments to the ``encrypt`` subcommand:

1. A 10 character key for the straddling checkerboard, where two of those characters are spaces that
   are used for the second and third layer of the checkerboard.
2. A 20 character passphrase used to derive the keys for the two transposition tables.
3. A 2 digit personal ID assigned per agent.  This is used to split the transposition key for the
   two transposition tables, thus making this too big means that the first table might end up taking
   up all of the key.  I would recommend keeping the IDs at least under 40.
4. A 6 digit date used to derive keys, and the last digit specifies where the message ID is inserted
   into the ciphertext.
5. A 5 digit unique and random message ID.
6. A plaintext message to encrypt.


To decrypt a message you have to pass the following as arguments to the ``decrypt`` subcommand:

1. A 10 character key for the straddling checkerboard, where two of those characters are spaces that
   are used for the second and third layer of the checkerboard.
2. A 20 character passphrase used to derive the keys for the two transposition tables.
3. A 2 digit personal ID assigned per agent.  This is used to split the transposition key for the
   two transposition tables, thus making this too big means that the first table might end up taking
   up all of the key.  I would recommend keeping the IDs at least under 40.
4. A 6 digit date used to derive keys, and the last digit specifies where the message ID is inserted
   into the ciphertext.
5. A ciphertext message to decrypt.

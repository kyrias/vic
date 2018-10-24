from itertools import islice


def take(generator, n):
    return list(islice(generator, n))


def modular_addition(list_a, list_b):
    return [ (a + b) % 10 for a, b in zip(list_a, list_b) ]


def modular_subtraction(list_a, list_b):
    return [ (a - b) % 10 for a, b in zip(list_a, list_b) ]


def chunk(chunkable, n):
    """ Yield successive n-sized chunks from chunkable."""
    for idx in range(0, len(chunkable), n):
        yield chunkable[idx:idx+n]


def pad_to_multiple(string, multiple):
    length = len(string)
    if length % multiple != 0:
        string.extend(['0'] * (multiple - (length % multiple)))
    return string

from .util import pad_to_width, lpop


def build_checkerboard(passphrase, c):
    passphrase = passphrase[0:10]
    if passphrase.count(' ') != 2:
        return None

    alphabet = list(map(chr, range(65, 91)))
    alphabet += ['.', '/']

    remaining_alpha = list(filter(lambda x: x not in passphrase, alphabet))

    layer_one = passphrase
    layer_two = remaining_alpha[0:10]
    layer_three = remaining_alpha[10:20]
    holes = []

    lookup_table = {}
    for i, char in enumerate(layer_one):
        if char == ' ':
            holes.append(str((int(c[i]) * 10)))
        else:
            lookup_table[char] = c[i]

    for beginning, layer in zip(holes, [layer_two, layer_three]):
        for i, char in enumerate(layer):
            lookup_table[char] = str(int(beginning) + int(c[i]))

    return lookup_table


def build_inverted_checkerboard(passphrase, c):
    checkerboard = build_checkerboard(passphrase, c)
    inverted_checkerboard = {}

    holes = []
    for key, value in checkerboard.items():
        inverted_checkerboard[value] = key

        if len(value) == 2:
            if value[0] not in holes:
                holes.append(value[0])

    inverted_checkerboard['holes'] = holes

    return inverted_checkerboard


def lookup(xs, table):
    res = []
    for x in xs:
        for key, value in table.items():
            if key == x:
                if int(value) < 9:
                    res.append(value)
                else:
                    res += list(value)

    return pad_to_width(res, '0', 5)


def inverted_lookup(xs, table):
    res = []
    while xs:
        x, xs = lpop(xs)

        if x in table['holes']:
            prefix = x
            x, xs = lpop(xs)
            x = prefix + x

        res.append(table[x])

    return res

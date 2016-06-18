def invert_index(xs):
    def _helper(x):
        if x[1] == 0:
            return 10
        else:
            return x[1]

    xs = sorted(enumerate(xs), key=_helper)
    return [x[0] for x in xs]


def lpop(a):
    x = a[:1][0]
    xs = a[1:]
    return (x, xs)


def group_by_n(x, n):
    res = []
    while x:
        res.append(x[0:n])
        x = x[n:]

    return res


def pad_to_width(xs, character, width):
    xs_len = len(xs)
    if xs_len % width != 0:
        xs += [character] * (width - xs_len % width)

    return xs


def sequentialize(xs):
    xs = list(xs)
    unique_xs = sorted(set(sorted(xs)))
    if 0 in unique_xs:
        _, unique_xs = lpop(unique_xs)
        unique_xs.append(0)

    i = 1
    res = [None] * len(xs)
    for current_x in unique_xs:
        for index, x in enumerate(xs):
            if x == current_x:
                res[index] = i
                i += 1

    return res

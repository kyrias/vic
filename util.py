def invert_index(xs):
    def _helper(x):
        if x[1] == 0:
            return 10
        else:
            return x[1]

    xs = sorted(enumerate(xs), key=_helper)
    return [x[0] for x in xs]


def split_digits(x):
    res = []

    while x > 9:
        res.append(x % 10)
        x = x // 10

    res.append(x)

    return list(reversed(res))


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


def pad_to_length(xs, character, width):
    xs_len = len(xs)
    if xs_len % width != 0:
        xs += [character] * (width - xs_len % width)

    return xs


def pad_message(xs):
    xs_len = len(xs)
    if xs_len % 5 != 0:
        xs += ['0'] * (5 - xs_len % 5)

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


def mod_add(x, y):
    return (x + y) % 10


def mod_adds(xs, ys):
    return [ mod_add(x, y) for x, y in zip(xs, ys)]


def wrap_sub(x, y):
    return (10 + (x - y)) % 10


def wrap_subs(xs, ys):
    return [ wrap_sub(x, y) for x, y in zip(xs, ys) ]


def chain_add(xs, expand_by, done=[]):
    xs = xs[::1]
    if expand_by == 0:
        return done + xs

    x, xs = lpop(xs)
    xs.append(mod_add(x, xs[0]))
    done.append(x)

    return chain_add(xs, expand_by - 1, done)


def pa(a):
    for row in a:
        print('\t'.join([str(x) for x in row]))

from .util import lpop


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

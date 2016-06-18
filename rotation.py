def rotate_right(a):
    rev = a[::-1]
    zipped = list(zip(*rev))
    return zipped


def rotate_left(a):
    zipped = list(zip(*a))
    rev = zipped[::-1]
    return rev

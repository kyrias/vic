def rotate_left(a):
    zipped = list(zip(*a))
    rev = zipped[::-1]
    return rev

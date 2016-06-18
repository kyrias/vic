from .util import sequentialize
from .rotation import rotate_left
from .arithmetic import wrap_subs, mod_adds, chain_add


def derive_s(passphrase):
    i_one = passphrase[0:10]
    i_two = passphrase[10:20]

    return (list(map(str, [x % 10 for x in sequentialize(i_one)])),
            list(map(str, [x % 10 for x in sequentialize(i_two)])))


def derive_g(message_id, date, s_one):
    mid = map(int, list(message_id))
    date = map(int, list(date))
    s_one = map(int, s_one)
    temp = wrap_subs(mid, date)

    expanded = chain_add(temp, 5)
    g = mod_adds(expanded, s_one)

    return g


def derive_t(g, s_two):
    t = []
    for digit in g:
        t.append(s_two[digit - 1])

    return t


def derive_u(t):
    t = list(map(int, t))
    u = chain_add(t, 50, done=[])[10:]

    return list(map(str, u))


def derive_w(pid, u):
    pid = int(pid)
    u = u[::1]
    u_w_two = u.pop()

    u_w_one = u.pop()
    while u_w_two == u_w_one:
        u_w_one = u.pop()

    w_one, w_two = map(lambda x: str(pid + int(x)), [u_w_one, u_w_two])

    return (w_one, w_two)


def derive_k(t, u, w_one, w_two):
    w_one = int(w_one)
    w_two = int(w_two)

    seqT = sequentialize(t)

    d_u = []
    while u:
        line = u[:10]
        if len(line) < 10:
            line += [None] * (10 - len(line))
        u = u[10:]

        d_u.append(line)

    u_left = rotate_left(d_u)

    res = []
    for i in range(1, 11):
        index = list.index(seqT, i)
        res.append( u_left[ -(index + 1) ] )

    res_two = []
    for row in res:
        for digit in row:
            if digit is not None:
                res_two.append(int(digit))

    U_k_one = res_two[:w_one]
    res_two = res_two[w_one:]
    U_k_two = res_two[:w_two]

    k_one = list(map(str, sequentialize(U_k_one)))
    k_two = list(map(str, sequentialize(U_k_two)))

    return k_one, k_two


def derive_c(u):
    last_row = u[-10:]
    sequentialized = sequentialize(map(int, last_row))
    modded = map(lambda x: x % 10, sequentialized)
    stringified = map(str, modded)

    return list(stringified)


def generate_ik(passphrase, message_id, date, personal_id):
    s_one, s_two = derive_s(passphrase)
    g = derive_g(message_id, date, s_one)
    t = derive_t(g, s_two)
    u = derive_u(t)

    width_one, width_two = derive_w(personal_id, u)
    key_one, key_two     = derive_k(t, u, width_one, width_two)
    checkerboard_header  = derive_c(u)

    return {
        'S1': s_one,
        'S2': s_two,
        'G': g,
        'T': t,
        'U': u,
        'width_one': width_one,
        'width_two': width_two,
        'key_one': key_one,
        'key_two': key_two,
        'checkerboard_header': checkerboard_header,
    }

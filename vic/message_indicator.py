from .util import group_by_n


def insert_message_indicator(ciphertext, mi, date):
    last_digit = int(date[-1])
    grouped = group_by_n(ciphertext, 5)
    grouped.insert(len(grouped) - (last_digit - 1), mi)

    return grouped


def pop_message_indicator(ciphertext, date):
    last_digit = int(date[-1])
    grouped = group_by_n(ciphertext, 5)
    mi = grouped.pop(len(grouped) - (last_digit))

    ungrouped = group_by_n(''.join(grouped), 1)

    return (mi, ungrouped)

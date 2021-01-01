import collections

full = '#'
empty = '.'

def parse(inp):
    lines = inp.splitlines()

    init = lines[0][15:]
    rules = {}

    for line in lines[2:]:
        front, back = line.split(' => ')
        rules[front] = back
    return init, rules

def print_pots(pots):
    a, b = min(pots), max(pots)
    row = []
    for pos in range(a, b+1):
        row.append(full if pos in pots else empty)
    print(''.join(row))


def generation(pots, rules):
    new_pots = set()
    a, b = min(pots), max(pots)
    for pos in range(a-5, b+5):
        frame = ''.join(full if pos+i in pots else empty
                            for i in range(-2,3))
        if rules.get(frame) == full:
            new_pots.add(pos)
    return new_pots


def part1(inp):
    init, rules = parse(inp)

    pots = set(pos for pos, pot in enumerate(init) if pot=='#')
    for g in range(20):
        pots = generation(pots, rules)
    return sum(pots)

def part2(inp):
    init, rules = parse(inp)

    pots = set(pos for pos, pot in enumerate(init) if pot=='#')

    # After a chaotic start the growth becomes linear
    i = 0
    prev_sum = 0
    prev_delta = 0
    while True:
        pots = generation(pots, rules)
        curr_sum = sum(pots)
        delta = curr_sum - prev_sum
        if delta == prev_delta:
            break

        prev_delta = delta
        prev_sum = curr_sum
        i += 1

    total = (50_000_000_000 - i)*prev_delta + prev_sum
    return total


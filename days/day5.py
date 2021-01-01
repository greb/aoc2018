def react(poly):
    new = []
    check = lambda x,y: abs(ord(x) - ord(y)) == 32
    for u in poly:
        if new and check(u, new[-1]):
            new.pop()
        else:
            new.append(u)
    return len(new)

def part1(inp):
    poly = inp.strip()
    return react(poly)

def part2(inp):
    poly = inp.strip()
    units = set(u.lower() for u in poly)

    lengths = []
    for u in units:
        new_poly = poly.replace(u, '').replace(u.upper(), '')
        lengths.append(react(new_poly))
    return min(lengths)

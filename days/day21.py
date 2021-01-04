def parse(inp):
    lines = inp.splitlines()
    magic_number = int(lines[8].split()[1])
    return magic_number

def mystery_function(magic_number):
    # Again, some dissasebly was required
    r3 = 0
    while True:
        r1 = r3 | 0x10000
        r3 = magic_number

        while True:
            r3 += r1 & 0xff
            r3 &= 0xffffff
            r3 *= 0x1016b
            r3 &= 0xffffff

            if 0x100 > r1:
                yield r3
                break
            else:
                # WTF r4! Are you drunk?
                r1 //= 0x100


def part1(inp):
    magic_number = parse(inp)
    mystery = mystery_function(magic_number)
    return next(mystery)

def part2(inp):
    magic_number = parse(inp)
    mystery = mystery_function(magic_number)

    seen = set()
    while True:
        nxt = next(mystery)
        if nxt in seen:
            break
        last = nxt
        seen.add(nxt)

    return last


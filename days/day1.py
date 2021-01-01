import itertools

def part1(inp):
    return sum(int(n) for n in inp.splitlines())

def part2(inp):
    nums = [int(n) for n in inp.splitlines()]

    history = set()
    s = 0
    for n in itertools.cycle(nums):
        s += n
        if s in history:
            break
        history.add(s)
    return s

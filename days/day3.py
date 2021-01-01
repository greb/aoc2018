import re
import collections

def parse(inp):
    pattern = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')
    claims = []
    for line in inp.splitlines():
        claim = [int(v) for v in pattern.match(line).groups()]
        claims.append(claim)
    return claims

def part1(inp):
    claims = parse(inp)

    fabric = collections.defaultdict(int)
    for _, x,y,w,h in claims:
        for xd in range(w):
            for yd in range(h):
                pos = x+xd, y+yd
                fabric[pos] += 1

    cnt = 0
    for v in fabric.values():
        if v >= 2:
            cnt += 1
    return cnt


def part2(inp):
    claims = parse(inp)

    fabric = collections.defaultdict(int)
    for _, x,y,w,h in claims:
        for xd in range(w):
            for yd in range(h):
                pos = x+xd, y+yd
                fabric[pos] += 1

    for claim_id, x,y,w,h in claims:
        cnt = 0
        for xd in range(w):
            for yd in range(h):
                pos = x+xd, y+yd
                if fabric[pos] > 1:
                    cnt += 1
        if cnt == 0:
            break
    return claim_id

import heapq
import itertools
import re

import pdb

def manhatten(pos0, pos1):
    return sum(abs(v0-v1) for v0,v1 in zip(pos0, pos1))

def parse(inp):
    bots = []
    for line in inp.splitlines():
        params = list(map(int, re.findall(r'-?\d+', line)))
        bots.append((params[:3], params[3]))
    return bots

def part1(inp):
    bots = parse(inp)
    m_bot, m_r = max(bots, key=lambda x:x[1])

    cnt = 0
    for bot, _ in bots:
        if manhatten(m_bot, bot) <= m_r:
            cnt += 1
    return cnt


def intersect(box, size, bots):
    size //= 2
    cnt = 0
    for bot, r in bots:
        dist = 0
        for b,p in zip(box, bot):
            dist += abs(b+size - p) - size
        if dist <= r:
            cnt += 1
    return cnt

def split_box(box, size):
    size //= 2
    for delta in itertools.product([0,1], repeat=3):
        n_box = [b+d*size for b,d in zip(box, delta)]
        yield tuple(n_box), size

def find_bounding_box(bots):
    size = 1
    cnt = 0
    while True:
        box = [-size//2 for _ in range(3)]
        cnt = intersect(box, size, bots)
        if cnt == len(bots):
            break
        size *= 2
    return box, size


def part2(inp):
    bots = parse(inp)
    box, size = find_bounding_box(bots)

    origin = (0,0,0)
    queue = [(-len(bots), -size, 0, box)]
    while queue:
        canidate = heapq.heappop(queue)
        _, neg_size, _, box = canidate
        if neg_size == 0:
            break

        for n_box, n_size in split_box(box, -neg_size):
            cnt = intersect(n_box, n_size, bots)
            dist = manhatten(origin, n_box)
            canidate = -cnt, -n_size, dist, n_box
            heapq.heappush(queue, canidate)
    return dist

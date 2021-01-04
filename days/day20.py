from collections import defaultdict

dirs = {
    'N': (0, -1),
    'E': (1, 0),
    'S': (0, 1),
    'W': (-1, 0),
}

def move(pos, dir):
    x,y = pos
    dx,dy = dirs[dir]
    return dx+x, dy+y


def walk_maze(regex):
    pos = (0,0)
    stack = []

    prev = pos
    dists = {pos: 0}

    for c in regex:
        if c == '(':
            stack.append(pos)
        elif c == ')':
            pos = stack.pop()
        elif c == '|':
            pos = stack[-1]
        else:
            pos = move(pos, c)
            new_dist = dists[prev]+1
            if pos not in dists or new_dist < dists[pos]:
                dists[pos] = new_dist
        prev = pos
    return dists

def part1(inp):
    dists = walk_maze(inp.strip()[1:-1])
    return max(dists.values())


def part2(inp):
    dists = walk_maze(inp.strip()[1:-1])
    return len([v for v in dists.values() if v >= 1000])

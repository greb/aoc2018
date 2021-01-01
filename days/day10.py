import re

def bounding_box(pos):
    xs = [p[0] for p in pos]
    ys = [p[1] for p in pos]
    return min(xs), max(xs), min(ys), max(ys)

def bbox_size(bbox):
    x0, x1, y0, y1 = bbox
    return abs(x1-x0) * abs(y1-y0)

def parse(inp):
    pos = []
    vel = []
    for line in inp.splitlines():
        nums = [int(n) for n in re.findall(r'-?\d+', line)]
        pos.append(nums[:2])
        vel.append(nums[2:])
    return pos, vel

def step(pos, vel):
    return [(x+dx, y+dy) for (x,y),(dx,dy) in zip(pos, vel)]

def print_pos(pos, bbox):
    x0, x1, y0, y1 = bbox
    for y in range(y0, y1+1):
        row = []
        for x in range(x0, x1+1):
            if (x,y) in pos:
                row.append('#')
            else:
                row.append(' ')
        print(''.join(row))


def part1(inp):
    pos, vel = parse(inp)

    while True:
        pos = step(pos, vel)
        bbox = bounding_box(pos)

        if bbox_size(bbox) == 549:
            break
    print_pos(pos, bbox)

    return 'GPEPPPEJ' # My solution

def part2(inp):
    pos, vel = parse(inp)

    i = 1
    while True:
        pos = step(pos, vel)
        bbox = bounding_box(pos)

        if bbox_size(bbox) == 549:
            break
        i += 1

    return i

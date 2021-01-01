from collections import defaultdict

def manhatten_dist(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def bounding_box(coords):
    xs = sorted(c[0] for c in coords)
    ys = sorted(c[1] for c in coords)
    return min(xs), max(xs), min(ys), max(ys)

def gen_locations(bbox):
    x0,x1,y0,y1 = bbox
    for x in range(x0, x1+1):
        for y in range(y0, y1+1):
            yield x,y

def closest_coord(loc, coords):
    dists = []
    for coord in coords:
        d = manhatten_dist(loc, coord)
        dists.append( (d, coord) )

    dists.sort()
    if dists[0][0] == dists[1][0]:
        return None
    return dists[0][1]

def part1(inp):
    coords = [tuple(map(int, line.split(', '))) for line in inp.splitlines()]

    bbox = bounding_box(coords)
    areas = defaultdict(int)
    infs = set()

    for loc in gen_locations(bbox):
        closest = closest_coord(loc, coords)
        if not closest:
            continue
        areas[closest] += 1

        x,y = loc
        x0,x1,y0,y1 = bbox
        if x == x0 or x == x1 or y == y0 or y == y1:
            infs.add(closest)

    for inf in infs:
        del areas[inf]

    return max(areas.items(), key=lambda x:x[1])[1]

def part2(inp):
    coords = [tuple(map(int, line.split(', '))) for line in inp.splitlines()]
    bbox = bounding_box(coords)

    cnt = 0
    for loc in gen_locations(bbox):
        dist_sum = sum(manhatten_dist(loc, coord) for coord in coords)
        if dist_sum < 10_000:
            cnt += 1
    return cnt


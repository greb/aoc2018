import collections

def manhatten(pa, pb):
    return sum(abs(a-b) for a,b in zip(pa,pb))

def part1(inp):
    coords = [tuple(int(n) for n in line.split(','))
            for line in inp.splitlines()]

    neighbors = collections.defaultdict(set)
    for i, src in enumerate(coords):
        for dst in coords[i:]:
            if manhatten(src, dst) <= 3:
                neighbors[src].add(dst)
                neighbors[dst].add(src)
    
    n_const = 0
    coords = set(coords)
    while coords:
        n_const += 1
        stack = [coords.pop()]
        while stack:
            curr = stack.pop()
            coords.discard(curr)

            for n in neighbors[curr]:
                if n in coords:
                    stack.append(n)

    return n_const

import re

def parse(inp):
    clay = []
    pattern = re.compile(r'([xy])=(\d+), [xy]=(\d+)..(\d+)')
    for line in inp.splitlines():
        match = pattern.match(line)
        clay.append(match.groups())
    return clay

def build(clay):
    tiles = dict()

    for dim, *args in clay:
        a, b0, b1 = map(int, args)
        for b in range(b0, b1+1):
            pos = (a,b) if dim=='x' else (b,a)
            tiles[pos] = '#'
    top = min(t[1] for t in tiles)
    bottom = max(t[1] for t in tiles)
    return tiles, top, bottom

def print_tiles(tiles):
    x0 = min(t[0] for t in tiles)
    x1 = max(t[0] for t in tiles)
    y0 = min(t[1] for t in tiles)
    y1 = max(t[1] for t in tiles)

    for y in range(y0, y1+1):
        row = []
        for x in range(x0, x1+1):
            row.append(tiles.get((x,y), '.'))
        print(''.join(row))
    print(x0, x1, y0, y1)

def check_overflow(x, y, dir, tiles, sources):
    while True:
        below = tiles.get((x,y+1))
        curr  = tiles.get((x,y))

        if not below:
            sources.append((x,y))
            return x, True
        elif curr == '#':
            return x-dir, False
        elif curr == '|' and below == '|':
            return x, True
        x += dir

def fill(source, bottom, tiles):
    sources = [source]

    while sources:
        x,y = sources.pop()
        if tiles.get((x,y)) == '~':
            continue

        y += 1
        while y <= bottom:
            tile = tiles.get((x,y))
            if not tile:
                tiles[(x,y)] = '|'
                y += 1
            elif tile == '#' or tile == '~':
                y -= 1
                left, over_left = check_overflow(x, y, -1, tiles, sources)
                right, over_right = check_overflow(x, y, 1, tiles, sources)
                overflow = over_left or over_right
                for tx in range(left, right+1):
                    tiles[(tx,y)] = '|' if overflow else '~'
            elif tile == '|':
                break

def part1(inp):
    clay = parse(inp)
    tiles, top, bottom = build(clay)

    source = (500, 0)
    fill(source, bottom, tiles)

    # Fuck, reading fucking helps! The y should be limited
    return sum(t in '|~' for (_,y),t in tiles.items() if top <= y)

def part2(inp):
    clay = parse(inp)
    tiles, top, bottom = build(clay)

    source = (500, 0)
    fill(source, bottom, tiles)

    return sum(t == '~' for (_,y),t in tiles.items() if top <= y)

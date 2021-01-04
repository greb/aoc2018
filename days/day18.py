import collections

t_open = '.'
t_tree = '|'
t_lumb = '#'

def neighbors(x,y, size):
    adjecant = [(x+1,y), (x+1,y+1), (x,y+1), (x-1,y+1),
                (x-1,y), (x-1,y-1), (x,y-1), (x+1,y-1)]
    for ax, ay in adjecant:
        if 0 <= ax < size and 0 <= ay < size:
            yield ax, ay

def count_adjecant(x,y, grid, size):
    cnt = collections.defaultdict(int)
    for nx,ny in neighbors(x,y, size):
        tile = grid[ny][nx]
        cnt[tile] += 1
    return cnt

def step(grid):
    size = len(grid)
    new_grid = []
    for y, row in enumerate(grid):
        new_row = []
        for x, tile in enumerate(row):
            cnt = count_adjecant(x,y, grid, size)
            if tile == t_open and cnt[t_tree] >= 3:
                new_row.append(t_tree)
            elif tile == t_tree and cnt[t_lumb] >= 3:
                new_row.append(t_lumb)
            elif tile == t_lumb and not (cnt[t_lumb] >= 1 and cnt[t_tree] >= 1):
                new_row.append(t_open)
            else:
                new_row.append(tile)
        new_grid.append(''.join(new_row))
    return tuple(new_grid)

def print_grid(grid):
    for row in grid:
        print(row)
    print()

def count_grid(grid):
    cnt = collections.defaultdict(int)
    for row in grid:
        for tile in row:
            cnt[tile] += 1
    return cnt


def part1(inp):
    grid = tuple(line for line in inp.splitlines())

    for x in range(10):
        grid = step(grid)

    cnt = count_grid(grid)
    return cnt[t_tree] * cnt[t_lumb]


def part2(inp):
    grid = tuple(line for line in inp.splitlines())

    history = dict()
    i = 0
    while grid not in history:
        history[grid] = i
        grid = step(grid)
        i += 1

    # The grid has become periodic
    start = history[grid]
    period = i - start
    rest = (1_000_000_000 - start) % period

    for x in range(rest):
        grid = step(grid)

    cnt = count_grid(grid)
    return cnt[t_tree] * cnt[t_lumb]



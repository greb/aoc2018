def power_lvl(x,y, grid_serial):
    rack = x+10
    power = (y*rack + grid_serial) * rack
    power = (power//100) % 10
    return power-5

size = 300
def make_grid(grid_serial):
    # Using partial sums to speed up part2
    # https://en.wikipedia.org/wiki/Summed-area_table
    grid = [[0 for _ in range(size+1)] for _ in range(size+1)]
    for y in range(1,size+1):
        row = []
        for x in range(1, size+1):
            power = power_lvl(x, y, grid_serial)
            power += grid[y-1][x] + grid[y][x-1] - grid[y-1][x-1]
            grid[y][x] = power
    return grid

def find_best_cell(grid, n=3):
    best_cell = None
    best_val  = None

    for y in range(n, size+1):
        for x in range(n, size+1):
            val = grid[y][x] - grid[y-n][x] - grid[y][x-n] + grid[y-n][x-n]
            if best_val is None or val > best_val:
                best_val = val
                best_cell = (x-n+1,y-n+1)
    return best_cell, best_val

def part1(inp):
    grid_serial = int(inp.strip())
    grid = make_grid(grid_serial)
    best_cell, _ = find_best_cell(grid)
    return ','.join(map(str, best_cell))

def part2(inp):
    grid_serial = int(inp.strip())
    grid = make_grid(grid_serial)

    vals = []
    for n in range(3, 301):
        cell, val = find_best_cell(grid, n)
        print(val, cell, n)
        vals.append((val, cell, n))
    best =  max(vals)
    print(best)

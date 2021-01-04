import collections
import heapq

Region = collections.namedtuple('Region',
        ['geo_idx', 'ero_lvl', 'reg_type'])

def parse(inp):
    lines = inp.splitlines()
    depth = int(lines[0].split()[1])
    target = tuple(map(int, lines[1].split()[1].split(',')))
    return depth, target


class Maze:
    valid_gear = {
        0: set(['climb', 'torch']),
        1: set(['climb', 'empty']),
        2: set(['torch', 'empty'])
    }

    def __init__(self, depth, target):
        self.depth = depth
        self.target = target
        self.regions = {}

    def add_region(self, pos):
        x,y = pos
        if pos == (0,0) or pos == self.target:
            geo_idx = 0
        elif y == 0:
            geo_idx = x*16807
        elif x == 0:
            geo_idx = y*48271
        else:
            geo_idx = self[(x,y-1)].ero_lvl * self[(x-1, y)].ero_lvl

        ero_lvl = (geo_idx+self.depth) % 20183
        reg_type = ero_lvl % 3
        self.regions[pos] = Region(geo_idx, ero_lvl, reg_type)

    def __getitem__(self, pos):
        if pos in self.regions:
            return self.regions[pos]
        return self.gen_regions(pos)

    def gen_regions(self, pos):
        rx,ry = pos
        stack = []
        for x in range(rx, -1, -1):
            if (x, ry) in self.regions:
                break
            for y in range(ry, -1, -1):
                if (x, y) in self.regions:
                    break
                stack.append((x,y))

        while stack:
            pos = stack.pop()
            self.add_region(pos)
        return self.regions[pos]

    def risk_level(self):
        score = 0
        tx, ty = self.target
        for x in range(tx+1):
            for y in range(ty+1):
                score += self[(x,y)].reg_type
        return score

    def valid_moves(self, pos, gear):
        x,y = pos
        reg = self[pos].reg_type

        neighbors = [(x+1,y),(x, y+1),(x-1,y),(x,y-1)]
        for n_pos in neighbors:
            if n_pos[0] < 0 or n_pos[1] < 0:
                continue

            n_reg = self[n_pos].reg_type
            valid_gear = self.valid_gear[reg] & self.valid_gear[n_reg]
            for n_gear in valid_gear:
                if n_pos == self.target and n_gear != 'torch':
                    continue
                cost = 8 if gear != n_gear else 1
                yield cost, (n_pos, n_gear)

    def search_path(self):
        curr= (0,0), 'torch'

        distances = dict()
        distances[curr] = 0
        queue = [(0, curr)]
        prev = {curr: None}

        while queue:
            dist, curr = heapq.heappop(queue)
            pos, gear = curr
            if pos == self.target:
                return dist

            if dist > distances[curr]:
                continue

            for cost, move in self.valid_moves(pos, gear):
                new_dist = dist + cost
                if move not in distances or distances[move] > new_dist:
                    distances[move] = new_dist
                    prev[move] = curr
                    heapq.heappush(queue, (new_dist, move))


def part1(inp):
    depth, target = parse(inp)
    maze = Maze(depth, target)
    return maze.risk_level()


def part2(inp):
    depth, target = parse(inp)
    maze = Maze(depth, target)
    return maze.search_path()

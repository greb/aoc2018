import collections

# By using y,x coordinates we always prefer the items in reading order
def neighbors(pos):
    y,x = pos
    dirs = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    for dy, dx in dirs:
        yield y+dy, x+dx

class Unit:
    def __init__(self, pos, team):
        self.pos = pos
        self.team = team
        self.alive = True
        self.hp = 200

    def __eq__(self, other):
        return self.pos == other.pos

    def __repr__(self):
        if self.alive:
            return f'<Unit {self.team} @ {self.pos} hp={self.hp}>'

        return f'<Unit {self.team} @ {self.pos} DEAD>'


class Grid:
    def __init__(self, inp, elf_power=3):
        self.walls = set()
        self.units = []
        self.elf_power = elf_power

        for y, row in enumerate(inp.splitlines()):
            for x, tile in enumerate(row):
                if tile == '#':
                    self.walls.add((y,x))
                elif tile in 'EG':
                    self.units.append(Unit((y,x), tile))
        self.w, self.h = x+1, y+1


    def round(self, check_elf_dead=False):
        for unit in sorted(self.units, key=lambda unit: unit.pos):
            if not unit.alive:
                continue

            targets = self.find_targets(unit)
            if not targets:
                return unit.team

            in_range = self.find_in_range(unit, targets)
            if not unit.pos in in_range:
                self.move_unit(unit, in_range)

            elf_dead = self.attack_targets(unit, targets)
            if check_elf_dead and elf_dead:
                return 'G'


    def attack_targets(self, unit, targets):
        targets = [target for target in targets
                if target.pos in neighbors(unit.pos)]
        if not targets:
            return

        target = min(targets, key=lambda u: (u.hp, u.pos))
        ap = self.elf_power if unit.team == 'E' else 3

        target.hp -= ap
        if target.hp <= 0:
            target.alive = False
            if target.team == 'E':
                return True
        return False


    def move_unit(self, unit, in_range):
        dists, prev = self.find_distances(unit.pos)
        reachable = [(d,pos) for pos,d in dists.items()
                if pos in in_range]
        if not reachable:
            return

        dist, pos = min(reachable)
        while prev[pos] != unit.pos:
            pos = prev[pos]
        unit.pos = pos

    def find_targets(self, unit):
        return [other for other in self.units
                if unit.team != other.team and other.alive]

    def find_in_range(self, unit, targets):
        adjecant = set(neigh for target in targets
                for neigh in neighbors(target.pos))
        occupied = set(other.pos for other in self.units
                if other != unit and other.alive)
        return adjecant - self.walls - occupied

    def find_distances(self, pos):
        occupied = set(unit.pos for unit in self.units if unit.alive)

        dists = {pos: 0}
        prev = {pos: None}

        visited = set()
        visited.add(pos)

        queue = collections.deque([(0, pos)])
        while queue:
            dist, pos = queue.pop()

            for n in neighbors(pos):
                if n in self.walls or n in occupied or n in visited:
                    continue

                new_dist = dist + 1
                dists[n] = new_dist
                prev[n] = pos
                visited.add(n)

                queue.appendleft((new_dist, n))

        return dists, prev

    def print(self):
        units = {unit.pos: unit for unit in self.units}
        for y in range(self.h):
            map_row = []
            unit_row = []
            for x in range(self.w):
                pos = y,x
                unit = units.get(pos)

                if pos in self.walls:
                    map_row.append('#')
                elif unit and unit.alive:
                    map_row.append(unit.team)
                    unit_row.append(f'{unit.team}({unit.hp})')
                else:
                    map_row.append('.')
            map_row = ''.join(map_row)
            unit_row = ', '.join(unit_row)
            print(f'{map_row}    {unit_row}')

def part1(inp):
    grid = Grid(inp)

    cnt_round = 0
    while True:
        winner = grid.round()
        if winner:
            break
        cnt_round += 1

    winner_score = sum(unit.hp for unit in grid.units if unit.alive)
    return winner_score * cnt_round

def part2(inp):

    elf_power = 4
    while True:
        grid = Grid(inp, elf_power)

        cnt_round = 0
        while True:
            winner = grid.round(check_elf_dead=True)
            if winner:
                break
            cnt_round += 1

        if winner == 'E':
            break
        else:
            elf_power += 1

    winner_score = sum(unit.hp for unit in grid.units if unit.alive)
    return winner_score * cnt_round

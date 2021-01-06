import pdb
import copy

class Group:
    def __init__(self, team, id, line):
        self.team = team
        self.id = id
        self.parse(line)

    def parse(self, line):
        words = line.split()
        self.units       = int(words[0])
        self.hp          = int(words[4])
        self.weak        = Group.parse_attr(line, 'weak')
        self.immune      = Group.parse_attr(line, 'immune')
        self.ap          = int(words[-6])
        self.attack      = words[-5]
        self.initiative  = int(words[-1])

    def __repr__(self):
        return f'<Group team={self.team}, id={self.id}, units={self.units}>'

    @staticmethod
    def parse_attr(line, attr):
        s = f'{attr} to '
        start = line.find(s)
        if start < 0:
            return []

        start += len(s)
        end = line.find(';', start)
        if end < 0:
            end = line.find(')', start)
        return set(line[start:end].split(', '))

    def __hash__(self):
        return hash((self.team, self.id))

    def power(self):
        return self.units * self.ap

    def damage(self, attacker):
        if attacker.attack in self.immune:
            return 0

        power = attacker.power()
        if attacker.attack in self.weak:
            power *= 2
        return power


def parse(inp):
    groups = []
    armies = inp.split('\n\n')
    for team_id, army in enumerate(armies):
        lines = army.splitlines()[1:]
        for group_id, line in enumerate(lines):
            group = Group(team_id, group_id, line)
            groups.append(group)
    return groups


def fight_round(groups):
    selections = []
    chosen = set()
    n_kills = 0

    att_key = lambda a: (-a.power(), -a.initiative)
    for att in sorted(groups, key=att_key):

        def_key = lambda d: (-d.damage(att), -d.power(), -d.initiative)
        defs = [d for d in groups if d.team != att.team
                and d not in chosen and d.damage(att) > 0]

        defs = sorted(defs, key=def_key)
        if defs:
            selections.append((att, defs[0]))
            chosen.add(defs[0])

    sel_key = lambda s: s[0].initiative
    for a, d in sorted(selections, key=sel_key, reverse=True):
        damage = d.damage(a)
        killed = min(d.units, damage // d.hp)
        d.units -= killed
        n_kills += killed

    groups = [g for g in groups if g.units > 0]
    return n_kills, groups

def battle(groups):
    while True:
        n_kills, groups = fight_round(groups)
        team0 = sum([g.units for g in groups if g.team==0])
        team1 = sum([g.units for g in groups if g.team==1])

        if n_kills == 0:
            return 1, team1

        if team0 == 0:
            return 1, team1
        if team1 == 0:
            return 0, team0

def part1(inp):
    groups = parse(inp)
    return battle(groups)[1]


def part2(inp):
    groups = parse(inp)

    boost = 1
    while True:
        boost_groups = copy.deepcopy(groups)

        for group in boost_groups:
            if group.team == 0:
                group.ap += boost

        winner, score = battle(boost_groups)
        if winner == 0:
            return score
        boost += 1


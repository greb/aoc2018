import collections
import re

class Node:
    def __init__(self, value):
        self.value = value
        self.n_next = None
        self.n_prev  = None

    def insert_next(self, value):
        node = Node(value)
        node.n_next, node.n_prev = self.n_next, self
        self.n_next.n_prev, self.n_next = node, node
        return node

    def remove(self):
        self.n_next.n_prev = self.n_prev
        self.n_prev.n_next = self.n_next
        return self.value

    def to_list(self):
        lst = []
        node = self
        lst.append(node.value)
        while node.n_next is not self:
            node = node.n_next
            lst.append(node.value)
        return lst


def parse(inp):
    return map(int, re.findall(r'\d+', inp))

def play_game(n_players, n_rounds):
    current = Node(0)
    current.n_next = current
    current.n_prev = current
    players = collections.defaultdict(int)

    for n in range(n_rounds):
        player = n % n_players
        marble = n+1

        if marble % 23 == 0:
            players[player] += marble
            node = current
            for _ in range(7):
                node = node.n_prev
            players[player] += node.remove()
            current = node.n_next
        else:
            current = current.n_next.insert_next(marble)
    return max(players.values())

def part1(inp):
    n_players, n_rounds = parse(inp)
    return play_game(n_players, n_rounds)

def part2(inp):
    n_players, n_rounds = parse(inp)
    return play_game(n_players, n_rounds*100)


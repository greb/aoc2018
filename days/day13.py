import collections
import operator

class Cart:
    dirs = {
        '^': (-1, 0),
        '>': (0, 1),
        'v': (1, 0),
        '<': (0, -1)
    }
    turn_r = {'^':'>', '>':'v', 'v':'<', '<':'^'}
    turn_l = {'^':'<', '>':'^', 'v':'>', '<':'v'}
    reflect_r = {'^':'>', '>':'^', 'v':'<', '<':'v'}
    reflect_l = {'^':'<', '>':'v', 'v':'>', '<':'^'}

    def __init__(self, cart_id, dir, pos):
        self.cart_id = cart_id
        self.dir = dir
        self.pos = pos
        self.cnt = 0

    def step(self, grid):
        y, x = self.pos
        tile = grid[y][x]
        assert tile != ' '

        self.decide(tile)
        self.forward()

    def decide(self, tile):
        if tile == '+':
            m = self.cnt % 3
            if m == 0:
                self.dir = Cart.turn_l[self.dir]
            elif m == 2:
                self.dir = Cart.turn_r[self.dir]
            self.cnt += 1
        elif tile == '/':
            self.dir = Cart.reflect_r[self.dir]
        elif tile == '\\':
            self.dir = Cart.reflect_l[self.dir]

    def forward(self):
        x, y = self.pos
        dx, dy = Cart.dirs[self.dir]
        self.pos = x+dx, y+dy

    def collision(self, other):
        return self.pos == other.pos

    def __repr__(self):
        return (f'<Cart id={self.cart_id}, dir={self.dir}, '
                   f'pos={self.pos}, cnt={self.cnt}>')

    def __eq__(self, other):
        return self.cart_id == other.cart_id

    def __hash__(self):
        return self.cart_id


def parse(inp):
    grid = []
    carts = set()
    cart_id = 0
    for y, row in enumerate(inp.splitlines()):
        row = list(row)
        for x, tile in enumerate(row):
            if tile in Cart.dirs:
                cart = Cart(cart_id, tile, (y,x))
                cart_id += 1
                carts.add(cart)

                if tile in '<>':
                    row[x] = '-'
                else:
                    row[x] = '|'
        grid.append(row)
    return grid, carts


def tick(grid, carts):
    collisions = []
    crashed = set()

    by_pos = operator.attrgetter('pos')
    for cart_a in sorted(carts, key=by_pos):
        cart_a.step(grid)

        for cart_b in carts:
            if cart_a == cart_b or cart_b in crashed:
                continue
            if cart_b.collision(cart_a):
                collisions.append(cart_b.pos)
                crashed.add(cart_a)
                crashed.add(cart_b)
                break

    carts -= crashed
    return collisions

def pos_to_str(pos):
    y,x = pos
    return f'{x},{y}'

def part1(inp):
    grid, carts = parse(inp)

    while True:
        collisions = tick(grid, carts)
        if collisions:
            break
    return pos_to_str(collisions[0])


def part2(inp):
    grid, carts = parse(inp)

    while True:
        tick(grid, carts)
        if len(carts) == 1:
            break

    last_cart = carts.pop()
    return pos_to_str(last_cart.pos)

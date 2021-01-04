import operator

opcodes = {
        'addr': (operator.add,  True,  True ),
        'addi': (operator.add,  True,  False),
        'mulr': (operator.mul,  True,  True ),
        'muli': (operator.mul,  True,  False),
        'banr': (operator.and_, True,  True ),
        'bani': (operator.and_, True,  False),
        'borr': (operator.or_,  True,  True ),
        'bori': (operator.or_,  True,  False),
        'setr': ('set',         True,  False),
        'seti': ('set',         False, False),
        'gtir': (operator.gt,   False, True ),
        'gtri': (operator.gt,   True,  False),
        'gtrr': (operator.gt,   True,  True ),
        'eqir': (operator.eq,   False, True ),
        'eqri': (operator.eq,   True,  False),
        'eqrr': (operator.eq,   True,  True )
}

class Device:
    def __init__(self, inp):
        self.regs = [0,0,0,0,0,0]

        lines = inp.splitlines()
        self.ip = int(lines[0][-1])

        self.code = []
        for line in lines[1:]:
            instr, *args = line.split()
            args = list(map(int, args))
            self.code.append([instr] + args)

    def step(self):
        ip = self.regs[self.ip]
        instr, a, b, c = self.code[ip]

        if instr not in opcodes:
            if instr == 'opt':
                self.optimized()
            self.regs[self.ip] += 1
            return

        func, reg_a, reg_b = opcodes[instr]
        if reg_a:
            a = self.regs[a]
        if reg_b:
            b = self.regs[b]

        if func == 'set':
            self.regs[c] = a
        else:
            self.regs[c] = int(func(a,b))

        self.regs[self.ip] += 1

    def run(self):
        while self.regs[self.ip] < len(self.code):
            self.step()

    def dump_code(self):
        with open('dump.txt', 'wt') as handle:
            for i, instr in enumerate(self.code):
                handle.write(f'{i:02d} {instr}\n')

    def debug(self):
        ip = self.regs[self.ip]
        print(f'ip={ip}: {self.code[ip]}')
        regs = [f'    {r}={v}' for r,v in zip('abcdef', self.regs)]
        print(', '.join(regs))


    def optimize_code(self):
        # Replace hot code with optimized function
        self.code[1][0] = 'opt'
        for i in range(2, 16):
            self.code[i][0] = 'nop'

    def optimized(self):
        val = self.regs[2]
        s = 0
        n = 1
        while n*n < val:
            d, m = divmod(val, n)
            if m == 0:
                s += d
                s += val//d
            n += 1
        self.regs[0] = s

def part1(inp):
    dev = Device(inp)
    dev.optimize_code()
    dev.run()
    return dev.regs[0]

def part2(inp):
    dev = Device(inp)
    dev.optimize_code()
    dev.regs[0] = 1
    dev.run()
    return dev.regs[0]

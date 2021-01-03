import operator
import collections

def parse(inp):
    first, second = inp.split('\n\n\n\n')
    samples = []
    for segment in first.split('\n\n'):
        lines = segment.splitlines()
        before = [int(n) for n in lines[0][9:-1].split(', ')]
        op = [int(n) for n in lines[1].split()]
        after = [int(n) for n in lines[2][9:-1].split(', ')]
        samples.append((before, op, after))
    instrs = []
    for line in second.splitlines():
        instrs.append([int(n) for n in line.split()])
    return samples, instrs

opcodes_decode = {
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

def check_reg(reg):
    return 0 <= reg < 4

def valid_opcodes(sample):
    valid = set()

    for opcode in opcodes_decode:
        func, reg_a, reg_b = opcodes_decode[opcode]

        regs = sample[0].copy()
        _, a, b, c = sample[1]
        after = sample[2]

        if reg_a:
            if not check_reg(a):
                continue
            a = regs[a]

        if reg_b:
            if not check_reg(b):
                continue
            b = regs[b]

        if not check_reg(c):
            continue

        if func == 'set':
            regs[c] = a
        else:
            regs[c] = int(func(a, b))

        if regs == after:
            valid.add(opcode)

    return valid

def find_opcode_mapping(samples):
    canidates = collections.defaultdict(lambda: opcodes_decode.keys())
    for sample in samples:
        opnum = sample[1][0]
        canidates[opnum] &= valid_opcodes(sample)

    mapping = dict()
    found = set()
    while len(mapping) < len(opcodes_decode):
        for opnum, opcodes in canidates.items():
            opcodes -= found
            if len(opcodes) == 1:
                opcode = opcodes.pop()
                mapping[opnum] = opcode
                found.add(opcode)
    return mapping


def part1(inp):
    samples, _ = parse(inp)

    cnt = 0
    for sample in samples:
        valid = valid_opcodes(sample)
        if len(valid) >= 3:
            cnt += 1
    return cnt


def part2(inp):
    samples, instrs = parse(inp)
    mapping = find_opcode_mapping(samples)

    regs = [0,0,0,0]
    for instr in instrs:
        opnum, a, b, c = instr
        func, reg_a, reg_b = opcodes_decode[mapping[opnum]]

        if reg_a:
            a = regs[a]
        if reg_b:
            b = regs[b]

        if func == 'set':
            regs[c] = a
        else:
            regs[c] = int(func(a,b))
    return regs[0]

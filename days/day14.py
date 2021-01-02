def part1(inp):
    n = int(inp.strip())
    recs = '37'
    elf_a, elf_b = 0, 1

    while len(recs) < n + 10:
        recs += str(int(recs[elf_a]) + int(recs[elf_b]))
        elf_a = (elf_a + int(recs[elf_a]) + 1) % len(recs)
        elf_b = (elf_b + int(recs[elf_b]) + 1) % len(recs)
    return recs[n:n+10]


def part2(inp):
    n = inp.strip()
    recs = '37'
    elf_a, elf_b = 0, 1

    l = len(n)+1
    while n not in recs[-l:]:
        recs += str(int(recs[elf_a]) + int(recs[elf_b]))
        elf_a = (elf_a + int(recs[elf_a]) + 1) % len(recs)
        elf_b = (elf_b + int(recs[elf_b]) + 1) % len(recs)
    return recs.index(n)

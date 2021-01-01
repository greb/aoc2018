import itertools

def part1(inp):
    boxes = inp.splitlines()

    cnt_doubles = 0
    cnt_tripples = 0

    for box in boxes:
        box = sorted(box)
        counts = [len(list(g)) for _, g in itertools.groupby(box)]

        if 2 in counts:
            cnt_doubles += 1
        if 3 in counts:
            cnt_tripples += 1

    return cnt_doubles * cnt_tripples


def part2(inp):
    boxes = inp.splitlines()

    for box_a, box_b in itertools.product(boxes, repeat=2):
        diffs = [i for i, (a,b) in enumerate(zip(box_a, box_b)) if a != b]
        if len(diffs) == 1:
            i = diffs[0]
            return box_a[:i] + box_a[i+1:]

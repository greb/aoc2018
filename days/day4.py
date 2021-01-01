import collections

def parse(inp):
    curr_shift = None
    shifts = []
    for line in sorted(inp.splitlines()):
        h, m = int(line[12:14]), int(line[15:17])
        event = line[19:].split()

        if event[0] == 'Guard':
            if curr_shift:
                shifts.append(curr_shift)
            if h != 0:
                m = 0
            guard = event[1]
            curr_shift = guard, []
        else:
            curr_shift[1].append(m)

    shifts.append(curr_shift)
    return shifts

def sleep_per_minute(shifts):
    guards = collections.defaultdict(lambda: [0]*60)
    for guard, events in shifts:
        for e in range(0, len(events), 2):
            sleep, wake = events[e:e+2]
            for i in range(sleep, wake):
                guards[guard][i] += 1
    return guards


def part1(inp):
    shifts = parse(inp)
    guards = sleep_per_minute(shifts)

    guard = max(guards, key=lambda k: sum(guards[k]))
    minute = max((s, m) for m,s in enumerate(guards[guard]))[1]
    return int(guard[1:]) * minute


def part2(inp):
    shifts = parse(inp)
    guards = sleep_per_minute(shifts)


    guard = max(guards, key=lambda k: max(guards[k]))
    minute = max((s, m) for m,s in enumerate(guards[guard]))[1]
    return int(guard[1:]) * minute

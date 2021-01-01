from collections import defaultdict

def parse(inp):
    plan = defaultdict(set)
    parts = set()

    for line in inp.splitlines():
        words = line.split()
        goal, req = words[7], words[1]
        plan[goal].add(req)
        parts.add(goal)
        parts.add(req)
    return plan, parts


def next_ready(plan, parts):
    ready = parts - plan.keys()
    if ready:
        ready = min(ready)
        parts.discard(ready)
        return ready

def update_plan(plan, ready):
    done = []
    for goal, reqs in plan.items():
        reqs.discard(ready)
        if not reqs:
            done.append(goal)
    for goal in done:
        del plan[goal]
    return ready


def part1(inp):
    plan, parts = parse(inp)

    buf = []
    while parts:
        ready = next_ready(plan, parts)
        update_plan(plan, ready)
        buf.append(ready)
    return ''.join(buf)


def part2(inp):
    plan, parts = parse(inp)

    t = 0
    workers = dict()
    while True:
        for w in range(5):
            wait, ready = workers.get(w, (0, None))
            if wait > 0:
                wait -= 1
            else:
                if ready:
                    update_plan(plan, ready)
                ready = next_ready(plan, parts)
                wait = 60 + (ord(ready)-ord('A')) if ready else 0
            workers[w] = wait, ready

        if all(not v[1] for v in workers.values()):
            break
        t += 1
    return t

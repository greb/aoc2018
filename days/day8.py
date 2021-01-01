import itertools

class Node:
    def __init__(self, children, metadata):
        self.children = children
        self.metadata = metadata

    def metadata_sum(self):
        s = sum(self.metadata)
        s += sum(c.metadata_sum() for c in self.children)
        return s

    def value(self):
        if not self.children:
            return sum(self.metadata)

        s = 0
        try:
            for m in self.metadata:
                if m > 0 and len(self.children) >= m:
                    s += self.children[m-1].value()
        except:
            import pdb; pdb.set_trace()
        return s


def build_tree(it):
    n_children = next(it)
    n_metadata = next(it)
    children = []
    for i in range(n_children):
        children.append(build_tree(it))
    metadata = list(itertools.islice(it, n_metadata))
    return Node(children, metadata)

def part1(inp):
    it = (int(n) for n in inp.strip().split())
    tree = build_tree(it)
    return tree.metadata_sum()

def part2(inp):
    it = (int(n) for n in inp.strip().split())
    tree = build_tree(it)
    return tree.value()

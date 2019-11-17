from anytree import NodeMixin
from aocd import data


class MyNode(NodeMixin):
    def __init__(self, parent=None):
        self.parent = parent

    @property
    def val(self):
        children = self.children
        if len(children) == 0:
            return sum(self.metas)
        else:
            total = 0
            for m in self.metas:
                try:
                    total += children[m - 1].val
                except IndexError:
                    pass
            return total


def part_ab(data):
    data = [int(x) for x in data.split()]
    sum_all_metas = 0
    node = root = MyNode()
    try:
        i = 0
        while data:
            if data[i] == 0:
                n_metas = data[i + 1]
                metas = data[i + 2 : i + 2 + n_metas]
                sum_all_metas += sum(metas)
                del data[i : i + 2 + n_metas]
                data[i - 2] -= 1
                i -= 2
                node.metas = metas
                node = node.parent
            else:
                i += 2
                node = MyNode(parent=node)
    except IndexError:
        assert node is root
        root.metas = metas
        part_a = sum_all_metas
        part_b = node.val
        return part_a, part_b


test_data = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"

test_a, test_b = part_ab(test_data)
assert test_a == 138
assert test_b == 66


a, b = part_ab(data)
print("part a:", a)
print("part b:", b)

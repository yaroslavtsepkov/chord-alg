from typing import *
from chord_node import ChordNode


def stabilize_and_print(nodes: List[ChordNode]):
    print('**************************')
    for i in range(10):
        for node in nodes:
            node.stabilize()
            node.fix_fingers()

    for node in nodes:
        print(node)

    print('**************************')


if __name__ == "__main__":
    m: int = 3

    nodes: List[ChordNode] = []

    head: ChordNode = ChordNode(3, 0)
    head.join(None)
    nodes.append(head)

    for n in [1, 3]:
        node: ChordNode = ChordNode(m, n)
        node.join2(head)
        nodes.append(node)
        
    stabilize_and_print(nodes)
    print("stabilize... until append\n")
    six_node: ChordNode = ChordNode(m, 6)
    six_node.join2(head)
    nodes.append(six_node)
    print("stabilize... before append\n")
    stabilize_and_print(nodes)

    six_node._delete()
    nodes.remove(six_node)
    print("stabilize... before remove\n")
    stabilize_and_print(nodes)
    print("done")
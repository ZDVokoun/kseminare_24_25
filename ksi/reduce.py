from typing import Tuple, Union, Callable, TypeVar, Self
from functools import partial

T = TypeVar("T")
LeafFunc = Callable[[int], T]
IntTransform = Callable[[int, T, T], T]
StrTransform = Callable[[str, T, T], T]

IntFunction = Callable[[int], int]

ArithmTree = Union["ArithmLeaf", "ArithmNode"]


class Tree:
    def __init__(
        self,
        value: int,
        left: Self | None = None,
        right: Self | None = None,
    ):
        self.value = value
        self.left = left
        self.right = right

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Tree)
            and self.value == other.value
            and self.left == other.left
            and self.right == other.right
        )


class ArithmLeaf:
    def __init__(self, value: int) -> None:
        self.value = value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ArithmLeaf) and self.value == other.value


class ArithmNode:
    def __init__(
        self, value: str, left: ArithmTree, right: ArithmTree
    ) -> None:
        """
        self.value can be one of +, -, *
        """
        self.value = value
        self.left = left
        self.right = right

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, ArithmNode)
            and self.value == other.value
            and self.left == other.left
            and self.right == other.right
        )


class LinkedListNode:
    def __init__(self, value: int, next_node: Self | None = None) -> None:
        self.value = value
        self.next = next_node

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, LinkedListNode)
            and self.value == other.value
            and self.next == other.next
        )


class ListTree:
    def __init__(self, value: int, children: list["ListTree"]) -> None:
        self.value = value
        self.children = children

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, ListTree)
            and self.value == other.value
            and self.children == other.children
        )


def tree_reduce(func: IntTransform[T], leaf_val: T, tree: Tree | None) -> T:
    if tree is None:
        return leaf_val
    return func(
        tree.value,
        tree_reduce(func, leaf_val, tree.left),
        tree_reduce(func, leaf_val, tree.right),
    )


def arithm_tree_reduce(
    func: StrTransform[T], leaf_func: LeafFunc[T], tree: ArithmTree
) -> T:
    if isinstance(tree, ArithmLeaf):
        return leaf_func(tree.value)
    return func(
        tree.value,
        arithm_tree_reduce(func, leaf_func, tree.left),
        arithm_tree_reduce(func, leaf_func, tree.right),
    )


def in_order_function(
    value: int, left: list[int], right: list[int]
) -> list[int]:
    # TODO
    return left + [value] + right


def in_order_base() -> list[int]:
    # TODO
    return []


def node_map_apply(
    function: IntFunction, value: int, left: Tree, right: Tree
) -> Tree | None:
    # TODO
    return Tree(function(value), left, right)


def node_map_base() -> Tree | None:
    # TODO
    return None


def evaluate_function(value: str, left: int, right: int) -> int:
    # TODO
    return eval(str(left) + value + str(right))


def evaluate_base(value: int) -> int:
    # TODO
    return value


LinkedFunction = Callable[[int, T], T]
ListFunction = Callable[[int, list[T]], T]


def linked_reduce(
    linked_func: LinkedFunction[T], leaf_val: T, node: LinkedListNode | None
) -> T:
    # TODO
    if node is None:
        return leaf_val
    return linked_func(
        node.value, linked_reduce(linked_func, leaf_val, node.next)
    )


def list_tree_reduce(list_func: ListFunction[T], node: ListTree) -> T:
    # TODO
    if len(node.children) == 0:
        return list_func(node.value, [])
    return list_func(
        node.value,
        list(
            map(lambda ch: list_tree_reduce(list_func, ch), node.children)
        ),
    )


def in_order(tree: Tree | None) -> list[int]:
    return tree_reduce(in_order_function, in_order_base(), tree)


def node_map(function: IntFunction, tree: Tree | None) -> Tree | None:
    node_map_function = partial(node_map_apply, function)
    return tree_reduce(node_map_function, node_map_base(), tree)


def is_bst(tree: Tree | None) -> bool:
    if tree is None:
        return True
    def helper(
        value, left: Tuple[bool, int] | None, right: Tuple[bool, int] | None
    ) -> Tuple[bool, int]:
        left_holds = True
        right_holds = True
        if left is not None:
            left_holds = left_holds and left[0]
            left_holds = left_holds and (left[1] <= value)
        if right is not None:
            right_holds = right_holds and right[0]
            right_holds = right_holds and (right[1] >= value)
        return (left_holds and right_holds, value)
    return tree_reduce(helper, None, tree)[0]


def evaluate(tree: ArithmTree) -> int:
    return arithm_tree_reduce(evaluate_function, evaluate_base, tree)


if __name__ == "__main__":
    # Trees
    leaf0 = Tree(0)
    leaf1 = Tree(1)
    leaf2 = Tree(2)
    leaf3 = Tree(3)
    leaf4 = Tree(4)
    leaf5 = Tree(5)
    leaf6 = Tree(6)
    leaf7 = Tree(7)
    leaf8 = Tree(8)
    leaf14 = Tree(14)

    sub_tree1 = Tree(4, leaf3, leaf1)
    sub_tree2 = Tree(0, leaf2, leaf7)
    sub_tree3 = Tree(8, leaf6, leaf2)
    sub_tree4 = Tree(0, leaf4, leaf14)
    sub_tree5 = Tree(1, leaf0, leaf2)
    sub_tree6 = Tree(5, leaf4, leaf7)
    tree1 = Tree(5, sub_tree1, sub_tree2)
    tree2 = Tree(10, sub_tree3, sub_tree4)
    tree3 = Tree(3, sub_tree5, sub_tree6)

    # Arithmetic trees
    aleaf0 = ArithmLeaf(0)
    aleaf1 = ArithmLeaf(1)
    aleaf2 = ArithmLeaf(2)
    aleaf3 = ArithmLeaf(3)
    aleaf4 = ArithmLeaf(4)
    aleaf5 = ArithmLeaf(5)
    aleaf6 = ArithmLeaf(6)
    aleaf7 = ArithmLeaf(7)
    aleaf8 = ArithmLeaf(8)

    atree1 = ArithmNode("-", aleaf3, aleaf1)
    atree2 = ArithmNode("+", aleaf2, aleaf7)
    tree4 = ArithmNode("*", atree1, atree2)

    # Linked lists
    linked_list1 = LinkedListNode(4)
    linked_list2 = LinkedListNode(2, linked_list1)
    linked_list3 = LinkedListNode(1, linked_list2)

    # List trees
    list_tree1 = ListTree(1, [])
    list_tree2 = ListTree(2, [])
    list_tree3 = ListTree(3, [])
    list_tree4 = ListTree(4, [])
    list_tree5 = ListTree(5, [list_tree1, list_tree2, list_tree3])
    list_tree6 = ListTree(6, [list_tree4])
    tree5 = ListTree(7, [list_tree5, list_tree6])
    tree6 = None

    # In-order
    assert in_order(leaf3) == [3]
    assert in_order(leaf1) == [1]
    assert in_order(leaf2) == [2]
    assert in_order(leaf7) == [7]
    assert in_order(sub_tree1) == [3, 4, 1]
    assert in_order(sub_tree2) == [2, 0, 7]
    assert in_order(tree1) == [3, 4, 1, 5, 2, 0, 7]
    assert in_order(tree6) == []

    # Node map
    assert node_map(lambda x: x * 2, tree1) == tree2
    assert node_map(lambda x: x, tree1) == tree1
    assert node_map(lambda x: x % 2, sub_tree2) == Tree(0, leaf0, leaf1)
    assert node_map(lambda x: x * 2, tree6) is None

    # Binary search tree
    assert not is_bst(tree1)
    assert not is_bst(tree2)
    assert is_bst(tree3)
    assert not is_bst(sub_tree1)
    assert not is_bst(sub_tree2)
    assert not is_bst(sub_tree3)
    assert not is_bst(sub_tree4)
    assert is_bst(sub_tree5)
    assert is_bst(sub_tree6)
    assert is_bst(tree6)

    # Arithmetic tree
    assert evaluate(tree4) == 18
    assert evaluate(atree1) == 2
    assert evaluate(atree2) == 9
    assert evaluate(aleaf0) == 0
    assert evaluate(aleaf5) == 5
    assert evaluate(ArithmNode("+", tree4, tree4)) == 36

    # Linked list
    assert linked_reduce(lambda x, y: x - y, 0, linked_list3) == 3
    assert linked_reduce(lambda x, y: x + y, 0, linked_list3) == 7
    assert linked_reduce(lambda x, y: x * y, 1, linked_list3) == 8
    assert linked_reduce(lambda x, y: x * y, 0, linked_list3) == 0
    assert linked_reduce(lambda x, y: x * y, 0, tree6) == 0

    assert (
        list_tree_reduce(
            lambda value, children: value + sum(children), tree5
        )
        == 28
    )
    assert list_tree_reduce(lambda x, _: x, tree5) == 7
    assert (
        list_tree_reduce(
            lambda value, children: str(value)
            + ": ["
            + ", ".join(children)
            + "]",
            tree5,
        )
        == "7: [5: [1: [], 2: [], 3: []], 6: [4: []]]"
    )

    print("All tests passed!")

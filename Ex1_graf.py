class BST:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None

def add_root(root, value):  # jak Pani rozumie słowo 'root'?
    if root.value > value:
        if root.left is None:
            root.left = BST(value)
            root.left.parent = root
        else:
            add_root(root.left, value)
    else:
        if root.right is None:
            root.right = BST(value)
            root.right.parent = root
        else:
            add_root(root.right, value)

def find(root, value):
    if root is None:
        return False
    if root.value == value:
        return True
    if root.value > value:
        return find(root.left, value)
    return find(root.right, value)

def in_order(root):
    if root.left:
        in_order(root.left)
    print(root.value)
    if root.right:
        in_order(root.right)

if __name__ == "__main__":
    root = BST(5)

    add_root(root, 3)
    add_root(root, 7)
    add_root(root, 2)
    add_root(root, 1)
    add_root(root, 5)
    add_root(root, 8)
    add_root(root, 0)

    print(find(root, 3))
    print(find(root, 6))
    in_order(root)

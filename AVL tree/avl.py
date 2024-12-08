class AvlNode:
    def __init__(self, data):
        self.data = data
        self.height = 1
        self.left = None
        self.right = None

class AvlTree:
    def __init__(self):
        self.root = None

    def max(self, a, b):
        return a if a > b else b

    def height(self, node):
        if node is None:
            return 0
        return node.height

    def get_balance(self, node):
        if node is None:
            return 0
        return self.height(node.left) - self.height(node.right)

    def rotate_right(self, node):
        x = node.left
        t2 = x.right

        x.right = node
        node.left = t2

        node.height = 1 + self.max(self.height(node.left), self.height(node.right))
        x.height = 1 + self.max(self.height(x.left), self.height(x.right))

        return x

    def rotate_left(self, node):
        x = node.right
        t2 = x.left

        x.left = node
        node.right = t2

        node.height = 1 + self.max(self.height(node.left), self.height(node.right))
        x.height = 1 + self.max(self.height(x.left), self.height(x.right))

        return x



    def insert(self, root, data):
        if root is None:
            return AvlNode(data=data)

        if data < root.data:
            root.left = self.insert(root.left, data=data)
        elif data > root.data:
            root.right = self.insert(root.right, data=data)
        else:
            return root

        root.height = 1 + self.max(self.height(root.left), self.height(root.right))

        balance = self.get_balance(root)

        # LL
        if balance > 1 and data < root.left.data:
            return self.rotate_right(root)

        # RR
        if balance < -1 and data > root.right.data:
            return self.rotate_left(root)

        # LR
        if balance > 1 and data > root.left.data:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)

        # RL
        if balance < -1 and data < root.right.data:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root

    def inorder(self, root):
        if root is not None:
            self.inorder(root.left)
            print("data:", root.data)
            self.inorder(root.right)


# Ana Program
tree = AvlTree()

while True:
    print("1- List AVL")
    print("2- Insert AVL")
    print("3- Exit")
    choice = input("-> ")
    if choice == "1":
        if tree.root:
            tree.inorder(tree.root)
        else:
            print("Ağaç boş!")
    elif choice == "2":
        try:
            data = int(input("Enter a number: "))
            tree.root = tree.insert(root=tree.root, data=data)
        except ValueError:
            print("Invalid input!")
    elif choice == "3":
        break
    else:
        print("Geçersiz seçim!")

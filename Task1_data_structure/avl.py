"""
AVL Tree (self-balancing BST) for storing city locations.
Guarantees O(log n) insert/delete/search via rotations.
"""

from bst import City  # reuse City class


class AVLNode:
    __slots__ = ("key", "city", "left", "right", "height")

    def __init__(self, key, city):
        self.key = key
        self.city = city
        self.left = None
        self.right = None
        self.height = 1  # leaf height = 1


class AVLTree:
    def __init__(self):
        self.root = None
        self._size = 0

    def __len__(self):
        return self._size

    def _h(self, node):
        return node.height if node else 0

    def _balance_factor(self, node):
        return self._h(node.left) - self._h(node.right) if node else 0

    def _update_height(self, node):
        node.height = 1 + max(self._h(node.left), self._h(node.right))

    def _rotate_right(self, y):
        x = y.left
        t2 = x.right
        x.right = y
        y.left = t2
        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x):
        y = x.right
        t2 = y.left
        y.left = x
        x.right = t2
        self._update_height(x)
        self._update_height(y)
        return y

    def _rebalance(self, node):
        self._update_height(node)
        bf = self._balance_factor(node)

        if bf > 1:  # left-heavy
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)  # LR case
            return self._rotate_right(node)  # LL case

        if bf < -1:  # right-heavy
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)  # RL case
            return self._rotate_left(node)  # RR case

        return node

    # ---------- Insert: O(log n) guaranteed ----------
    def insert(self, key, city):
        self.root = self._insert(self.root, key, city)

    def _insert(self, node, key, city):
        if node is None:
            self._size += 1
            return AVLNode(key, city)
        if key < node.key:
            node.left = self._insert(node.left, key, city)
        elif key > node.key:
            node.right = self._insert(node.right, key, city)
        else:
            node.city = city
            return node
        return self._rebalance(node)

    # ---------- Search: O(log n) guaranteed ----------
    def search(self, key):
        node = self.root
        while node is not None:
            if key == node.key:
                return node.city
            node = node.left if key < node.key else node.right
        return None

    # ---------- Delete: O(log n) guaranteed ----------
    def delete(self, key):
        self.root, deleted = self._delete(self.root, key)
        if deleted:
            self._size -= 1
        return deleted

    def _delete(self, node, key):
        if node is None:
            return node, False
        if key < node.key:
            node.left, deleted = self._delete(node.left, key)
        elif key > node.key:
            node.right, deleted = self._delete(node.right, key)
        else:
            deleted = True
            if node.left is None:
                return node.right, deleted
            if node.right is None:
                return node.left, deleted
            successor = self._min_node(node.right)
            node.key, node.city = successor.key, successor.city
            node.right, _ = self._delete(node.right, successor.key)
        if node is not None:
            node = self._rebalance(node)
        return node, deleted

    def _min_node(self, node):
        while node.left is not None:
            node = node.left
        return node

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node is not None:
            self._inorder(node.left, result)
            result.append((node.key, node.city))
            self._inorder(node.right, result)

    def height(self):
        return self._h(self.root) - 1 if self.root else -1


if __name__ == "__main__":
    tree = AVLTree()
    cities = [
        City("Kathmandu", 27.7172, 85.3240, 1_500_000, 0),
        City("Pokhara", 28.2096, 83.9856, 400_000, 200),
        City("Butwal", 27.7000, 83.4486, 150_000, 280),
        City("Biratnagar", 26.4525, 87.2718, 250_000, 400),
        City("Dharan", 26.8065, 87.2846, 150_000, 370),
        City("Nepalgunj", 28.0500, 81.6167, 150_000, 550),
    ]

    print("=" * 50)
    print("AVL TREE - DEMO")
    print("=" * 50)

    print("\nInsertion:")
    for c in cities:
        tree.insert(c.name, c)
        print(f"  Inserted -> {c.name}  (height={tree.height()})")

    print("\nInorder Traversal (sorted by key):")
    for key, city in tree.inorder():
        print(f"  {key:<12} pop={city.population:<10} dist={city.distance}")

    print(f"\nTree Height: {tree.height()}")
    print(f"Total Nodes: {len(tree)}")

    print("\nSearch:")
    for name in ["Pokhara", "Itahari"]:
        result = tree.search(name)
        status = "FOUND" if result else "NOT FOUND"
        print(f"  {name:<12} -> {status}")

    print("\nDeletion:")
    for name in ["Pokhara", "Itahari"]:
        deleted = tree.delete(name)
        status = "DELETED" if deleted else "NOT FOUND"
        print(f"  {name:<12} -> {status}  (height={tree.height()})")

    print("\nFinal Inorder Traversal:")
    for key, city in tree.inorder():
        print(f"  {key:<12} pop={city.population:<10} dist={city.distance}")

    print(f"\nTotal Nodes: {len(tree)}")
    print("=" * 50)
"""
AVL Tree (self-balancing BST) for storing city locations.
Guarantees O(log n) insert/delete/search via rotations.
"""

from bst import City  # reuse City class


class AVLNode:
    __slots__ = ("key", "city", "left", "right", "height")

    def __init__(self, key, city):
        self.key = key
        self.city = city
        self.left = None
        self.right = None
        self.height = 1  # leaf height = 1


class AVLTree:
    def __init__(self):
        self.root = None
        self._size = 0

    def __len__(self):
        return self._size

    def _h(self, node):
        return node.height if node else 0

    def _balance_factor(self, node):
        return self._h(node.left) - self._h(node.right) if node else 0

    def _update_height(self, node):
        node.height = 1 + max(self._h(node.left), self._h(node.right))

    def _rotate_right(self, y):
        x = y.left
        t2 = x.right
        x.right = y
        y.left = t2
        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x):
        y = x.right
        t2 = y.left
        y.left = x
        x.right = t2
        self._update_height(x)
        self._update_height(y)
        return y

    def _rebalance(self, node):
        self._update_height(node)
        bf = self._balance_factor(node)

        if bf > 1:  # left-heavy
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)  # LR case
            return self._rotate_right(node)  # LL case

        if bf < -1:  # right-heavy
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)  # RL case
            return self._rotate_left(node)  # RR case

        return node

    # ---------- Insert: O(log n) guaranteed ----------
    def insert(self, key, city):
        self.root = self._insert(self.root, key, city)

    def _insert(self, node, key, city):
        if node is None:
            self._size += 1
            return AVLNode(key, city)
        if key < node.key:
            node.left = self._insert(node.left, key, city)
        elif key > node.key:
            node.right = self._insert(node.right, key, city)
        else:
            node.city = city
            return node
        return self._rebalance(node)

    # ---------- Search: O(log n) guaranteed ----------
    def search(self, key):
        node = self.root
        while node is not None:
            if key == node.key:
                return node.city
            node = node.left if key < node.key else node.right
        return None

    # ---------- Delete: O(log n) guaranteed ----------
    def delete(self, key):
        self.root, deleted = self._delete(self.root, key)
        if deleted:
            self._size -= 1
        return deleted

    def _delete(self, node, key):
        if node is None:
            return node, False
        if key < node.key:
            node.left, deleted = self._delete(node.left, key)
        elif key > node.key:
            node.right, deleted = self._delete(node.right, key)
        else:
            deleted = True
            if node.left is None:
                return node.right, deleted
            if node.right is None:
                return node.left, deleted
            successor = self._min_node(node.right)
            node.key, node.city = successor.key, successor.city
            node.right, _ = self._delete(node.right, successor.key)
        if node is not None:
            node = self._rebalance(node)
        return node, deleted

    def _min_node(self, node):
        while node.left is not None:
            node = node.left
        return node

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node is not None:
            self._inorder(node.left, result)
            result.append((node.key, node.city))
            self._inorder(node.right, result)

    def height(self):
        return self._h(self.root) - 1 if self.root else -1


if __name__ == "__main__":
    tree = AVLTree()
    cities = [
        City("Kathmandu", 27.7172, 85.3240, 1_500_000, 0),
        City("Pokhara", 28.2096, 83.9856, 400_000, 200),
        City("Butwal", 27.7000, 83.4486, 150_000, 280),
        City("Biratnagar", 26.4525, 87.2718, 250_000, 400),
        City("Dharan", 26.8065, 87.2846, 150_000, 370),
        City("Nepalgunj", 28.0500, 81.6167, 150_000, 550),
    ]

    print("=" * 50)
    print("AVL TREE - DEMO")
    print("=" * 50)

    print("\nInsertion:")
    for c in cities:
        tree.insert(c.name, c)
        print(f"  Inserted -> {c.name}  (height={tree.height()})")

    print("\nInorder Traversal (sorted by key):")
    for key, city in tree.inorder():
        print(f"  {key:<12} pop={city.population:<10} dist={city.distance}")

    print(f"\nTree Height: {tree.height()}")
    print(f"Total Nodes: {len(tree)}")

    print("\nSearch:")
    for name in ["Pokhara", "Itahari"]:
        result = tree.search(name)
        status = "FOUND" if result else "NOT FOUND"
        print(f"  {name:<12} -> {status}")

    print("\nDeletion:")
    for name in ["Pokhara", "Itahari"]:
        deleted = tree.delete(name)
        status = "DELETED" if deleted else "NOT FOUND"
        print(f"  {name:<12} -> {status}  (height={tree.height()})")

    print("\nFinal Inorder Traversal:")
    for key, city in tree.inorder():
        print(f"  {key:<12} pop={city.population:<10} dist={city.distance}")

    print(f"\nTotal Nodes: {len(tree)}")
    print("=" * 50)
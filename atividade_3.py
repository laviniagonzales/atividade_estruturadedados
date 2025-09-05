# atividade_3.py

from graphviz import Digraph
import random

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None

    # Inserção em BST
    def insert(self, value):
        if not self.root:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, current, value):
        if value < current.value:
            if current.left:
                self._insert_recursive(current.left, value)
            else:
                current.left = Node(value)
        elif value > current.value:
            if current.right:
                self._insert_recursive(current.right, value)
            else:
                current.right = Node(value)
        # duplicados não são inseridos

    # Travessias DFS
    def inorder(self):
        return self._inorder_recursive(self.root)

    def _inorder_recursive(self, node):
        if not node:
            return []
        return self._inorder_recursive(node.left) + [node.value] + self._inorder_recursive(node.right)

    def preorder(self):
        return self._preorder_recursive(self.root)

    def _preorder_recursive(self, node):
        if not node:
            return []
        return [node.value] + self._preorder_recursive(node.left) + self._preorder_recursive(node.right)

    def postorder(self):
        return self._postorder_recursive(self.root)

    def _postorder_recursive(self, node):
        if not node:
            return []
        return self._postorder_recursive(node.left) + self._postorder_recursive(node.right) + [node.value]

    # Visualização com Graphviz
    def visualize(self, filename="tree"):
        dot = Digraph()
        def add_nodes_edges(node):
            if not node:
                return
            dot.node(str(node.value))
            if node.left:
                dot.edge(str(node.value), str(node.left.value))
                add_nodes_edges(node.left)
            if node.right:
                dot.edge(str(node.value), str(node.right.value))
                add_nodes_edges(node.right)
        add_nodes_edges(self.root)
        dot.render(filename, view=True, format="png")


# ---------------------------
# Árvore com Valores Fixos
# ---------------------------
print("=== Árvore Fixa ===")
fixed_values = [55, 30, 80, 20, 45, 70, 90]
bt_fixed = BinaryTree()
for v in fixed_values:
    bt_fixed.insert(v)

bt_fixed.visualize("fixed_tree")

print("In-Order:", bt_fixed.inorder())
print("Pre-Order:", bt_fixed.preorder())
print("Post-Order:", bt_fixed.postorder())

# ---------------------------
# Árvore com Valores Aleatórios
# ---------------------------
print("\n=== Árvore Aleatória ===")
random_values = random.sample(range(1, 101), 10)
bt_random = BinaryTree()
for v in random_values:
    bt_random.insert(v)

bt_random.visualize("random_tree")
print("Valores aleatórios inseridos:", random_values)
print("In-Order:", bt_random.inorder())
print("Pre-Order:", bt_random.preorder())
print("Post-Order:", bt_random.postorder())

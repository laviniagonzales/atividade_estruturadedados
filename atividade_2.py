# atividade_2.py

from graphviz import Digraph
import random

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    # ---------------------------
    # Inserção
    # ---------------------------
    def insert(self, value):
        self.root = self._insert(self.root, value)

    def _insert(self, node, value):
        if not node:
            return Node(value)
        if value < node.value:
            node.left = self._insert(node.left, value)
        elif value > node.value:
            node.right = self._insert(node.right, value)
        return node  # duplicados não são inseridos

    # ---------------------------
    # Busca
    # ---------------------------
    def search(self, value):
        return self._search(self.root, value)

    def _search(self, node, value):
        if not node:
            return False
        if value == node.value:
            return True
        elif value < node.value:
            return self._search(node.left, value)
        else:
            return self._search(node.right, value)

    # ---------------------------
    # Remoção
    # ---------------------------
    def delete(self, value):
        self.root = self._delete(self.root, value)

    def _delete(self, node, value):
        if not node:
            return None
        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            # Nó sem filhos
            if not node.left and not node.right:
                return None
            # Nó com um filho
            if not node.left:
                return node.right
            if not node.right:
                return node.left
            # Nó com dois filhos
            temp = self._min_value_node(node.right)
            node.value = temp.value
            node.right = self._delete(node.right, temp.value)
        return node

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    # ---------------------------
    # Altura
    # ---------------------------
    def height(self):
        return self._height(self.root)

    def _height(self, node):
        if not node:
            return -1
        return 1 + max(self._height(node.left), self._height(node.right))

    # ---------------------------
    # Profundidade
    # ---------------------------
    def depth(self, value):
        return self._depth(self.root, value, 0)

    def _depth(self, node, value, d):
        if not node:
            return -1
        if value == node.value:
            return d
        elif value < node.value:
            return self._depth(node.left, value, d + 1)
        else:
            return self._depth(node.right, value, d + 1)

    # ---------------------------
    # Visualização com Graphviz
    # ---------------------------
    def visualize(self, filename="tree"):
        dot = Digraph()
        def add_edges(node):
            if not node:
                return
            dot.node(str(node.value))
            if node.left:
                dot.edge(str(node.value), str(node.left.value))
                add_edges(node.left)
            if node.right:
                dot.edge(str(node.value), str(node.right.value))
                add_edges(node.right)
        add_edges(self.root)
        dot.render(filename, view=True, format="png")

# ---------------------------
# Árvore Fixa
# ---------------------------
print("=== Árvore com Valores Fixos ===")
fixed_values = [55, 30, 80, 20, 45, 70, 90]
bst_fixed = BinarySearchTree()
for v in fixed_values:
    bst_fixed.insert(v)

bst_fixed.visualize("fixed_tree")
print("Busca 45:", bst_fixed.search(45))

bst_fixed.delete(30)
bst_fixed.insert(60)
print("Altura da árvore:", bst_fixed.height())
print("Profundidade do nó 45:", bst_fixed.depth(45))
bst_fixed.visualize("fixed_tree_after_ops")

# ---------------------------
# Árvore Aleatória
# ---------------------------
print("\n=== Árvore com Valores Aleatórios ===")
random_values = random.sample(range(1, 201), 15)
bst_random = BinarySearchTree()
for v in random_values:
    bst_random.insert(v)

print("Valores aleatórios inseridos:", random_values)
bst_random.visualize("random_tree")
print("Altura da árvore aleatória:", bst_random.height())

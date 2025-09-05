# atividade_4.py
# Nome: Lavinia Gonzales de Lima

from graphviz import Digraph
import random

class AVLNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    # Inserção pública
    def insert(self, value):
        self.root = self._insert_node(self.root, value)

    # Inserção recursiva com balanceamento
    def _insert_node(self, node, value):
        if not node:
            return AVLNode(value)
        elif value < node.value:
            node.left = self._insert_node(node.left, value)
        elif value > node.value:
            node.right = self._insert_node(node.right, value)
        else:
            return node  # duplicados não são permitidos

        # Atualizar altura
        node.height = 1 + max(self._height(node.left), self._height(node.right))

        # Balanceamento
        return self._balance_node(node, value)

    # Altura do nó
    def _height(self, node):
        return node.height if node else 0

    # Calcula fator de balanceamento
    def _balance_factor(self, node):
        return self._height(node.left) - self._height(node.right) if node else 0

    # Balanceia o nó e aplica rotações se necessário
    def _balance_node(self, node, value):
        balance = self._balance_factor(node)

        # Rotação LL
        if balance > 1 and value < node.left.value:
            return self._rotate_right(node)
        # Rotação RR
        if balance < -1 and value > node.right.value:
            return self._rotate_left(node)
        # Rotação LR
        if balance > 1 and value > node.left.value:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        # Rotação RL
        if balance < -1 and value < node.right.value:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    # Rotação à direita
    def _rotate_right(self, y):
        x = y.left
        y.left = x.right
        x.right = y

        # Atualiza alturas
        y.height = 1 + max(self._height(y.left), self._height(y.right))
        x.height = 1 + max(self._height(x.left), self._height(x.right))
        return x

    # Rotação à esquerda
    def _rotate_left(self, x):
        y = x.right
        x.right = y.left
        y.left = x

        # Atualiza alturas
        x.height = 1 + max(self._height(x.left), self._height(x.right))
        y.height = 1 + max(self._height(y.left), self._height(y.right))
        return y

    # Visualização da árvore com Graphviz
    def visualize(self, filename="avl_tree"):
        dot = Digraph()
        def _add_edges(node):
            if not node:
                return
            dot.node(str(node.value))
            if node.left:
                dot.edge(str(node.value), str(node.left.value))
                _add_edges(node.left)
            if node.right:
                dot.edge(str(node.value), str(node.right.value))
                _add_edges(node.right)
        _add_edges(self.root)
        dot.render(filename, view=True, format="png")

# ---------------------------
# Demonstração: Rotação Simples
# ---------------------------
print("=== AVL Simples (RR ou LL) ===")
avl_simple = AVLTree()
for v in [10, 20, 30]:  # forçando rotação RR
    avl_simple.insert(v)
    avl_simple.visualize(f"avl_simple_{v}")

# ---------------------------
# Demonstração: Rotação Dupla
# ---------------------------
print("=== AVL Dupla (RL ou LR) ===")
avl_double = AVLTree()
for v in [10, 30, 20]:  # forçando rotação RL
    avl_double.insert(v)
    avl_double.visualize(f"avl_double_{v}")

# ---------------------------
# Demonstração: Valores Aleatórios
# ---------------------------
print("=== AVL Aleatória ===")
random_values = random.sample(range(1, 201), 20)
avl_random = AVLTree()
for v in random_values:
    avl_random.insert(v)

print("Valores aleatórios inseridos:", random_values)
avl_random.visualize("avl_random_tree")

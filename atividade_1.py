# atividade_1.py
# Nome: Lavinia Gonzales de Lima

import random
from graphviz import Digraph

# -------------------------------
# Classe para representar um nó da árvore
# -------------------------------
class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value  # operador ou operando
        self.left = left    # filho esquerdo
        self.right = right  # filho direito


# -------------------------------
# Função para desenhar a árvore
# -------------------------------
def draw_tree(root, filename="tree"):
    dot = Digraph(comment="Expression Tree")
    
    def add_nodes_edges(node, parent=None):
        if node:
            dot.node(str(id(node)), str(node.value))
            if parent:
                dot.edge(str(id(parent)), str(id(node)))
            add_nodes_edges(node.left, node)
            add_nodes_edges(node.right, node)
    
    add_nodes_edges(root)
    dot.render(filename, format="png", cleanup=True)
    print(f"Árvore salva como {filename}.png")


# -------------------------------
# Árvore fixa
# Expressão: (( (7 + 3) * (5 - 2)) / (10 * 20))
# -------------------------------
def fixed_expression_tree():
    # Construindo manualmente a árvore
    left_subtree = Node("*", Node("+", Node(7), Node(3)), Node("-", Node(5), Node(2)))
    right_subtree = Node("*", Node(10), Node(20))
    root = Node("/", left_subtree, right_subtree)
    return root


# -------------------------------
# Árvore randômica
# -------------------------------
def random_expression_tree():
    operators = ["+", "-", "*", "/"]
    
    # Gera 3 operandos aleatórios entre 1 e 20
    operands = [str(random.randint(1, 20)) for _ in range(3)]
    
    # Seleciona 2 operadores aleatórios
    op1, op2 = random.sample(operators, 2)
    
    # Monta expressão do tipo: (a op1 b) op2 c
    left_subtree = Node(op1, Node(operands[0]), Node(operands[1]))
    root = Node(op2, left_subtree, Node(operands[2]))
    
    return root


# -------------------------------
# Programa principal
# -------------------------------
if __name__ == "__main__":
    # Árvore fixa
    print("Gerando árvore da expressão fixa...")
    fixed_tree = fixed_expression_tree()
    draw_tree(fixed_tree, "expressao_fixa")
    
    # Árvore randômica
    print("Gerando árvore da expressão randômica...")
    random_tree = random_expression_tree()
    draw_tree(random_tree, "expressao_randomica")


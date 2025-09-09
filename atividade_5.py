# -*- coding: utf-8 -*-

class No:
    """
    Representa um nó na Árvore AVL.
    Cada nó armazena uma chave, referências para os filhos e sua altura.
    """
    def __init__(self, chave):
        self.chave = chave
        self.esquerda = None
        self.direita = None
        self.altura = 1  # A altura de um novo nó (folha) é sempre 1


class ArvoreAVL:
    """
    Implementa a estrutura e as operações de uma Árvore AVL.
    """
    def __init__(self):
        self.raiz = None

    # ===============================================================
    # TAREFA 0: MÉTODOS AUXILIARES E ROTAÇÕES
    # ===============================================================

    def obter_altura(self, no):
        """
        Calcula a altura de um nó. Se o nó for nulo, a altura é 0.
        """
        return no.altura if no is not None else 0

    def obter_fator_balanceamento(self, no):
        """
        Calcula o fator de balanceamento de um nó (altura(esq) - altura(dir)).
        """
        if no is None:
            return 0
        return self.obter_altura(no.esquerda) - self.obter_altura(no.direita)

    def _atualizar_altura(self, no):
        """
        Atualiza a altura de um nó com base na altura máxima de seus filhos.
        A altura é 1 + max(altura(esquerda), altura(direita)).
        """
        no.altura = 1 + max(self.obter_altura(no.esquerda),
                            self.obter_altura(no.direita))

    def obter_no_valor_minimo(self, no):
        """
        Encontra o nó com o menor valor em uma subárvore (o nó mais à esquerda).
        """
        atual = no
        while atual and atual.esquerda is not None:
            atual = atual.esquerda
        return atual

    def _rotacao_direita(self, no_pivo):
        """
        Realiza uma rotação para a direita em torno do no_pivo.
        """
        y = no_pivo.esquerda
        T3 = y.direita

        # Rotaciona
        y.direita = no_pivo
        no_pivo.esquerda = T3

        # Atualiza alturas
        self._atualizar_altura(no_pivo)
        self._atualizar_altura(y)

        # Nova raiz da subárvore
        return y

    def _rotacao_esquerda(self, no_pivo):
        """
        Realiza uma rotação para a esquerda em torno do no_pivo.
        """
        y = no_pivo.direita
        T2 = y.esquerda

        # Rotaciona
        y.esquerda = no_pivo
        no_pivo.direita = T2

        # Atualiza alturas
        self._atualizar_altura(no_pivo)
        self._atualizar_altura(y)

        # Nova raiz da subárvore
        return y

    # ===============================================================
    # TAREFA 1: INSERÇÃO E DELEÇÃO COM BALANCEAMENTO
    # ===============================================================

    def inserir(self, chave):
        """Método público para inserir uma chave na árvore."""
        self.raiz = self._inserir_recursivo(self.raiz, chave)

    def _inserir_recursivo(self, no_atual, chave):
        # Passo 1: Inserção padrão BST
        if no_atual is None:
            return No(chave)
        if chave < no_atual.chave:
            no_atual.esquerda = self._inserir_recursivo(no_atual.esquerda, chave)
        elif chave > no_atual.chave:
            no_atual.direita = self._inserir_recursivo(no_atual.direita, chave)
        else:
            raise ValueError(f"Chave duplicada não permitida: {chave}")

        # Passo 2: Atualiza altura
        self._atualizar_altura(no_atual)

        # Passo 3: Calcula fator de balanceamento
        fb = self.obter_fator_balanceamento(no_atual)

        # Passo 4: Corrige desbalanceamentos com rotações
        # Caso 1: Esquerda-Esquerda
        if fb > 1 and chave < no_atual.esquerda.chave:
            return self._rotacao_direita(no_atual)

        # Caso 2: Direita-Direita
        if fb < -1 and chave > no_atual.direita.chave:
            return self._rotacao_esquerda(no_atual)

        # Caso 3: Esquerda-Direita
        if fb > 1 and chave > no_atual.esquerda.chave:
            no_atual.esquerda = self._rotacao_esquerda(no_atual.esquerda)
            return self._rotacao_direita(no_atual)

        # Caso 4: Direita-Esquerda
        if fb < -1 and chave < no_atual.direita.chave:
            no_atual.direita = self._rotacao_direita(no_atual.direita)
            return self._rotacao_esquerda(no_atual)

        return no_atual

    def deletar(self, chave):
        """Método público para deletar uma chave da árvore."""
        self.raiz = self._deletar_recursivo(self.raiz, chave)

    def _deletar_recursivo(self, no_atual, chave):
        # Passo 1: Deleção padrão BST
        if no_atual is None:
            return no_atual

        if chave < no_atual.chave:
            no_atual.esquerda = self._deletar_recursivo(no_atual.esquerda, chave)
        elif chave > no_atual.chave:
            no_atual.direita = self._deletar_recursivo(no_atual.direita, chave)
        else:
            # Encontrou o nó a deletar
            if no_atual.esquerda is None or no_atual.direita is None:
                # Um filho ou nenhum
                temp = no_atual.esquerda if no_atual.esquerda else no_atual.direita
                if temp is None:
                    # Sem filhos
                    no_atual = None
                else:
                    # Um único filho (copia o conteúdo)
                    no_atual.chave = temp.chave
                    no_atual.esquerda = temp.esquerda
                    no_atual.direita = temp.direita
                    no_atual.altura = temp.altura
            else:
                # Dois filhos: pega o sucessor (menor da direita)
                sucessor = self.obter_no_valor_minimo(no_atual.direita)
                no_atual.chave = sucessor.chave
                no_atual.direita = self._deletar_recursivo(no_atual.direita, sucessor.chave)

        # Se a árvore ficou vazia
        if no_atual is None:
            return no_atual

        # Passo 2: Atualiza altura
        self._atualizar_altura(no_atual)

        # Passo 3: Calcula fator
        fb = self.obter_fator_balanceamento(no_atual)

        # Passo 4: Corrige desbalanceamentos
        # Esquerda-Esquerda
        if fb > 1 and self.obter_fator_balanceamento(no_atual.esquerda) >= 0:
            return self._rotacao_direita(no_atual)

        # Esquerda-Direita
        if fb > 1 and self.obter_fator_balanceamento(no_atual.esquerda) < 0:
            no_atual.esquerda = self._rotacao_esquerda(no_atual.esquerda)
            return self._rotacao_direita(no_atual)

        # Direita-Direita
        if fb < -1 and self.obter_fator_balanceamento(no_atual.direita) <= 0:
            return self._rotacao_esquerda(no_atual)

        # Direita-Esquerda
        if fb < -1 and self.obter_fator_balanceamento(no_atual.direita) > 0:
            no_atual.direita = self._rotacao_direita(no_atual.direita)
            return self._rotacao_esquerda(no_atual)

        return no_atual

    # ===============================================================
    # TAREFA 2 E 3: BUSCAS
    # ===============================================================

    def encontrar_nos_intervalo(self, chave1, chave2):
        """
        Encontra e retorna uma lista com todas as chaves no intervalo [chave1, chave2].
        """
        resultado = []
        def inorder_interval(no):
            if no is None:
                return
            if no.chave >= chave1:
                inorder_interval(no.esquerda)
            if chave1 <= no.chave <= chave2:
                resultado.append(no.chave)
            if no.chave <= chave2:
                inorder_interval(no.direita)
        inorder_interval(self.raiz)
        return resultado

    def obter_profundidade_no(self, chave):
        """
        Calcula a profundidade (nível) de um nó com uma chave específica.
        A raiz está no nível 0. Se o nó não for encontrado, retorna -1.
        """
        profundidade = 0
        atual = self.raiz
        while atual is not None:
            if chave == atual.chave:
                return profundidade
            elif chave < atual.chave:
                atual = atual.esquerda
            else:
                atual = atual.direita
            profundidade += 1
        return -1

    # --- Utilitário para depuração/validação ---
    def em_ordem(self):
        """Retorna a lista de chaves em percurso em-ordem (crescente)."""
        res = []
        def _inorder(no):
            if no is None:
                return
            _inorder(no.esquerda)
            res.append(no.chave)
            _inorder(no.direita)
        _inorder(self.raiz)
        return res


# --- Bloco de Teste e Demonstração da Atividade AVL ---
if __name__ == "__main__":
    arvore_avl = ArvoreAVL()
    
    print("\n--- ATIVIDADE PRÁTICA: ÁRVORE AVL ---")
    
    print("\n--- 1. Inserindo nós ---")
    chaves_para_inserir = [9, 5, 10, 0, 6, 11, -1, 1, 2]
    try:
        for chave in chaves_para_inserir:
            arvore_avl.inserir(chave)
        print("Inserção concluída (sem erros).")
        print("In-ordem:", arvore_avl.em_ordem())
    except Exception as e:
        print(f"\nERRO DURANTE A INSERÇÃO: {e}")

    print("\n--- 2. Deletando nós ---")
    try:
        chaves_para_deletar = [10, 11]
        for chave in chaves_para_deletar:
            arvore_avl.deletar(chave)
        print("Deleção concluída (sem erros).")
        print("In-ordem após deleção:", arvore_avl.em_ordem())
    except Exception as e:
        print(f"\nERRO DURANTE A DELEÇÃO: {e}")

    print("\n--- 3. Buscando nós no intervalo [1, 9] ---")
    try:
        nos_no_intervalo = arvore_avl.encontrar_nos_intervalo(1, 9)
        if nos_no_intervalo is not None:
            print(f"Nós encontrados: {sorted(nos_no_intervalo)}")
        else:
            print("Método `encontrar_nos_intervalo` ainda não implementado.")
    except Exception as e:
        print(f"\nERRO DURANTE A BUSCA POR INTERVALO: {e}")

    print("\n--- 4. Calculando profundidade do nó 6 ---")
    try:
        profundidade = arvore_avl.obter_profundidade_no(6)
        if profundidade is not None:
            if profundidade != -1:
                print(f"O nó 6 está no nível/profundidade: {profundidade}")
            else:
                print("O nó 6 não foi encontrado.")
        else:
            print("Método `obter_profundidade_no` ainda não implementado.")
    except Exception as e:
        print(f"\nERRO DURANTE O CÁLCULO DE PROFUNDIDADE: {e}")


from turtle import st
from Node import Arbol
from Leaf import Leaf
import functools
from graphviz import Digraph


class AFD():
    def __init__(self, regex):

        self.count = 0
        self.rounds = 1
        self.states = []
        self.simbolos = []
        self.transiciones = []
        self.ef = []
        self.e0 = None
        self.nodes = []  # Tiene el conjunto de hojas
        self.root = None
        self.id = 0
        self.final_state = None
        self.follow_pos = {}
        self.time_total = 0

        self.build_tree(regex)  # Se construye el arbol con la expresion dada

        # Funcion que termina proceso al encontrar el simbolo
        # que significa el final de la expresion
        for n in self.nodes:
            if n.name == '#':
                self.final_state = n.position
                break

        self.calculate_followpow()
        # print(self.follow_pos)
        self.creacion_afd()
        self.estados = []
        self.simbolos = []
        self.aceptados = []
        for state in self.states:
            self.estados.append(state.name)
        for hoja in self.simbolos:
            if isinstance(hoja, str):
                self.simbolos.append(hoja)
            else:
                pass
        for aceptado in self.ef:
            self.aceptados.append(aceptado)

        # Crear un nuevo gráfico
        dot = Digraph()
        # Agregar los nodos al gráfico
        for i, estado in enumerate(self.estados):
            # estados completos : dot.node(str(i), label=str(sorted(estado)))
            # estados con letras +97 para minusculas
            dot.node(str(estado), label=str(chr(i+65)))
            if estado in self.aceptados:
                dot.node(str(estado), shape='doublecircle')
        # Agregar las transiciones al gráfico
        for transicion in self.transiciones:
            dot.edge(str(transicion[0]), str(
                transicion[2]), label=str(transicion[1]))
        # Exportar el gráfico como un archivo PNG
        dot.render('afd_directo_grafico', format='png', view=True)

        with open('afd_directo.txt', 'a', encoding="utf-8") as f:
            f.write("AFD a partir de un regex -->")
            f.write("\n")
            f.write("Símbolos: " + str(self.simbolos))
            f.write("\n")
            f.write("Estados:  " + str(self.estados))
            f.write("\n")
            f.write("Estado inicial: " + str(self.e0))
            f.write("\n")
            f.write("Estados de aceptación:" + str(self.aceptados))
            f.write("\n")
            f.write("Transiciones: " + str(self.transiciones))

        print("\nArchivo de AFD directo escrito con éxito")

    def build_tree(self, regex):
        stack = []  # guarda simbolos
        op = []  # guarda operadores

        for character in regex:
            if self.is_symbols(character):
                stack.append(character)
            elif character == '(':
                op.append('(')
            elif character == ')':
                last_in = self.peek_stack(op)
                while last_in is not None and last_in != '(':
                    root = self.operate(op, stack)
                    stack.append(root)
                    last_in = self.peek_stack(op)
                op.pop()
            else:
                last_in = self.peek_stack(op)
                while last_in is not None and last_in not in '()' and self.preceding_operator(last_in, character):
                    root = self.operate(op, stack)
                    stack.append(root)
                    last_in = self.peek_stack(op)
                op.append(character)

        while self.peek_stack(op) is not None:
            root = self.operate(op, stack)
            stack.append(root)
        self.root = stack.pop()

    # Obtiene la precedencia entre dos operadores
    def preceding_operator(self, op1, op2):
        order = ['|', '.', '*']
        if order.index(op1) >= order.index(op2):
            return True
        else:
            return False
    # Funcion que identifica si es 'ε', letra o numero

    def is_symbols(self, character):
        symbols = 'ε'+'abcdefghijklmnopqrstuvwxyz0123456789#'
        # si no lo encuentra regresa vacio
        return symbols.find(character) != -1

    # funcion que regresa ultimo elemento del stack
    def peek_stack(self, stack):
        if stack:
            return stack[-1]  # Ultimo elemento
        else:
            return None

    # Obtiene el ID del nodo
    def get_id(self):
        self.id = self.id + 1
        return self.id

    # Funcion que dependiendo si es simbolo u operador realiza un append
    # o realiza la operacion
    def operate(self, operators, values):
        operator = operators.pop()
        right = values.pop()
        left = '@'

        if right not in self.simbolos and right != 'ε' and right != '@' and right != '#':
            self.simbolos.append(right)

        if operator != '*' and operator != '+' and operator != '?':
            left = values.pop()

            if left not in self.simbolos and left != 'ε' and left != '@' and left != '#':
                self.simbolos.append(left)

        if operator == '|':
            return self.operator_or(left, right)
        elif operator == '.':
            return self.operator_concat(left, right)
        elif operator == '*':
            return self.operator_kleene(right)

    # Funcion del operador or
    def operator_or(self, left, right):
        operator = '|'

        if isinstance(left, Leaf) and isinstance(right, Leaf):
            root = Leaf(operator, None, True, [
                        left, right], left.nullable or right.nullable)
            self.nodes += [root]
            return root

        elif not isinstance(left, Leaf) and not isinstance(right, Leaf):
            id_left = None
            id_right = None
            if left != 'ε':
                id_left = self.get_id()
            if right != 'ε':
                id_right = self.get_id()

            left_leaf = Leaf(left, id_left, False, [], False)
            right_leaf = Leaf(right, id_right, False, [], False)
            root = Leaf(operator, None, True, [
                        left_leaf, right_leaf], left_leaf.nullable or right_leaf.nullable)

            self.nodes += [left_leaf, right_leaf, root]

            return root

        elif isinstance(left, Leaf) and not isinstance(right, Leaf):
            id_right = None
            if right != 'ε':
                id_right = self.get_id()

            right_leaf = Leaf(right, id_right, False, [], False)
            root = Leaf(operator, None, True, [
                        left, right_leaf], left.nullable or right_leaf.nullable)

            self.nodes += [right_leaf, root]
            return root

        elif not isinstance(left, Leaf) and isinstance(right, Leaf):
            id_left = None
            if left != 'ε':
                id_left = self.get_id()

            left_leaf = Leaf(left, id_left, False, [], False)
            root = Leaf(operator, None, True, [
                        left_leaf, right], left_leaf.nullable or right.nullable)

            self.nodes += [left_leaf, root]
            return root

    # Operacion kleen
    def operator_kleene(self, leaf):
        operator = '*'
        if isinstance(leaf, Leaf):
            root = Leaf(operator, None, True, [leaf], True)
            self.nodes += [root]
            return root

        else:
            id_left = None
            if leaf != 'ε':
                id_left = self.get_id()

            left_leaf = Leaf(leaf, id_left, False, [], False)
            root = Leaf(operator, None, True, [left_leaf], True)
            self.nodes += [left_leaf, root]

            return root

    # Operacion concatenacion
    def operator_concat(self, left, right):
        operator = '.'
        if isinstance(left, Leaf) and isinstance(right, Leaf):
            root = Leaf(operator, None, True, [
                        left, right], left.nullable and right.nullable)
            self.nodes += [root]
            return root

        elif not isinstance(left, Leaf) and not isinstance(right, Leaf):
            id_left = None
            id_right = None
            if left != 'ε':
                id_left = self.get_id()
            if right != 'ε':
                id_right = self.get_id()

            left_leaf = Leaf(left, id_left, False, [], False)
            right_leaf = Leaf(right, id_right, False, [], False)
            root = Leaf(operator, None, True, [
                        left_leaf, right_leaf], left_leaf.nullable and right_leaf.nullable)

            self.nodes += [left_leaf, right_leaf, root]
            return root

        elif isinstance(left, Leaf) and not isinstance(right, Leaf):
            id_right = None
            if right != 'ε':
                id_right = self.get_id()

            right_leaf = Leaf(right, id_right, False, [], False)
            root = Leaf(operator, None, True, [
                        left, right_leaf], left.nullable and right_leaf.nullable)

            self.nodes += [right_leaf, root]
            return root

        elif not isinstance(left, Leaf) and isinstance(right, Leaf):
            id_left = None
            if left != 'ε':
                id_left = self.get_id()

            left_leaf = Leaf(left, id_left, False, [], False)
            root = Leaf(operator, None, True, [
                        left_leaf, right], left_leaf.nullable and right.nullable)

            self.nodes += [left_leaf, root]
            return root

    # Se realiza el calculo de followpos

    def calculate_followpow(self):
        for n in self.nodes:
            if not n.is_operator and not n.nullable:
                self.add_followpos(n.position, [])

        for n in self.nodes:
            if n.name == '.':
                c1, c2 = [*n.children]

                for i in c1.last_pos:
                    self.add_followpos(i, c2.first_pos)

            elif n.name == '*':
                for i in n.last_pos:
                    self.add_followpos(i, n.first_pos)

    # Agrega un followpos
    def add_followpos(self, pos, val):
        if pos not in self.follow_pos.keys():
            self.follow_pos[pos] = []

        self.follow_pos[pos] += val
        self.follow_pos[pos] = {i for i in self.follow_pos[pos]}
        self.follow_pos[pos] = [i for i in self.follow_pos[pos]]

    # Obtiene el nombre para asignarlo al nodo
    def get_name(self):
        if self.count == 0:
            self.count += 1
            return 'S'  # Starting node!

        available_letters = ' ABCDEFGHIJKLMNOPQRTUVWXYZ'
        name = available_letters[self.count]
        self.count += 1

        if self.count == len(available_letters):
            self.rounds += 1
            self.count = 0

        return name * self.rounds

    # Genera los nodos y transiciones para el AFD
    def creacion_afd(self):
        s0 = self.root.first_pos
        # print(s0)
        s0_AFD = Arbol(self.get_name(), s0, True)
        self.states.append(s0_AFD)
        self.e0 = s0_AFD.name

        if self.final_state in [u for u in s0_AFD.conjunto_nodos]:
            self.ef.append(s0_AFD.name)
            # print(s0_AFD.name)

        while not self.state_is_marked():
            T = self.state_is_unmarked()

            T.Mark()

            for s in self.simbolos:
                fp = []

                for u in T.conjunto_nodos:
                    if self.get_leaf(u).name == s:
                        fp += self.follow_pos[u]
                fp = {a for a in fp}
                fp = [a for a in fp]
                if len(fp) == 0:
                    continue

                U = Arbol(self.get_name(), fp, True)

                if U.id not in [n.id for n in self.states]:
                    # print(fp)
                    if self.final_state in [u for u in U.conjunto_nodos]:
                        self.ef.append(U.name)
                        # print(U.name)
                    self.states.append(U)
                    # print((T.conjunto_nodos, s, U.conjunto_nodos))
                    self.transiciones.append((T.name, s, U.name))
                else:
                    self.count -= 1
                    for estado in self.states:
                        if U.id == estado.id:
                            self.transiciones.append((T.name, s, estado.name))
                            # print((T.conjunto_nodos, s, estado.conjunto_nodos))

    # Obtiene el estado unmarked

    def state_is_unmarked(self):
        for n in self.states:
            if not n.isMarked:
                return n

     # Revisa si existe algun estado desmarcado

    def state_is_marked(self):
        marks = [n.isMarked for n in self.states]
        return functools.reduce(lambda a, b: a and b, marks)

    # Obtiene la hoja a traves de su nombre
    def get_leaf(self, name):
        for n in self.nodes:
            if n.position == name:
                return n

    # Crea las transiciones del grafo
    def create_transitions(self):
        f = {}
        for t in self.transiciones:
            i, s, fi = [*t]

            if i not in f.keys():
                f[i] = {}
            f[i][s] = fi

        return f

    # Implementacion de Move para la simulacion
    def simulate_move(self, Nodo, symbol):
        move = None
        for i in self.transiciones:
            if i[0] == Nodo and i[1] == symbol:
                move = i[2]

        return move

    # Simulacion de AFD
    def simulate_string(self, exp):
        start = self.e0
        for e in exp:
            start = self.simulate_move(start, e)
            if start == None:
                return False
        if start in self.ef:
            return True
        return False

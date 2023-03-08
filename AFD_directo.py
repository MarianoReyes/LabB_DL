class State:
    """
    Clase que representa un estado del AFD.
    """

    def __init__(self, name=None):
        self.name = name
        self.transitions = {}

    def add_transition(self, symbol, state):
        self.transitions[symbol] = state


class DFA:
    """
    Clase que representa el AFD.
    """

    def __init__(self, start_state, accepting_states):
        self.start_state = start_state
        self.accepting_states = accepting_states

    def accepts(self, string):
        """
        Función que determina si una cadena es aceptada o no por el AFD.
        """
        current_state = self.start_state
        for symbol in string:
            current_state = current_state.transitions.get(symbol)
            if current_state is None:
                return False
        return current_state in self.accepting_states


def parse_regex(regex):
    """
    Función que convierte la expresión regular en un árbol de sintaxis abstracta.
    """
    # Definimos las funciones que generan los nodos del AST.

    def parse_primary():
        nonlocal pos
        if pos >= len(regex):
            raise ValueError("Unexpected end of regex")
        if regex[pos] == "(":
            pos += 1
            node = parse_alternation()
            if pos >= len(regex) or regex[pos] != ")":
                raise ValueError("Expected closing parenthesis")
            pos += 1
        elif regex[pos] == ".":
            pos += 1
            node = ASTNode("concatenation")
        elif regex[pos] == "|":
            raise ValueError("Unexpected alternation")
        elif regex[pos] == "*":
            raise ValueError("Unexpected kleene star")
        elif regex[pos] == "+":
            raise ValueError("Unexpected positive closure")
        elif regex[pos] == "?":
            raise ValueError("Unexpected optional element")
        else:
            node = ASTNode("literal", regex[pos])
            pos += 1
        return node

    def parse_closure():
        nonlocal pos
        node = parse_primary()
        while pos < len(regex):
            if regex[pos] == "*":
                node = ASTNode("kleene_star", right=node)
                pos += 1
            elif regex[pos] == "+":
                node = ASTNode("positive_closure", right=node)
                pos += 1
            elif regex[pos] == "?":
                node = ASTNode("optional", right=node)
                pos += 1
            else:
                break
        return node

    def parse_concatenation():
        nonlocal pos
        left = parse_closure()
        while pos < len(regex) and regex[pos] not in "|)":
            right = parse_closure()
            left = ASTNode("concatenation", left=left, right=right)
        return left

    def parse_alternation():
        nonlocal pos
        left = parse_concatenation()
        if pos < len(regex) and regex[pos] == "|":
            pos += 1
            right = parse_alternation()
            left = ASTNode("alternation", left=left, right=right)
        return left

    # Convertimos la regex en un AST.
    pos = 0
    ast = parse_alternation()
    if pos < len(regex):
        raise ValueError("Unexpected character")
    return ast


def build_dfa(ast):
    """
    Función que construye el AFD a partir del AST.
    """
    start_state = State()
    accepting_states = set()

    # Implementar aquí el algoritmo de construcción directa.

    return DFA(start_state, accepting_states)


def build_dfa(ast):
    """
    Función que construye el AFD a partir del AST.
    """
    def build_dfa_rec(node):
        if node.kind == "literal":
            state1 = State()
            state2 = State()
            state1.add_transition(node.value, state2)
            return state1, state2
        elif node.kind == "concatenation":
            left_start, left_end = build_dfa_rec(node.left)
            right_start, right_end = build_dfa_rec(node.right)
            left_end.add_transition("", right_start)
            return left_start, right_end
        elif node.kind == "alternation":
            start = State()
            end = State()
            left_start, left_end = build_dfa_rec(node.left)
            right_start, right_end = build_dfa_rec(node.right)
            start.add_transition("", left_start)
            start.add_transition("", right_start)
            left_end.add_transition("", end)
            right_end.add_transition("", end)
            return start, end
        elif node.kind == "kleene_star":
            start = State()
            end = State()
            inner_start, inner_end = build_dfa_rec(node.right)
            start.add_transition("", inner_start)
            start.add_transition("", end)
            inner_end.add_transition("", inner_start)
            inner_end.add_transition("", end)
            return start, end
        elif node.kind == "positive_closure":
            start = State()
            end = State()
            inner_start, inner_end = build_dfa_rec(node.right)
            start.add_transition("", inner_start)
            inner_end.add_transition("", inner_start)
            inner_end.add_transition("", end)
            return start, end
        elif node.kind == "optional":
            start = State()
            end = State()
            inner_start, inner_end = build_dfa_rec(node.right)
            start.add_transition("", inner_start)
            start.add_transition("", end)
            inner_end.add_transition("", end)
            return start, end
        else:
            raise ValueError("Unknown AST node kind")

    start_state, end_state = build_dfa_rec(ast)
    accepting_states = {end_state}
    return DFA(start_state, accepting_states)


class ASTNode:
    """
    Clase que representa un nodo del AST.
    """

    def __init__(self, kind, value=None, left=None, right=None):
        self.kind = kind
        self.value = value
        self.left = left
        self.right = right


class State:
    """
    Clase que representa un estado del AFD.
    """

    def __init__(self, label=None):
        self.label = label
        self.transitions = {}

    def add_transition(self, symbol, state):
        self.transitions[symbol] = state


class DFA:
    """
    Clase que representa un AFD.
    """

    def __init__(self, start_state, accepting_states):
        self.start_state = start_state
        self.accepting_states = accepting_states

    def recognize(self, string):
        current_state = self.start_state
        for symbol in string:
            current_state = current_state.transitions.get(symbol)
            if current_state is None:
                return False
        return current_state in self.accepting_states


regex = "(a|b)*abb"
ast = parse_regex(regex)
dfa = build_dfa(ast)

# Reconocer cadenas
strings = ["", "a", "b", "ab", "ba", "abb", "bab", "bba", "abab", "bbabb"]
for s in strings:
    if dfa.recognize(s):
        print(f"'{s}' es una cadena válida")
    else:
        print(f"'{s}' no es una cadena válida")

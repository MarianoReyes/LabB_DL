from typing import List, Tuple, Set


class TreeNode:
    def __init__(self, val: str):
        self.val = val
        self.left = None
        self.right = None
        self.states = set()


def shunting_yard(expr: str) -> str:
    """
    Convierte una expresión regular a su forma postfija utilizando el algoritmo de Shunting Yard.
    """
    # Implementación del algoritmo de Shunting Yard


def build_syntax_tree(expr: str) -> TreeNode:
    """
    Construye un árbol sintáctico a partir de una expresión regular en forma postfija.
    """
    # Implementación del algoritmo de construcción de árboles sintácticos


def assign_states(node: TreeNode, start_state: int) -> int:
    """
    Asigna conjuntos de estados a cada nodo del árbol sintáctico.
    """
    if node.val == 'epsilon':
        node.states.add(start_state)
        return start_state
    elif node.val == 'char':
        node.states.add(start_state)
        node.states.add(start_state + 1)
        return start_state + 1
    elif node.val == '.':
        left_end_state = assign_states(node.left, start_state)
        for state in node.left.states:
            if state == left_end_state:
                continue
            for ch in node.right.states:
                node.left.states.add(ch)
                node.left.states.add(state)
        return assign_states(node.right, left_end_state)
    elif node.val == '|':
        end_state = max(assign_states(node.left, start_state),
                        assign_states(node.right, start_state))
        for state in node.left.states:
            node.states.add(state)
        for state in node.right.states:
            node.states.add(state)
        return end_state
    elif node.val == '*':
        node.states.add(start_state)
        node.states.add(start_state + 1)
        left_end_state = assign_states(node.left, start_state + 2)
        for state in node.left.states:
            if state == left_end_state:
                continue
            node.left.states.add(start_state)
            node.left.states.add(left_end_state + 1)
            node.left.states.add(state)
            node.left.states.add(left_end_state)
        node.left.states.add(start_state)
        node.left.states.add(left_end_state + 1)
        node.states.add(left_end_state + 1)
        return left_end_state + 1


def build_dfa(node: TreeNode) -> Tuple[Set[int], List[Set[int]], List[List[int]]]:
    """
    Genera un AFD a partir del árbol sintáctico.
    """
    # Creamos un diccionario para mapear los conjuntos de estados a los nuevos estados del AFD
    state_map = {}

    # Función auxiliar para obtener el conjunto de estados del nodo
    def get_node_states(n: TreeNode) -> Set[int]:
        return n.states

    # Función auxiliar para obtener el estado del conjunto de estados
    def get_state(states: Set[int]) -> int:
        if not states:
            return -1
        if states in state_map:
            return state_map[states]
        state_id = len(state_map)
        state_map[states] = state_id
        return state_id

    # Obtenemos el conjunto de estados inicial y lo añadimos al AFD
    initial_states = get_node_states(node)
    initial_state = get_state(initial_states)
    dfa_states = set([initial_state])
    dfa_accept_states = []
    dfa_transitions = []

    # Cola para procesar los nuevos estados del AFD
    state_queue = [initial_states]

    # Procesamos los nuevos estados del AFD
    while state_queue:
        current_states = state_queue.pop(0)
        current_state = get_state(current_states)

        # Comprobamos si este estado contiene un estado de aceptación
        if any(state in current_states for state in node.states):
            dfa_accept_states.append(current_state)

        # Creamos una nueva fila para las transiciones de este estado
        dfa_transitions.append([-1] * 26)

        # Comprobamos cada símbolo del alfabeto
        for i in range(26):
            symbol = chr(ord('a') + i)

            # Obtenemos el conjunto de estados a los que podemos transicionar con el símbolo actual
            next_states = set()
            for state in current_states:
                if state.val == 'char' and state.val == symbol:
                    next_states.add(state.right)
                elif state.val != 'char' and symbol == 'epsilon':
                    next_states |= get_node_states(state.left)
                    next_states |= get_node_states(state.right)

            # Si no hay estados a los que podamos transicionar, saltamos a la siguiente iteración
            if not next_states:
                continue

            # Obtenemos el estado del conjunto de estados resultante
            next_state = get_state(next_states)

            # Añadimos el estado resultante al AFD y a la cola de procesamiento si es un estado nuevo
            if next_state not in dfa_states:
                dfa_states.add(next_state)
                state_queue.append(next_states)

            # Añadimos la transición a la tabla de transiciones del AFD
            dfa_transitions[current_state][i] = next_state

    return dfa_states, dfa_accept_states, dfa_transitions


# Ejemplo de uso:
expr = 'a|b*'
postfix_expr = shunting_yard(expr)
syntax_tree = build_syntax_tree(postfix_expr)
assign_states(syntax_tree, 1)
dfa_states, dfa_accept_states, dfa_transitions = build_dfa(syntax_tree)

from graphviz import Digraph


class MinimizadorAFD:

    def __init__(self, e0, ef, transiciones, estados):
        self.e0 = e0
        self.ef = ef
        self.transiciones = transiciones
        self.estados = estados
        self.grupos = []

    def minimizar(self, filename):
        print("\nMinimizando AFD...")
        self.initialize_groups()
        self.split_groups()
        self.graficar(self.build_new_afd(), filename)
        self.escribir(filename)

    def initialize_groups(self):
        no_final = [x for x in self.estados if x not in self.ef]
        self.grupos = [no_final, self.ef]

    def split_groups(self):
        while True:
            new_groups = []
            for group in self.grupos:
                if len(group) == 1:
                    new_groups.append(group)
                    continue
                grouped_by_transitions = {}
                for state in group:
                    transition_key = self.get_transition_key(state)
                    if transition_key in grouped_by_transitions:
                        grouped_by_transitions[transition_key].append(state)
                    else:
                        grouped_by_transitions[transition_key] = [state]
                new_groups.extend(grouped_by_transitions.values())
            if new_groups == self.grupos:
                break
            self.grupos = new_groups

    def get_transition_key(self, state):
        transition_key = []
        for symbol in self.get_symbols():
            next_state = self.get_next_state(state, symbol)
            for i, group in enumerate(self.grupos):
                if next_state in group:
                    transition_key.append(i)
                    break
        return tuple(transition_key)

    def get_symbols(self):
        symbols = set()
        for transition in self.transiciones:
            symbols.add(transition[1])
        return symbols

    def get_next_state(self, state, symbol):
        for transition in self.transiciones:
            if transition[0] == state and transition[1] == symbol:
                return transition[2]
        return None

    def build_new_afd(self):
        self.new_states = [str(i) for i in range(len(self.grupos))]
        new_e0 = self.get_new_initial_state()
        new_ef = self.get_new_final_states()
        new_transitions = self.get_new_transitions()
        return MinimizadorAFD(new_e0, new_ef, new_transitions, self.new_states)

    def get_new_initial_state(self):
        for i, group in enumerate(self.grupos):
            if self.e0 in group:
                return str(i)
        return None

    def get_new_final_states(self):
        new_ef = []
        for i, group in enumerate(self.grupos):
            for state in group:
                if state in self.ef:
                    new_ef.append(str(i))
                    break
        return new_ef

    def get_new_transitions(self):
        new_transitions = []
        for i, group in enumerate(self.grupos):
            for symbol in self.get_symbols():
                next_state = self.get_next_state(group[0], symbol)
                for j, other_group in enumerate(self.grupos):
                    if next_state in other_group:
                        new_transitions.append([str(i), symbol, str(j)])
                        break
        return new_transitions

    def graficar(self, minimizador_afd, filename):
        graph = Digraph()
        graph.attr(rankdir='LR')

        # Agregar estados
        for i, estado in enumerate(minimizador_afd.estados):
            if estado in minimizador_afd.ef:
                graph.node(estado, shape='doublecircle', label=str(chr(i+65)))
            else:
                graph.node(estado, shape='circle', label=str(chr(i+65)))

        # Agregar transiciones
        for transicion in minimizador_afd.transiciones:
            graph.edge(transicion[0], transicion[2], label=transicion[1])

        graph.render(filename, format='png', view=True)

    def escribir(self, filename):
        with open(filename+'.txt', 'a', encoding="utf-8") as f:
            f.write("AFD Minimizado a partir de un AFD generado por AFN -->")
            f.write("\n")
            f.write("Estados:  " + str(self.new_states))
            f.write("\n")
            f.write("Estado inicial: { " +
                    str(self.get_new_initial_state()) + " }")
            f.write("\n")
            f.write(
                "Estados de aceptación: { " + str(self.get_new_final_states()) + " }")
            f.write("\n")
            f.write("Transiciones: " + str(self.get_new_transitions()))

        print("\nArchivo de AFD Minimizado escrito con éxito")

    # metodo para simular una cadena en un afd minimizado
    def simular_cadena(self, cadena):
        # Empezar desde el estado inicial
        current_state = self.e0
        # Iterar a través de la cadena de entrada
        for symbol in cadena:
            # Obtener el próximo estado usando la transición actual
            next_state = self.get_next_state(current_state, symbol)
            # Si no hay transición disponible, la cadena es rechazada
            if next_state is None:
                return False
            # Actualizar el estado actual
            current_state = next_state
        # Verificar si el estado actual es final
        if current_state in self.ef:
            return True
        else:
            return False

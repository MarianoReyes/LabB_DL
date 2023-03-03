import pickle
from graphviz import Digraph


class AFNToAFD:
    def __init__(self, e0, ef, estados, simbolos, transiciones):
        self.e0 = e0
        self.ef = ef
        self.estados = estados
        self.simbolos = simbolos
        self.transiciones = transiciones
        self.transiciones_afd = []

    def conversion(self):
        nuevos_estados = []  # Conjunto de nuevos estados del AFD
        nuevos_transiciones = {}  # Diccionario de nuevas transiciones del AFD
        # Estado actual del AFD, como un conjunto inmutable
        estado_actual = frozenset([self.e0])

        # Inicializamos el conjunto de nuevos estados y transiciones con el estado actual del AFN
        nuevos_estados.append(estado_actual)
        for s in self.simbolos:
            nuevos_transiciones[(estado_actual, s)] = frozenset(
                self.obtener_transiciones(estado_actual, s))

        # Iteramos hasta que no se puedan encontrar más estados nuevos
        while True:
            nuevos_estados_encontrados = False
            for estado in nuevos_estados:
                for s in self.simbolos:
                    estado_alcanzable = frozenset(
                        self.obtener_transiciones(estado, s))
                    if estado_alcanzable not in nuevos_estados:
                        nuevos_estados.append(estado_alcanzable)
                        nuevos_estados_encontrados = True
                    nuevos_transiciones[(estado, s)] = estado_alcanzable

            if not nuevos_estados_encontrados:
                break

        # Creamos un nuevo diccionario de transiciones utilizando los nuevos estados y transiciones del AFD

        for k, v in nuevos_transiciones.items():
            self.transiciones_afd.append(
                [nuevos_estados.index(k[0]), k[1], nuevos_estados.index(v)])

        # Devolvemos el nuevo AFD
        return [0, len(nuevos_estados) - 1, nuevos_estados, self.simbolos, self.transiciones_afd]

    def obtener_transiciones(self, estado, simbolo):
        # Devuelve el conjunto de estados alcanzables desde el estado dado utilizando el símbolo dado
        estados_alcanzables = []
        for t in self.transiciones:
            if t[0] in estado and t[1] == simbolo:
                estados_alcanzables.append(t[2])
        return estados_alcanzables

    def graficar_afd(self):
        # Obtener la información del AFD
        [e0, ef, estados, simbolos, transiciones_afd] = self.conversion()

        # Crear el objeto Digraph de graphviz
        graph = Digraph()

        # Agregar los nodos al grafo
        for i, estado in enumerate(estados):
            # El estado inicial se representa como una flecha apuntando al estado
            if estado == frozenset([e0]):
                graph.node(str(i), shape='none')
                graph.edge('', str(i), label='inicio')

            # El estado final se representa como un doble círculo
            if ef in estado:
                graph.node(str(i), shape='doublecircle')

            # Los estados normales se representan como círculos simples
            if estado != frozenset([e0]) and ef not in estado:
                graph.node(str(i), shape='circle')

        # Agregar las transiciones al grafo
        for transicion in transiciones_afd:
            graph.edge(str(transicion[0]), str(
                transicion[2]), label=transicion[1])

        # Mostrar el grafo
        graph.view()

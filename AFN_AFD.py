from graphviz import Digraph


class AFNtoAFD:
    def __init__(self, e0, ef, estados, simbolos, transiciones):
        self.e0 = e0
        self.ef = ef
        self.estados = estados
        self.simbolos = simbolos
        self.transiciones = transiciones
        self.afd_estados = []
        self.afd_transiciones = []

    def cerradura_epsilon(self, estado):
        """
        Aplica la cerradura epsilon al estado dado y devuelve todos los estados alcanzables.
        """
        # Inicializar una lista con el estado inicial
        resultado = [estado]
        # Inicializar una pila con el estado inicial
        pila = [estado]
        # Mientras la pila no esté vacía
        while pila:
            # Obtener el siguiente estado de la pila
            actual = pila.pop()
            # Obtener todas las transiciones epsilon desde el estado actual
            epsilon_transiciones = [
                t[2] for t in self.transiciones if t[0] == actual and t[1] == "ε"]
            # Para cada estado alcanzable a través de una transición epsilon
            for e in epsilon_transiciones:
                # Si el estado no está en el resultado
                if e not in resultado:
                    # Agregar el estado al resultado y a la pila
                    resultado.append(e)
                    pila.append(e)
        # Devolver todos los estados alcanzables
        return resultado

    def mover(self, estados, simbolo):
        """
        Aplica la operación mover a un conjunto de estados y un símbolo y devuelve
        todos los estados alcanzables.
        """
        # Inicializar una lista vacía para almacenar los estados alcanzables
        resultado = []
        # Para cada estado en el conjunto de estados
        for estado in estados:
            # Obtener todas las transiciones que coincidan con el símbolo dado
            simbolo_transiciones = [
                t[2] for t in self.transiciones if t[0] == estado and t[1] == simbolo]
            # Agregar todos los estados alcanzables a través de estas transiciones al resultado
            resultado.extend(simbolo_transiciones)
        # Devolver todos los estados alcanzables
        return resultado

    def construir_afd(self):
        """
        Construye un AFD a partir del AFN dado utilizando la cerradura epsilon y mover.
        """
        print("\nConvirtiendo de AFN a AFD...")
        # Obtener la cerradura epsilon del estado inicial
        e0_cerradura = self.cerradura_epsilon(self.e0)
        # Agregar la cerradura epsilon del estado inicial como el primer estado del AFD
        self.afd_estados.append(e0_cerradura)
        # Inicializar una cola con el primer estado del AFD
        cola = [e0_cerradura]
        # Mientras la cola no esté vacía
        while cola:
            # Obtener el siguiente estado de la cola
            actual = cola.pop(0)
            # Para cada símbolo en el alfabeto del AFN
            for simbolo in self.simbolos:
                # Obtener la cerradura epsilon del conjunto de estados alcanzables
                # desde el estado actual consumiendo el símbolo actual

                for i in self.mover(actual, simbolo):
                    alcanzables = (self.cerradura_epsilon(i))

                # Si el conjunto de estados alcanzables no está en el AFD
                if alcanzables not in self.afd_estados:
                    # Agregar el conjunto de estados alcanzables al AFD como un nuevo estado
                    self.afd_estados.append(alcanzables)
                    # Agregar una transición desde el estado actual con el símbolo actual al
                    # conjunto de estados alcanzables en el AFD
                    self.afd_transiciones.append((self.afd_estados.index(
                        actual), simbolo, self.afd_estados.index(alcanzables)))
                    # Agregar el conjunto de estados alcanzables a la cola
                    cola.append(alcanzables)
                # Si el conjunto de estados alcanzables ya está en el AFD
                elif alcanzables in self.afd_estados and len(self.mover(actual, simbolo)) != 0:
                    # Agregar una transición desde el estado actual con el símbolo actual al
                    # conjunto de estados alcanzables en el AFD
                    self.afd_transiciones.append((self.afd_estados.index(
                        actual), simbolo, self.afd_estados.index(alcanzables)))

        # Crear un nuevo gráfico
        dot = Digraph()
        dot.attr(rankdir='LR')
        # Agregar los nodos al gráfico
        for i, estado in enumerate(self.afd_estados):
            dot.node(str(i), label=str(sorted(estado)))
            if estado == [self.e0]:
                dot.node('inicio', shape='none', label='')
                dot.edge('inicio', str(i))
            if self.ef in estado:
                dot.node(str(i), shape='doublecircle')
        # Agregar las transiciones al gráfico
        for transicion in self.afd_transiciones:
            dot.edge(str(transicion[0]), str(
                transicion[2]), label=str(transicion[1]))
        # Exportar el gráfico como un archivo PNG
        dot.render('afd_grafico', format='png', view=True)

        print("\nArchivo de AFD escrito con éxito")

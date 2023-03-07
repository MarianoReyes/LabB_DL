class MinimizadorAFD:
    def __init__(self, e0, ef, transiciones):
        self.e0 = e0
        self.ef = ef
        self.transiciones = transiciones

    def minimizar(self):
        # Paso 1: Construir tabla de equivalencia
        tabla = []
        for i in range(len(self.transiciones)):
            tabla.append([False] * i)
        for i in range(len(self.transiciones)):
            for j in range(i):
                if (i in self.ef and j not in self.ef) or (j in self.ef and i not in self.ef):
                    tabla[i][j] = True
        cambios = True
        while cambios:
            cambios = False
            for i in range(len(self.transiciones)):
                for j in range(i):
                    if not tabla[i][j]:
                        for k in range(len(self.transiciones[0]) - 1):
                            estado_i = self.transiciones[i][k + 1]
                            estado_j = self.transiciones[j][k + 1]
                            if tabla[max(estado_i, estado_j)][min(estado_i, estado_j)]:
                                tabla[i][j] = True
                                cambios = True
                                break

        # Paso 2: Combinar estados equivalentes en una sola clase
        clases = []
        for i in range(len(self.transiciones)):
            encontrada = False
            for c in clases:
                if tabla[max(c[0], i)][min(c[0], i)]:
                    c.append(i)
                    encontrada = True
                    break
            if not encontrada:
                clases.append([i])

        # Paso 3: Reconstruir AFD utilizando las clases resultantes
        nuevos_estados = {}
        contador = 0
        for c in clases:
            nuevos_estados[min(c)] = contador
            contador += 1
        nuevas_transiciones = []
        for i in range(len(self.transiciones)):
            estado = nuevos_estados[min(
                clases, key=lambda c: min([abs(s - i) for s in c]))[0]]
            nuevas_transiciones.append([estado] + self.transiciones[i][1:])
        nuevo_e0 = nuevos_estados[min(
            clases, key=lambda c: abs(c[0] - self.e0))[0]]
        nuevo_ef = []
        for c in clases:
            if any(e in self.ef for e in c):
                nuevo_ef.append(nuevos_estados[min(c)])

        # Devolver el AFD minimizado
        return nuevo_e0, nuevo_ef, nuevas_transiciones

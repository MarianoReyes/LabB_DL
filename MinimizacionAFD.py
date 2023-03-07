class MinimizadorAFD:
    def __init__(self, e0, ef, transiciones):
        self.e0 = e0
        self.ef = ef
        self.transiciones = transiciones
        self.estados = set(range(len(transiciones)+1))
        self.alfabeto = set(s for _, s, _ in transiciones)

    def minimizar(self):
        print(self.estados)
        # Paso 1: separar estados finales y no finales
        no_finales = self.estados - set(self.ef)
        grupos = [no_finales, set(self.ef)]
        nuevos_grupos = []
        while nuevos_grupos != grupos:
            # Paso 2: dividir grupos según transiciones
            nuevos_grupos = [set()]
            for grupo in grupos:
                por_simbolo = {}
                for estado in grupo:
                    simbolos = set(
                        s for e, s, _ in self.transiciones if e == estado)
                    for s in simbolos:
                        if s in por_simbolo:
                            por_simbolo[s].add(estado)
                        else:
                            por_simbolo[s] = {estado}
                for subgrupo in por_simbolo.values():
                    if len(subgrupo) > 1:
                        nuevos_grupos.append(subgrupo)
                    else:
                        nuevos_grupos[0].update(subgrupo)
            grupos = nuevos_grupos

        # Paso 3: construir nuevo autómata
        estados_nuevos = {}
        for i, grupo in enumerate(grupos):
            estados_nuevos.update({e: i for e in grupo})
        nuevas_transiciones = []
        for e, s, e1 in self.transiciones:
            nuevas_transiciones.append(
                (estados_nuevos[e], s, estados_nuevos[e1]))
        nuevo_e0 = estados_nuevos[self.e0]
        nuevo_ef = set(estados_nuevos[e] for e in self.ef)
        return MinimizadorAFD(nuevo_e0, nuevo_ef, nuevas_transiciones)

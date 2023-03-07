'''
Postfix a AFN
'''

from re import S
import pandas as pd
from graphviz import Digraph


class PostifixToAFN():
    def __init__(self, postfix):
        self.postfix = postfix
        self.estados = []
        self.estados_list = []
        self.e0 = None
        self.ef = None
        self.transiciones = []
        self.transiciones_splited = []
        self.simbolos = []
        self.afn_final = []
        self.error = False

    def graficar(self, nombre):
        dot = Digraph()
        for i in range(len(self.estados)):
            if self.estados[i] == self.ef:
                dot.node(str(self.estados[i]), shape="doublecircle")
            else:
                dot.node(str(self.estados[i]), shape="circle")
        for transicion in self.transiciones_splited:
            if transicion[1] == "ε":
                dot.edge(str(transicion[0]), str(transicion[2]), label="ε")
            else:
                dot.edge(str(transicion[0]), str(
                    transicion[2]), label=transicion[1])
        dot.render(nombre, format='png', view=True)

    def operando(self, caracter):
        if(caracter.isalpha() or caracter.isnumeric() or caracter == "ε"):
            return True
        else:
            return False

    def reemplazar_interrogacion(self):
        self.postfix = self.postfix.replace('?', 'ε?')

    def conversion(self):
        print("\nPostfix: ", self.postfix)
        self.reemplazar_interrogacion()
        print("\nConvirtiendo de Postfix a AFN...")
        simbolos = []
        postfix = self.postfix
        for i in postfix:
            if self.operando(i):
                if i not in simbolos:
                    simbolos.append(i)

        self.simbolos = sorted(simbolos)

        stack = []
        start = 0
        end = 1

        counter = -1
        c1 = 0
        c2 = 0

        # implementation del algoritmo de thompson

        for i in postfix:
            # si es un simbolo
            if i in simbolos:
                counter = counter+1
                c1 = counter
                if c1 not in self.estados:
                    self.estados.append(c1)
                counter = counter+1
                c2 = counter
                if c2 not in self.estados:
                    self.estados.append(c2)
                self.afn_final.append({})
                self.afn_final.append({})
                stack.append([c1, c2])
                self.afn_final[c1][i] = c2
                self.transiciones_splited.append([c1, i, c2])
            # si es un kleene
            elif i == '*':
                try:
                    r1, r2 = stack.pop()
                    counter = counter+1
                    c1 = counter
                    if c1 not in self.estados:
                        self.estados.append(c1)
                    counter = counter+1
                    c2 = counter
                    if c2 not in self.estados:
                        self.estados.append(c2)
                    self.afn_final.append({})
                    self.afn_final.append({})
                    stack.append([c1, c2])
                    self.afn_final[r2]['ε'] = (r1, c2)
                    self.afn_final[c1]['ε'] = (r1, c2)
                    if start == r1:
                        start = c1
                    if end == r2:
                        end = c2
                    self.transiciones_splited.append([r2, "ε", r1])
                    self.transiciones_splited.append([r2, "ε", c2])
                    self.transiciones_splited.append([c1, "ε", r1])
                    self.transiciones_splited.append([c1, "ε", c2])
                except:
                    self.error = True
                    print("\nExpresión Regex inválida, * mal aplicado")
            # si es una cerradura positiva
            elif i == '+':
                try:
                    r1, r2 = stack.pop()
                    counter = counter+1
                    c1 = counter
                    if c1 not in self.estados:
                        self.estados.append(c1)
                    counter = counter+1
                    c2 = counter
                    if c2 not in self.estados:
                        self.estados.append(c2)
                    self.afn_final.append({})
                    self.afn_final.append({})
                    stack.append([c1, c2])
                    self.afn_final[r2]['ε'] = (r1, c2)
                    if start == r1:
                        start = c1
                    if end == r2:
                        end = c2
                    self.transiciones_splited.append([r2, "ε", r1])
                    self.transiciones_splited.append([r2, "ε", c2])
                    self.transiciones_splited.append([c1, "ε", r1])
                except:
                    self.error = True
                    print("\nExpresión Regex inválida, + mal aplicado")

            # si es una concatenacion
            elif i == '.':
                try:
                    r11, r12 = stack.pop()
                    r21, r22 = stack.pop()
                    stack.append([r21, r12])
                    self.afn_final[r22]['ε'] = r11
                    if start == r11:
                        start = r21
                    if end == r22:
                        end = r12
                    self.transiciones_splited.append([r22, "ε", r11])

                except:
                    self.error = True
                    print(
                        "\nExpresión Regex inválida, concatenación mal aplicada o operando inválido.")
            # si es un or
            elif i == "|":
                try:
                    counter = counter+1
                    c1 = counter
                    if c1 not in self.estados:
                        self.estados.append(c1)
                    counter = counter+1
                    c2 = counter
                    if c2 not in self.estados:
                        self.estados.append(c2)
                    self.afn_final.append({})
                    self.afn_final.append({})

                    r11, r12 = stack.pop()
                    r21, r22 = stack.pop()
                    stack.append([c1, c2])
                    self.afn_final[c1]['ε'] = (r21, r11)
                    self.afn_final[r12]['ε'] = c2
                    self.afn_final[r22]['ε'] = c2
                    if start == r11 or start == r21:
                        start = c1
                    if end == r22 or end == r12:
                        end = c2
                    self.transiciones_splited.append([c1, "ε", r21])
                    self.transiciones_splited.append([c1, "ε", r11])
                    self.transiciones_splited.append([r12, "ε", c2])
                    self.transiciones_splited.append([r22, "ε", c2])
                except:
                    self.error = True
                    print("\nExpresión Regex inválida, | mal aplicado")
            # si es un uno o cero ?
            elif i == "?":
                counter = counter+1
                c1 = counter
                if c1 not in self.estados:
                    self.estados.append(c1)
                counter = counter+1
                c2 = counter
                if c2 not in self.estados:
                    self.estados.append(c2)
                self.afn_final.append({})
                self.afn_final.append({})

                r11, r12 = stack.pop()
                r21, r22 = stack.pop()
                stack.append([c1, c2])
                self.afn_final[c1]['ε'] = (r21, r11)
                self.afn_final[r12]['ε'] = c2
                self.afn_final[r22]['ε'] = c2
                if start == r11 or start == r21:
                    start = c1
                if end == r22 or end == r12:
                    end = c2
                self.transiciones_splited.append([c1, "ε", r21])
                self.transiciones_splited.append([c1, "ε", r11])
                self.transiciones_splited.append([r12, "ε", c2])
                self.transiciones_splited.append([r22, "ε", c2])

        # asignacion de estados finales e iniciales
        self.e0 = start
        self.ef = end

        # Guardar variables para impresión
        df = pd.DataFrame(self.afn_final)
        string_afn = df.to_string()
        for i in range(len(self.transiciones_splited)):
            self.transiciones.append(
                "(" + str(self.transiciones_splited[i][0]) + " - " + str(self.transiciones_splited[i][1]) + " - " + str(self.transiciones_splited[i][2]) + ")")
        self.transiciones = ', '.join(self.transiciones)

        for i in range(len(self.estados)):
            if i == len(self.estados)-1:
                ef = i
            self.estados_list.append(str(self.estados[i]))
        self.estados_list = ", ".join(self.estados_list)

        if self.error == False:

            with open('afn.txt', 'a', encoding="utf-8") as f:
                f.write("AFN  a partir de la Expresión Regular -->")
                f.write("\n")
                f.write("Símbolos: "+', '.join(simbolos))
                f.write("\n")
                f.write("Estados:  " + str(self.estados_list))
                f.write("\n")
                f.write("Estado inicial: { " + str(self.e0) + " }")
                f.write("\n")
                f.write("Estados de aceptación: { " + str(self.ef) + " }")
                f.write("\n")
                f.write("Transiciones: " + str(self.transiciones))
                f.write("\n")
                f.write(string_afn)

            print("\nArchivo de AFN escrito con éxito")

            # SI NO SE DESEA GRAFICAR POR PROBLEMAS CON LIBRERIA QUITAR LA LINEA SIGUIENTE
            self.graficar('afn_grafico')  # imagen del AFN
        else:
            print("\nIngrese una expresión Regex válida")

    def cerradura_epsilon(self, estados):
        """
        Aplica la cerradura epsilon a los estados dados y devuelve todos los estados alcanzables.
        """
        # Inicializar una lista con los estados iniciales
        resultado = estados.copy()
        # Inicializar una pila con los estados iniciales
        pila = estados.copy()
        # Mientras la pila no esté vacía
        while pila:
            # Obtener el siguiente estado de la pila
            actual = pila.pop()
            # Obtener todas las transiciones epsilon desde el estado actual
            epsilon_transiciones = [
                t[2] for t in self.transiciones_splited if t[0] == actual and t[1] == "ε"]
            # Para cada estado alcanzable a través de una transición epsilon
            for e in epsilon_transiciones:
                # Si el estado no está en el resultado
                if e not in resultado:
                    # Agregar el estado al resultado y a la pila
                    resultado.append(e)
                    pila.append(e)
        # Devolver todos los estados alcanzables
        return resultado

    # metodo para simular una cadena en un afn
    def simular_cadena(self, cadena):
        estados_actuales = self.cerradura_epsilon([self.e0])
        estados_finales = []
        for simbolo in cadena:
            nuevos_estados = []
            for estado in estados_actuales:
                for transicion in self.transiciones_splited:
                    if estado == transicion[0] and simbolo == transicion[1]:
                        nuevos_estados.append(transicion[2])
            if not nuevos_estados:
                return False
            estados_actuales = self.cerradura_epsilon(nuevos_estados)
        estados_finales = self.cerradura_epsilon(estados_actuales)
        return self.ef in estados_finales

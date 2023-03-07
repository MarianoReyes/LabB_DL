"""
Laboratorio B
José Mariano Reyes 
20074
"""

from Regex_Postfix import convertExpression
from Postfix_AFN import PostifixToAFN
from AFN_AFD import AFNtoAFD

# main del programa
if __name__ == '__main__':
    # Simbolo epsilon  ε
    exp = input("\nIngrese una expresion a convertir: ")

    #exp = "(b|b)*abb(a|b)*"
    print("\nRegex: ", exp)

    conversion = convertExpression(len(exp))

    # llamada de funcion para convertir a postfix
    conversion.RegexToPostfix(exp)
    if conversion.ver == True:
        postfix = conversion.res

        # instancia de clase para convertir a AFN
        conversionAFN = PostifixToAFN(postfix)

        # llamada a metodo para convertir afn
        conversionAFN.conversion()

        # SIMULACION AFN
        cadena = input("\nIngrese una cadena para simular en AFN:\n-> ")
        acepta_cadena = conversionAFN.simular_cadena(cadena)
        if acepta_cadena:  # devuelve True
            print(f"\nLa cadena '{cadena}' es aceptada por el AFN.")
        else:
            print(f"\nLa cadena '{cadena}' NO es aceptada por el AFN.")

        # instancia de clase para convertir AFN a AFD
        conversionAFD = AFNtoAFD(conversionAFN.e0, conversionAFN.ef,
                                 conversionAFN.estados, conversionAFN.simbolos, conversionAFN.transiciones_splited)

        conversionAFD.construir_afd()

        # SIMULACION AFD
        cadena = input("\nIngrese una cadena para simular en AFD:\n-> ")
        acepta_cadena = conversionAFD.simular_cadena(conversionAFD.e0, cadena)
        if acepta_cadena:  # devuelve True
            print(f"\nLa cadena '{cadena}' es aceptada por el AFD.")
        else:
            print(f"\nLa cadena '{cadena}' NO es aceptada por el AFD.")

        # instancia de clase para convertir a AFD de forma Directa

    else:
        print("\nSe ha finalizado el programa por una mala expresión Regex")

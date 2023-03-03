"""
Laboratorio B
José Mariano Reyes 
20074
"""

from Regex_Postfix import convertExpression
from Postfix_AFN import PostifixToAFN
from AFN_AFD import AFNToAFD

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

        # instancia de clase para convertir a AFD
        conversionAFD = AFNToAFD(conversionAFN.e0, conversionAFN.ef,
                                 conversionAFN.estados, conversionAFN.simbolos, conversionAFN.transiciones_splited)

        conversionAFD.conversion()
        conversionAFD.graficar_afd()
    else:
        print("\nSe ha finalizado el programa por una mala expresión Regex")

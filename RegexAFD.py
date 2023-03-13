
def regex(expresion, isAFD=False):
    first = []
    regex_list = []
    last_index = 0
    i = 0

    SpecialCases = {
        'positive_closure_group': ')+',
        'null_check_group': ')?',
        'positive_closure': '+',
        'null_check': '?',
    }

    # Primer caso especial
    if expresion.find(SpecialCases['positive_closure_group']) != -1:
        for i in range(len(regex)):
            if expresion[i] == '(':
                first.append(expresion[i])  # guarda index

            # la posicion actual
            if expresion[i] == ')' and i < len(expresion) - 1:
                regex_list.append(expresion[i])

                # Para ver si el siguiente elemento es del positive group
                if expresion[i+1] == '+':
                    last_index = i+1  # la siguiente posicion
                    regex_list.append('*')
                    regex_list.append(expresion[first.pop(): last_index])
                    i = i+1
                else:
                    first.pop()
            else:
                # si no es el cierre del parentesis lo agrega a la lista
                regex_list.append(expresion[i])

    # Segundo caso especial
    if expresion.find(SpecialCases['null_check_group']) != -1:
        for i in range(len(regex)):
            if expresion[i] == '(':
                first.append(i)

            if expresion[i] == ')':
                regex_list.append(expresion[i])  # pos actual
                if expresion[i + 1] == '?':  # si la siguiente posicion es ?
                    last_index = i + 1
                    regex_list.append('|')
                    regex_list.append('ε')
                    regex_list.append(')')
                    regex_list.insert(first[-1], '(')
                    i = i + 1
                else:
                    first.pop()

            else:
                regex_list.append(expresion[i])

        expresion = ''.join(regex_list)

    resultado = expresion

    # Tercer caso especial
    if expresion.find(SpecialCases['positive_closure']) != -1:
        while resultado.find(SpecialCases['positive_closure']) != -1:
            i = resultado.find('+')
            symbol = resultado[i - 1]

            resultado = resultado.replace(
                symbol + '+', '(' + symbol + '*' + symbol + ')')

    # Cuarto caso especial
    if expresion.find(SpecialCases['null_check']) != -1:
        while resultado.find(SpecialCases['null_check']) != -1:
            i = resultado.find('?')
            symbol = resultado[i - 1]

            resultado = resultado.replace(
                symbol + '?', '(' + symbol + '|' + 'ε' + ')')

    if(isAFD == True):
        resultado = '(' + resultado + ')#'  # quite el #
        # El # avisa que es el final de la expresion

    return concatenacion(resultado)


def concatenacion(regex):
    operadores = ['(', '*', '|', '?', '+']
    encadenado = ''

    for i in range(len(regex)):
        if i+1 >= len(regex):
            encadenado += regex[-1]
            break
        if regex[i] == '*' and regex[i+1] != ')' and not (regex[i+1] in operadores):
            encadenado += regex[i]+'.'
        elif regex[i] == '*' and regex[i+1] == '(':
            encadenado += regex[i]+'.'
        elif regex[i] == '?' and regex[i+1] != ')' and not (regex[i+1] in operadores):
            encadenado += regex[i]+'.'
        elif regex[i] == '?' and regex[i+1] == '(':
            encadenado += regex[i]+'.'
        elif not (regex[i] in operadores) and regex[i+1] == ')':
            encadenado += regex[i]
        elif (not (regex[i] in operadores) and not (regex[i+1] in operadores)) or (not (regex[i] in operadores) and (regex[i+1] == '(')):
            encadenado += regex[i]+'.'
        else:
            encadenado += regex[i]

    return encadenado

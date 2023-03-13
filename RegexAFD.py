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
        for i in range(len(expresion)):
            if expresion[i] == '(':
                first.append(i)  # guarda index

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
        for i in range(len(expresion)):
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

            if i > 1 and resultado[i-2:i] == ')*':
                # caso cerradura positiva de grupo en parentesis
                end_group = i-2
                while resultado[end_group] != '(':
                    end_group -= 1

                start_group = first.index(end_group)
                resultado = resultado[:start_group] + \
                    resultado[end_group:i] + resultado[i:].replace(
                        symbol + '+', '(' + symbol + '*' + symbol + ')', 1)
                first = first[:start_group] + \
                    [end_group] + first[start_group:]
            else:
                resultado = resultado.replace(
                    symbol + '+', '(' + symbol + '*' + symbol + ')')

    # Cuarto caso especial
    if expresion.find(SpecialCases['null_check']) != -1:
        while resultado.find(SpecialCases['null_check']) != -1:
            i = resultado.find('?')
            symbol = resultado[i - 1]

            # Reemplaza el simbolo seguido de ? con una expresion alternativa que puede ser el simbolo o vacio (ε)
            resultado = resultado.replace(
                symbol + '?', '(' + symbol + '|' + 'ε' + ')')

    # Quinto caso especial
    if expresion.find('|?') != -1:
        while resultado.find('|?') != -1:
            i = resultado.find('|?')
            left = i - 1
            right = i + 2
            left_parenthesis_count = 1

            # Busca el inicio del parentesis izquierdo
            while left >= 0 and left_parenthesis_count > 0:
                if resultado[left] == ')':
                    left_parenthesis_count += 1
                elif resultado[left] == '(':
                    left_parenthesis_count -= 1
                left -= 1

            # Si hay un parentesis izquierdo, reemplaza la expresion '|?' por '|ε' y envuelve la expresion en parentesis para limitar el efecto del operador '|'
            if left >= 0:
                resultado = resultado[:left] + \
                    '(' + resultado[left+1:right] + '|ε)' + resultado[right:]

    # Sexto caso especial
    if expresion.find('+?') != -1:
        while resultado.find('+?') != -1:
            i = resultado.find('+?')
            left = i - 1
            right = i + 2
            left_parenthesis_count = 1

            # Busca el inicio del parentesis izquierdo
            while left >= 0 and left_parenthesis_count > 0:
                if resultado[left] == ')':
                    left_parenthesis_count += 1
                elif resultado[left] == '(':
                    left_parenthesis_count -= 1
                left -= 1

            # Si hay un parentesis izquierdo, reemplaza la expresion '+?' por '*?' y envuelve la expresion en parentesis para limitar el efecto del operador '*'
            if left >= 0:
                resultado = resultado[:left] + \
                    '(' + resultado[left+1:right-1] + \
                    ')*?' + resultado[right:]

    if(isAFD == True):
        resultado = '(' + resultado + ')#'  # quite el #
        # El # avisa que es el final de la expresion

    return concatenacion(resultado)

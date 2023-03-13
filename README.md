# Laboratorio B

Programa encargado de implementar la conversión de una expresión Regex a AFN pasando por postfix de primero, luego AFN a AFD y por último la Minimización. De igual manera se implementa la construcción de AFD de manera directa. La ejecución se realiza con el comando:

- python labB.py

## Clases

- Regex a Postfix
- Postfix a AFN
- AFN a AFD
- Minimización de AFD

## Gramaticas Soportadas

- r = (a)
- r = ab
- r = a|b
- r = a\*
- r = a+
- r = a?
- r = ϵ

## Observaciones

Es necesario tener graphviz instalado en la computadora y agregado al PATH en las variables de entorno. Para obviar la implementación gráfica remover la linea 264 del archivo Postfix_AFN.py

**EN LA REGEX NO VAN PUNTOS DE CONCATENACIÓN, LOS AGREGA AUTOMÁTICAMENTE**

# Laboratorio A

Programa encargado de implementar la conversión de una expresión Regex a AFN pasando por postfix de primero. La ejecución se realiza con el comando

- python labA.py

## Clases

- Regex a Postfix
- Postfix a AFN

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

- self.graficar() # imagen del AFN

El ejemplo usado para los archivos generados en el repositorio fue:

- 0?(1?)?0\*

**EN LA REGEX NO VAN PUNTOS DE CONCATENACIÓN, LOS AGREGA AUTOMÁTICAMENTE**

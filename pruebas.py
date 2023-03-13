from AFD_directo import AFD
from RegexAFD import *

# Simbolo epsilon  ε
exp = input("\nIngrese una expresion a convertir: ")

# convertir de regex a AFD
regext = regex(exp, True)
AFD_directo = AFD(regext)

# simulacion de string
cadena = input(
    "\nIngrese una cadena para simular en AFD directo:\n-> ")
acepta_cadena = AFD_directo.simulate_string(cadena)
if acepta_cadena:  # devuelve True
    print(f"\nLa cadena '{cadena}' es aceptada por el AFD directo.")
else:
    print(f"\nLa cadena '{cadena}' NO es aceptada por el AFD directo.")

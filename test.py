from modelo import resolver_asignacion_tribunales
from testConConsecutividad import resolver_asignacion_tribunalesPlus
import random
# Ejemplo de uso

#Tribunales = [[random.randint(1, 45) for _ in range(3)] for _ in range(50)]
#
#Ct = [random.randint(1, 2) for _ in range(50)]
#d = 5
#l = 5
#h = 4

Tribunales = [[1,2,3],[3,4,5]]

Ct = [1,1]
d = 1
l = 1
h = 2



msg, resultado = resolver_asignacion_tribunalesPlus(Tribunales, Ct, d, l, h)
print(msg)
print(resultado)

# Imprimir los resultados en lenguaje 
if resultado is not None:  # Verifica que haya asignaciones
    for tribunal, asignaciones in resultado.items():
        print(f"Asignaciones para el tribunal {tribunal}:")
        for asignacion in asignaciones:
            dia, lugar, hora = asignacion
            print(f"El tribunal {tribunal} está asignado para atender una tesis el día {dia}, en el lugar {lugar}, a la hora {hora}.")
else:
    print("No se encontraron asignaciones.")

# # Llamada a la función creando_T
# T, total_personas = creando_T(Tribunales)

# # Imprimir resultado
# print("Matriz T:")
# for fila in T:
#     print(fila)
# print("Total de personas:", total_personas)
from modelo import resolver_asignacion_tribunales
import random
from save import save, get_data

# Ejemplo de uso

Tribunales = [[random.randint(1, 20) for _ in range(3)] for _ in range(20)]

d = 4
l = 2
h = 7

restricciones = {1: {"d": [], "l": [0], "h": []}, 3: {"d": [1, 2], "l": [], "h": []}}

data = get_data("")
resultado = resolver_asignacion_tribunales(Tribunales, d, l, h, restricciones)
print(resultado)

# Imprimir los resultados en lenguaje
if (
    resultado is not None and type(resultado) is not str
):  # Verifica que haya asignaciones
    for tribunal, asignaciones in resultado.items():
        print(f"Asignaciones para el tribunal {tribunal}:")
        for asignacion in asignaciones:
            dia, lugar, hora = asignacion
            print(
                f"El tribunal {tribunal} está asignado para atender una tesis el día {dia}, en el lugar {lugar}, a la hora {hora}."
            )
    save(resultado)
else:
    print("No se encontraron asignaciones.")

# # Llamada a la función creando_T
# T, total_personas = creando_T(Tribunales)

# # Imprimir resultado
# print("Matriz T:")
# for fila in T:
#     print(fila)
# print("Total de personas:", total_personas)

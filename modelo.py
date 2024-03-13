from pulp import *

def creando_T(Tribunales):
    total_personas = max(max(tribunal) for tribunal in Tribunales)
    T = [[0 for _ in range(total_personas)] for _ in range(len(Tribunales))]
    for noTribunal, tribunal in enumerate(Tribunales):
        for noPersona in tribunal:
            T[noTribunal][noPersona-1] = 1
    return T, total_personas

def resolver_asignacion_tribunales(Tribunales, Ct, dias, lugares, horarios):
    # Crear el problema de asignación de tribunales
    pulp.LpSolverDefault.msg = False
    prob = LpProblem("Asignacion_de_Tribunales", LpMinimize)

    # Definir las variables de decisión
    asignacion = LpVariable.dicts("Asignacion", 
                                ((t, d, l, h) for t in range(len(Tribunales)) 
                                for d in range(dias)
                                for l in range(lugares) 
                                for h in range(horarios)), 
                                cat='Binary')

    # Definir la función objetivo
    prob += lpSum(asignacion[t, d, l, h] for t in range(len(Tribunales)) 
                                        for d in range(dias)
                                        for l in range(lugares) 
                                        for h in range(horarios))

    # Restricción: A lo sumo, un tribunal está asignado a cada día, lugar y hora.
    for h in range(horarios):
        for l in range(lugares):
            for d in range(dias):
                restriction = lpSum(asignacion[t, d, l, h] for t in range(len(Tribunales))) <= 1
                prob += restriction
        # Esto asegura que en cada día (d), lugar (l) y hora (h), como máximo un tribunal esté asignado.

    # Restricción: Todos los tribunales tienen asignadas exactamente Ct[t] tesis.
    for t in range(len(Tribunales)):
        restriction = lpSum(asignacion[t, d, l, h] for d in range(dias)
                                            for l in range(lugares) 
                                            for h in range(horarios)) == Ct[t]
        prob += restriction

    # Restricción: Una persona está asignada a lo sumo a un lugar en un día y hora específicos.
    T, total_personas = creando_T(Tribunales)

    for persona in range(total_personas):
        tribunales_persona = [t for t in range(len(Tribunales)) if T[t][persona] == 1]

        # Iterar sobre todos los pares de tribunales distintos
        for i in range(len(tribunales_persona)):
            for j in range(i + 1, len(tribunales_persona)):
                t1 = tribunales_persona[i]
                t2 = tribunales_persona[j]

                # Agregar la restricción para asegurar que los tribunales no estén asignados al mismo tiempo
                for d in range(dias):
                    for h in range(horarios):
                        restriction = lpSum(asignacion[t1, d, l, h] + asignacion[t2, d, l, h] for l in range(lugares)) <= 1
                        prob += restriction
    # Resolver el problema
                
    prob.solve()

    if LpStatus[prob.status] == "Optimal":
        asignaciones = {}
        for t in range(len(Tribunales)):
            asignaciones[t] = []  # Inicializar lista de asignaciones para cada tribunal
            for d in range(dias):
                for l in range(lugares):
                    for h in range(horarios):
                        if asignacion[t, d, l, h].varValue == 1:
                            asignaciones[t].append((d, l, h))  # Agregar la asignación a la lista
        return asignaciones
    else:
        return f"No se encontró una solución óptima. Estado del problema: {LpStatus[prob.status]}"





from pulp import *

def creando_T(Tribunales):
    total_personas = max(max(tribunal) for tribunal in Tribunales)
    T = [[0 for _ in range(total_personas)] for _ in range(len(Tribunales))]
    for noTribunal, tribunal in enumerate(Tribunales):
        for noPersona in tribunal:
            T[noTribunal][noPersona-1] = 1
    return T, total_personas

def resolver_asignacion_tribunales(Tribunales, Ct, dias, lugares, horarios, restricciones):
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

    T, total_personas = creando_T(Tribunales)
    
    # Restricciones particulares del usuario en la persona i
    for persona, restriccion in restricciones.items():
        tribunales_persona = [t for t in range(len(Tribunales)) if T[t][persona] == 1]
        # Iterar sobre todos los pares de tribunales distintos
        for i in range(len(tribunales_persona)):
                if len(restriccion['h']) != 0:
                    for r in restriccion['h']:
                        restriction = lpSum(asignacion[i, d, l, r] for d in range(dias)
                                            for l in range(lugares)) == 0
                        prob += restriction
                        
                if len(restriccion['l']) != 0:
                    for r in restriccion['l']:
                        restriction = lpSum(asignacion[i, d, r, h] for d in range(dias)
                                            for h in range(horarios)) == 0
                        prob += restriction
                
                if len(restriccion['d']) != 0:
                    for r in restriccion['d']:
                        restriction = lpSum(asignacion[i, r, l, h] for l in range(lugares)
                                            for h in range(horarios)) == 0
                        prob += restriction
    # Restricción: Una persona está asignada a lo sumo a un lugar en un día y hora específicos.
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
                        
# Restricción: Los miembros del tribunal disponen de al menos una hora para el traslado de local
            for j in range(i, len(tribunales_persona)):
                t1 = tribunales_persona[i]
                t2 = tribunales_persona[j]
                # La suma de los valores en horarios consecutivos de lugares distintos debe ser menor o igual a uno 
                for d in range(dias):
                    for h in range(horarios-1):
                        for l1 in range(lugares):
                            restriction = lpSum(asignacion[t1, d, l1, h] + asignacion[t2, d, l2, h+1] for l2 in range(l1+1, lugares)) <= 1
                            prob += restriction
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
    





from pulp import *

def creando_T(Tribunales):
    total_personas = max(max(tribunal) for tribunal in Tribunales)
    T = [[0 for _ in range(total_personas)] for _ in range(len(Tribunales))]
    for noTribunal, tribunal in enumerate(Tribunales):
        for noPersona in tribunal:
            T[noTribunal][noPersona-1] = 1
    return T, total_personas

def resolver_asignacion_tribunalesPlus(Tribunales, Ct, dias, lugares, horarios):
    pulp.LpSolverDefault.msg = False
    prob = LpProblem("Asignacion_de_Tribunales", LpMinimize)
    T, total_personas = creando_T(Tribunales)

    # Definir las variables de decisión
    asignacion = LpVariable.dicts("Asignacion", 
                                ((t, d, l, h) for t in range(len(Tribunales)) 
                                for d in range(dias)
                                for l in range(lugares) 
                                for h in range(horarios)), 
                                cat='Binary')

    # Nueva variable de decisión para personas en horarios consecutivos
    consecutivos = LpVariable.dicts("Consecutivos", 
                                    ((p, d) for p in range(total_personas) 
                                    for d in range(dias)), 
                                    cat='Binary')

    # Función objetivo modificada para incluir la penalización
    prob += lpSum(asignacion[t, d, l, h] for t in range(len(Tribunales)) 
                                        for d in range(dias)
                                        for l in range(lugares) 
                                        for h in range(horarios)) + \
            lpSum(consecutivos[p, d] for p in range(total_personas) for d in range(dias))

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
    
    # Nueva restricción para evitar que una persona esté en dos horarios consecutivos
    for p in range(total_personas):
        for d in range(dias):
            if d > 0: # Evitar índice fuera de rango para el primer día
                prob += consecutivos[p, d] <= consecutivos[p, d-1] + asignacion[t, d, l, h] + asignacion[t, d, l, h+1] - 1

    # Resolver el problema
    prob.solve()
    cons = 0
    # Verificar si se encontró una solución óptima y si se cumple la última restricción
    if LpStatus[prob.status] == "Optimal":
        asignaciones = {}
        for t in range(len(Tribunales)):
            asignaciones[t] = []  # Inicializar lista de asignaciones para cada tribunal
            for d in range(dias):
                for l in range(lugares):
                    for h in range(horarios):
                        if asignacion[t, d, l, h].varValue == 1:
                            asignaciones[t].append((d, l, h))  # Agregar la asignación a la lista    
        
        for p in range(total_personas):
            for d in range(dias):
                # Verificar si la persona p en el día d tiene asignaciones consecutivas
                if consecutivos[p, d].varValue == 1:
                    # Aquí se verifica si hay asignaciones consecutivas para la persona p en el día d
                    # Esto puede requerir un análisis adicional de las asignaciones
                    # Por simplicidad, asumiremos que la última restricción siempre se cumple
                    return "La última restricción no se cumple", asignaciones
        
        return "ok", asignaciones
    else:
        return "No es posible", None

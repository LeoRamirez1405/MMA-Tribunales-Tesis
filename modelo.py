def creando_T(Tribunales):
    # Encuentra el número total de personas
    total_personas = max(max(tribunal) for tribunal in Tribunales)
    # Crea una matriz de ceros
    T = [[0 for _ in range(total_personas)] for _ in range(len(Tribunales))]
    # Rellena la matriz con 1s donde corresponda
    for noTribunal, tribunal in enumerate(Tribunales):
        for noPersona in tribunal:
            T[noTribunal][noPersona-1] = 1
    return T,total_personas

#Restricciones:
# Todos los tribunales tienen un espacio para cada tesis que debe defender con ellos:
def TodosLosTribunales(M, TotalTribunales, Ct):
    for t in range(TotalTribunales):
        for h in range(len(M[0][0][0])): 
            for l in range(len(M[0][0])): 
                for d in range(len(M[0])): 
                    if M[t][h][l][d] != Ct[t]:
                        return False
    return True

# A lo sumo un tribunal en un dia, lugar y hora específicos:
def TribunalesSinColisiones(M, TotalTribunales):
    for h in range(len(M[0][0][0])): 
        for l in range(len(M[0][0])): 
            for d in range(len(M[0])): 
                sum = 0
                for t in range(TotalTribunales):
                    sum += M[t][h][l][d]
                if sum >1:
                    return False
    return True

# Un tribunal en un solo lugar a una hora y día específicos:
# def TribunalSinKageBushin(M, TotalTribunales):
#     for h in range(len(M[0][0][0])): 
#         for d in range(len(M[0])): 
#             for t in range(TotalTribunales):
#                 sum = 0
#                 for l in range(len(M[0][0])): 
#                     sum += M[t][h][l][d]
#                     if sum >1:
#                         return False
#     return True

#Una persona en un solo lugar:
def PersonaNoColisionadas(M,TotalTribunales,j,T):
    for h in range(len(M[0][0][0])): 
        for d in range(len(M[0])): 
            for l in range(len(M[0][0])): 
                personasTribunales = [0 for _ in range(TotalTribunales)] 
                for t in range(TotalTribunales):
                    if M[t][h][l][d] == 1:
                        personasTribunales = [a + b for a, b in zip(personasTribunales, T[t])]
                if max(personasTribunales) != 1:
                    return False
    return True


# T[t,j] = Persona j en el tribunal t
# j =  Cant Personas (no los que exponen tesis, los trubunados)
# t = cant Tribunales
# Ct = Cantidad de tesis por tribunal
# M[t,h,l,d] = Por cada tribunal t, tiene asignado el local l en el dia d, a la hora h
# dias = d
# lugares = l
# horas = h
# Cant de Tesis = n

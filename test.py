from modelo import *

Tribunales = [[1,2,3],[1,4,5]]
Ct = [3,4]
d = 3
l = 4
h = 4

def Asignacion(Tribunales, Ct, d, l, h):
    T, j = creando_T(Tribunales)
    t = len(T)
    n = sum(Ct)
    M = [[[[0 for d in range(d)] for l in range(l)] for h in range(h)] for t in range(t)]
    
    pass

resultado = Asignacion(Tribunales, Ct, d, l, h)
print(resultado)
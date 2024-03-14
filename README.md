# MMA-Tribunales-Tesis
## Informe sobre el Código de Asignación de Tribunales con PuLP y uso del software:
Este informe describe el código proporcionado, que utiliza la biblioteca PuLP para resolver un problema de asignación de tribunales. `PuLP` es una biblioteca de modelado de programación lineal en Python que permite generar archivos `MPS` o `LP` y llamar a solvers como `GLPK, COIN-OR CLP/CBC, CPLEX, GUROBI, MOSEK, XPRESS, CHOCO, MIPCL, HiGHS, SCIP/FSCIP` para resolver problemas lineales.

### Descripción General:
#### El código define dos funciones principales:
`creando_T(Tribunales):` Esta función crea una matriz T que representa la asignación de personas a tribunales. La matriz `T` es una matriz binaria donde `T[i][j]` es 1 si la persona `j+1` está asignada al tribunal `i+1`, y 0 en caso contrario. La función también devuelve el número total de personas.
`resolver_asignacion_tribunales(Tribunales, Ct, dias, lugares, horarios, restricciones):` Esta función resuelve el problema de asignación de tribunales utilizando `PuLP`. Define un problema de optimización donde el objetivo es minimizar el número total de asignaciones de tribunales a días, lugares y horarios, sujeto a varias restricciones.
#### Detalles de la Implementación:
`Creación de la Matriz de Asignación:`
La función `creando_T` itera sobre cada tribunal y cada persona en el tribunal, asignando un valor de 1 a la posición correspondiente en la matriz T. Esto permite representar la asignación de personas a tribunales de manera eficiente.

`Definición del Problema de Optimización:`
El problema de optimización se define utilizando `PuLP`. Se definen variables de decisión binarias para cada combinación de tribunal, día, lugar y hora, representando si un tribunal está asignado a un día, lugar y hora específicos. La función objetivo es minimizar el número total de asignaciones.

`Restricciones:`
El código implementa varias restricciones para garantizar que la asignación de tribunales sea factible:
- Cada día, lugar y hora puede tener asignado a lo sumo un tribunal.
- Cada tribunal debe tener asignadas exactamente Ct[t] tesis.
- Se aplican restricciones específicas para ciertas personas, como restricciones de horario, lugar y día.
- Una persona está asignada a lo sumo a un lugar en un día y hora específicos.
- Los miembros del tribunal disponen de al menos una hora para el traslado de local.
Resolución del Problema

El problema se resuelve utilizando el método `solve()` de `PuLP`. Si se encuentra una solución óptima, el código devuelve un diccionario con las asignaciones de tribunales. Si no se encuentra una solución óptima, se devuelve un mensaje indicando el estado del problema.

### Utilización del programa:
#### Para utilizar correctamente el programa de asignación de tribunales, es necesario proporcionar los datos necesarios en el formato adecuado. A continuación, se detallan los pasos para introducir los datos:

1. `Definir los Tribunales:` Los tribunales se representan como una lista de listas, donde cada sublista contiene los números de las personas asignadas a ese tribunal. Por ejemplo:
```python
Tribunales = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
```
Cada sublista representa un tribunal y los números dentro de la sublista representan las personas asignadas a ese tribunal.

2. `Definir el número de tesis por tribunal (Ct):` Se debe proporcionar una lista con el número de tesis que cada tribunal debe atender. Por ejemplo:

```python
Ct = [2, 1, 3]
```

Esta lista debe tener la misma longitud que la lista de tribunales, indicando cuántas tesis debe atender cada tribunal.

3. `Definir los parámetros de días, lugares y horarios:` Estos parámetros representan las opciones disponibles para asignar los tribunales. Por ejemplo:

```python
d = 5 # Días disponibles
l = 3 # Lugares disponibles
h = 8 # Horarios disponibles
```

Estos valores determinan el rango de opciones para asignar los tribunales a días, lugares y horarios.

4. `Definir las restricciones:` Las restricciones se aplican a ciertas personas y pueden incluir restricciones de día, lugar y hora. Por ejemplo:

``` python
restricciones = {
    1: {'d': [1, 2], 'l': [0], 'h': []},
    3: {'d': [3, 4], 'l': [1], 'h': []}
}
```

Esta estructura indica que la persona 1 no puede ser asignada en los días 1 y 2, en el lugar 0, y la persona 3 no puede ser asignada en los días 3 y 4, en el lugar 1. Las restricciones de hora se pueden especificar de manera similar.

Una vez que se han definido estos datos, se puede llamar a la función resolver_asignacion_tribunales con los parámetros adecuados para resolver el problema de asignación. La función devuelve un diccionario con las asignaciones de tribunales, que luego se pueden imprimir o guardar utilizando la función save.

Es `importante` asegurarse de que los datos proporcionados sean coherentes con las restricciones y los parámetros definidos. Por ejemplo, el número de tribunales en `Tribunales` debe coincidir con la longitud de `Ct`, y los números de personas en cada tribunal deben estar dentro del rango de total_personas definido por el programa.

### Representando los resultados:

Para representar en Excel una matriz donde cada fila represente una hora y cada columna un lugar, y en la posición i,j este el tribunal que tiene hora i y lugar j, necesitas transformar tus datos de manera que cada combinación única de hora y lugar tenga asignado un tribunal. Esto se puede lograr utilizando la función `pivot_table` de pandas, que permite reorganizar los datos en un formato tabular.

1. **Preparar los datos**: Se asegura que el DataFrame `df` tenga las columnas 'Hora', 'Lugar' y 'Tribunal'.

2. **Crear la matriz**: Se utiliza `pivot_table` para crear la matriz. La función `pivot_table` toma como argumentos el DataFrame, los valores que se deben colocar en las celdas de la matriz (en este caso, 'Tribunal'), y los índices y columnas que definen la estructura de la matriz (en este caso, 'Hora' y 'Lugar').

```python
# Crear la matriz
matriz = df.pivot_table(values='Tribunal', index='Hora', columns='Lugar', aggfunc='first')
```

3. **Guardar la matriz en Excel**: Ahora que se tiene la matriz en el formato deseado, puede guardarse en un archivo Excel. Para hacerlo, se utiliza el método `to_excel` de pandas.

```python
# Guardar la matriz en Excel
with pd.ExcelWriter('./data/horarios_matriz.xlsx') as writer:
    matriz.to_excel(writer, sheet_name='Matriz de Horarios', index=True)
```

Este código creará un archivo Excel llamado `horarios_matriz.xlsx` con una hoja llamada 'Matriz de Horarios'. Cada fila representará una hora, cada columna un lugar, y en la celda i,j se encontrará el tribunal asignado a esa hora y lugar.

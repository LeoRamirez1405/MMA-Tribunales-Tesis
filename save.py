import pandas as pd

def save(resultados):
    # Transformar el diccionario en un DataFrame
    df = pd.DataFrame([(d, t, 'Lugar_'+str(l), h) for d, schedules in resultados.items() for t, l, h in schedules],
                    columns=['Tribunal', 'Día', 'Lugar', 'Hora'])

    # Crear un nuevo libro de trabajo de Excel
    with pd.ExcelWriter('./data/horarios_matriz.xlsx') as writer:
        # Ordenar los días de forma ascendente
        sorted_days = sorted(df['Día'].unique())
        
        # Para cada día único en el DataFrame
        for day in sorted_days:
            # Filtrar el DataFrame para el día actual 
            df_day = df[df['Día'] == day]
            # Crear la matriz para el día actual
            matriz = df_day.pivot_table(values='Tribunal', index='Hora', columns='Lugar', aggfunc='first')
            
            # Guardar el DataFrame final en una hoja de Excel con el nombre del día
            matriz.to_excel(writer, sheet_name=str('Day_'+str(day)), index=True)






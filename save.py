import pandas as pd
import numpy as np
import datetime


def get_data(path):
    path = './data/Tribulanes/CC-2023.xlsx'
    df = pd.read_excel(path)
    
    # columns = df.columns.to_list()
    # for col in columns:
    #     print(col)
    days = [day for day in df['Día'].tolist() if isinstance(day, datetime.date)]
    hours = [hour for hour in df['Hora '].tolist() if isinstance(hour, datetime.time)]
    places = [place for place in df['Lugar'].tolist() if isinstance(place, str)]
    # thesis_panel = []
    thesis_panel = set([])
    print('set: ', thesis_panel)
    
    columns = df[['Tutor', 'Presidente', 'Secretario', 'Vocal', 'Oponente']]
    for index, row in columns.iterrows():
        # panel = []
        panel = set([])
        for col in columns:
            member = row[col]
            # print(type(member))
            if type(member) == str:
                # panel.append(member)
                panel.add(member)
        if len(panel) > 0:
            thesis_panel.add(frozenset(panel))
            
    thesis_panel = [list(panel) for panel in thesis_panel]
    for panel in thesis_panel:
        print(panel)
    print(len(thesis_panel))
            
    return days, thesis_panel, places, hours 
            
    # print('days: \n', days)
    # print('hours: \n', hours)
    # print('places: \n', places)
    # print('thesis_panel: \n', thesis_panel)


    
    
    
    # # Imprimir las primeras filas del DataFrame
    # print(df.columns)


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


get_data('')



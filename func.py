import pandas as pd
from datetime import datetime, date
import matplotlib.pyplot as plt
from points_for_actions import POINTS as p

# Сюда бы еще описание закидывать след. колонкой

def write_to_databse(direction, sub_direction, points, action,state_for_database, desc):

    formatted_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    lst = [[formatted_datetime, direction, sub_direction, points, action, desc]]

    new_df = pd.DataFrame(lst, columns=['datetime', 'direction','sub_direction', 'points','action','description'])

    # Записываем данные в CSV (append mode)
    if state_for_database:
        new_df.to_csv('data_history_prod.csv', mode='a', index=False, header=False, encoding='utf-8')
    else:
        new_df.to_csv('data_history_dev.csv', mode='a', index=False, header=False, encoding='utf-8')
    return 'Запись сделана'

# write_to_databse('social','sex',100)




def bar_points(points_y, points_m, points_w):


    target_social = p['sex']*5 + p['courses']*5*3 + p['meeting']*4*12 + p['touch']*5*50 + p['social_book']*30*320
    target_health = p['training']*3*50 + p['stretching']*2*340 + p['eating']*350
    target_finance = p['finance_studing']*30*350
    target_studing = p['ds_python_studing']*60*350 + p['english']*20*350

    total_points_per_year = target_social + target_health + target_finance + target_studing
    dict_period = {
    'year': {
        'name': 'Суммарное количество очков за год',
        'total_points': round(total_points_per_year),
        'points': points_y,
        'divider':12
    },
    'month': {
        'name': 'Суммарное количество очков за месяц',
        'total_points': round(total_points_per_year / 12),
        'points': points_m,
        'divider':4
    },
    'week': {
        'name': 'Суммарное количество очков за неделю',
        'total_points': round(total_points_per_year / 50),
        'points': points_w,
        'divider':7
        }
    }

    # Создание фигуры и субплотов
    fig, ax = plt.subplots(figsize=(8, 2), nrows=3, gridspec_kw={'hspace': 0.9})

    # Обход субплотов циклом
    for i, title in enumerate(dict_period):

        fact_points = dict_period[title]['points']
        total_points = dict_period[title]['total_points']
        title_bar = dict_period[title]['name']
        divider_for_bar = dict_period[title]['divider']

        # Построение гистограммы
        ax[i].barh(y=0, width=fact_points, color='#3ce580', height=0.1, label=f'Заполнено {fact_points}')

        line = round(total_points / divider_for_bar)
        for line_points in range(line,total_points,line):
            ax[i].axvline(x=line_points, color='black', linewidth = 0.5, alpha = 0.5)

        # Настройка осей
        ax[i].set_xlim(0, total_points)
        ax[i].set_title(title_bar, fontsize=10)
        ax[i].xaxis.set_visible(False)
        ax[i].yaxis.set_visible(False)

        # Добавление текста внутри бара
        ax[i].text(fact_points / 2, 0, f'{int(fact_points)}', color='black', va='center', ha='center', size=10)
        ax[i].text(total_points + total_points * 0.02, 0, f'{int(total_points)}', color='black', va='center', size=10)

    plt.savefig('bar_chart.png', bbox_inches='tight')  # Сохраняем как файл PNG
    plt.close(fig)

    #plt.show()

POINTS: dict[str, float] = {
    # Social
    'courses': 30,
    'sex': 150, # Разные девушки
    'meeting': 35,
    'touch':15,
    # За минуту чтения
    'social_book':0.25,


    # Health
    'training': 20,
    'stretching': 2,
    'eating': 3,

    # Finance
    # Тоже минута занятий
    'finance_studing': 0.33,

    # Studing
    # Тоже минута занятий
    'ds_python_studing': 0.2,
    'english':0.5
    }

# По идее у нас должна быть цель на год, месяц, неделю.
# Также должны быть min, avg, max цели.
# Пока сделаем
POINTS_TARGET: dict[str, float] = {

    # Годовой объем
    'social':3000,
    'finance': 1600,
    'health': 4500,
    'ds_python_studing':3000

}
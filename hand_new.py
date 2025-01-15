from aiogram import F, Router
from aiogram.filters import CommandStart,Command
from aiogram.types import Message,FSInputFile, BotCommand
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from keybords import direction, direction_social,direction_health,direction_finance,direction_ds
from lexicon_ru import LEXICON_RU
from points_for_actions import POINTS
from func import write_to_databse, bar_points
import pandas as pd
from datetime import datetime, date


API_TOKEN = '7923040381:AAGq_IWqljso21A6M1z_Ey6qXZl7LplIQnA'
state_for_database = True
file_path = 'data_history_prod.csv'


bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())  # Подключаем память для FSM


async def set_main_menu(bot: Bot):

    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Запуск бота'),
        BotCommand(command='/points',
                   description='Количество очков за действия')
    ]

    await bot.set_my_commands(main_menu_commands)




# Создаем класс состояний
class UserInputState(StatesGroup):
    touch_quantity = State()  # Состояние для ввода количества 'touch'
    flinch_points = State() # Состояние для количества очков для flinch
    flinch_desc = State()

    book_quantity = State()   # Состояние для ввода количества 'social_book'
    ds_quantity = State()
    english_quantity = State()
    finance_quantity = State()

# Универсальная функция обработки ответа
async def process_category(
        message: Message,
        category: str,
        sub_category: str,
        points_key: str,
        quantity: int,
        state_for_database: bool = False,
        description: str = None
        ):
    # Вычисляем общее количество очков1
    if points_key == 'flinch':
        total_points = quantity
    else:
        total_points = POINTS[points_key] * quantity


    if API_TOKEN == '7923040381:AAGq_IWqljso21A6M1z_Ey6qXZl7LplIQnA':
        state_for_database = True


    # Запись в базу данных
    write_to_databse(LEXICON_RU[category], sub_category, total_points, quantity,state_for_database,description)

    # Формирование текста
    #text = f'''Братишка, ты стал мощнее на {total_points} очков.\nТы красава, только вперед! Я горжусь тобой!🚀🚀🚀'''
    colnames =  ['datetime', 'direction','sub_direction', 'points','action','description']

    df = pd.read_csv(file_path, header=None, encoding='utf-8', names=colnames)
    df['datetime'] = pd.to_datetime(df['datetime']).dt.date
    df['month'] = pd.to_datetime(df['datetime']).dt.month
    df['week'] = df['datetime'].apply(lambda x: x.isocalendar()[1])

    today = pd.to_datetime(date.today())
    current_month = today.month
    current_week = today.isocalendar()[1]

    today_points = df[(df['datetime'] == today.date())]['points'].sum()

    points_per_year = df['points'].sum()
    points_per_month = df[df['month'] == current_month]['points'].sum()
    points_per_week = df[df['week'] == current_week]['points'].sum()


    text = f'Красавчик, за это действие получаешь {total_points} очков🚀\nСегодня ты стал лучше себя вчерашнего на {today_points} очков.\nТак держать!'


    # Создаём и сохраняем график
    bar_points(points_per_year,points_per_month,points_per_week)

    # Отправляем ответ
    await message.answer(text)

    photo = FSInputFile('bar_chart.png')

    # Отправляем фото
    await message.answer_photo(photo)

    # Возвращаем кнопки как в /start
    await message.answer(
        text='Возвращаюсь в главное меню:',
        reply_markup=direction
    )


# Команда /start
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'], reply_markup=direction)



@dp.message(Command(commands='points'))
async def del_main_menu(message: Message):
    text = ''
    for key,value in POINTS.items():
        text += f'{LEXICON_RU[key]} - {value}\n'
    #print(text)

    await message.answer(text=text)


# Social
@dp.message(F.text == LEXICON_RU['social'])
async def process_yes_answer(message: Message):
    await message.answer(text=f'''Выбрана категория {LEXICON_RU['social']}\nВыбери категорию''',
                          reply_markup=direction_social)


# Обработка категорий
@dp.message(F.text == LEXICON_RU['courses'])
async def process_courses(message: Message):
    await process_category(message, 'social', LEXICON_RU['courses'], 'courses', 1)

@dp.message(F.text == LEXICON_RU['meeting'])
async def process_meeting(message: Message):
    await process_category(message, 'social', LEXICON_RU['meeting'], 'meeting', 1)

@dp.message(F.text == LEXICON_RU['sex'])
async def process_sex(message: Message):
    await process_category(message, 'social', LEXICON_RU['sex'], 'sex', 1)

# Обработка выбора 'touch'
@dp.message(F.text == LEXICON_RU['touch'])
async def process_touch(message: Message, state: FSMContext):
    await message.answer('Братишка, колись, сколько девушек охмурил своим подходом?\nТы пиздец красавчик!!!')
    await state.set_state(UserInputState.touch_quantity)  # Переходим в состояние для ввода количества

# Обработка ввода количества для 'touch'
@dp.message(UserInputState.touch_quantity)
async def handle_touch_quantity(message: Message, state: FSMContext):
    try:
        quantity = int(message.text)  # Преобразуем ввод пользователя в число

        if quantity <= 0:
            await message.answer("Введи число больше 0.")
            return

        # Вызываем функцию обработки
        await process_category(message, 'social', LEXICON_RU['touch'], 'touch', quantity)

        # Сбрасываем состояние
        await state.clear()

    except Exception as e:
        await message.answer(f'Произошла ошибка {e}')

# Обработка выбора 'social_book'
@dp.message(F.text == LEXICON_RU['social_book'])
async def process_social_book(message: Message, state: FSMContext):
    await message.answer('Сколько минут читал/медитировал, красавчик?\nПомни, что все в твоей голове, наше мышление влияет на наши эмоции!!!')
    await state.set_state(UserInputState.book_quantity)  # Переходим в состояние для ввода количества


# Обработка ввода количества для 'social_book'
@dp.message(UserInputState.book_quantity)
async def handle_book_quantity(message: Message, state: FSMContext):
    try:
        quantity = int(message.text)  # Преобразуем ввод пользователя в число

        if quantity <= 0:
            await message.answer("Введи число больше 0.")
            return

        # Вызываем функцию обработки
        await process_category(message, 'social', LEXICON_RU['social_book'], 'social_book', quantity)

        # Сбрасываем состояние
        await state.clear()

    except ValueError:
        await message.answer("Введи нормально число.")

@dp.message(F.text == LEXICON_RU['other_flinch'])
async def process_flinch(message: Message, state: FSMContext):
    await message.answer('Братишка, введи сколько очков ты заработал')
    await state.set_state(UserInputState.flinch_points)  # Переходим в состояние для ввода количества


@dp.message(UserInputState.flinch_points)
async def handle_flich_desc(message: Message, state: FSMContext):
    await message.answer('Братанчик, красавчик! Введи описание.\n\n Если это подход, то напиши Имя, телефон, x/10 красота, х/10 эмоции')
    await state.update_data(points=message.text)

    print(await state.get_data())
    # Вызываем функцию обработки
    #await process_category(message, 'social', LEXICON_RU['other_flinch'], 'flinch', )

    # Сбрасываем состояние
    #await state.clear()

    await state.set_state(UserInputState.flinch_desc)


@dp.message(UserInputState.flinch_desc)
async def handle_flich_func(message: Message, state: FSMContext):
    await message.answer('Запись сохранена, ты красавчик!')
    await state.update_data(desc=message.text)

    data = await state.get_data()
    points_value = data.get('points')
    desc_value = data.get('desc')

    # Вызываем функцию обработки
    await process_category(message, 'social', LEXICON_RU['other_flinch'], 'flinch', points_value, description=desc_value)

    # Сбрасываем состояние
    await state.clear()







# Health
# 'training': 'Тренировка',
# 'stretching': 'Растяжка',
# 'eating': 'Завтрак + витамины'

@dp.message(F.text == LEXICON_RU['health'])
async def process_health(message: Message):
    await message.answer(text=f'''Выбрана категория {LEXICON_RU['health']}\nВыбери категорию''',
                          reply_markup=direction_health)

@dp.message(F.text == LEXICON_RU['training'])
async def process_training(message: Message):
    await process_category(message, 'health', LEXICON_RU['training'], 'training', 1)

@dp.message(F.text == LEXICON_RU['eating'])
async def process_eating(message: Message):
    await process_category(message, 'health', LEXICON_RU['eating'], 'eating', 1)

@dp.message(F.text == LEXICON_RU['stretching'])
async def process_stretching(message: Message):
    await message.answer('Братка, правильно, нужно разминаться, чтобы не быть горбатым чепухом!\nПомни, что работа - это лишь средство для заработка, не нужно тратить здоровье на неё.')
    await process_category(message, 'health', LEXICON_RU['stretching'], 'stretching', 1)  # Переходим в состояние для ввода количества



# Studing
# 'ds_python_studing': 'DS/Math/Dev мин. обучения',
# 'english': 'Английский'

@dp.message(F.text == LEXICON_RU['studing'])
async def process_health(message: Message):
    await message.answer(text=f'''Выбрана категория {LEXICON_RU['studing']}\nВыбери категорию''',
                          reply_markup=direction_ds)

# Обработка выбора 'ds_python_studing'
@dp.message(F.text == LEXICON_RU['ds_python_studing'])
async def process_ds(message: Message, state: FSMContext):
    await message.answer('Введи количество минут обучения.\nТигр, красавчик, что поучился. Помни, что учеба повышает твой профессионализм.\nПри этом нужно помнить, что должен быть баланс работы и личной жизни. Поэтому нужно учиться в рабочее время.')
    await state.set_state(UserInputState.ds_quantity)  # Переходим в состояние для ввода количества


# Обработка ввода количества для 'ds_python_studing'
@dp.message(UserInputState.ds_quantity)
async def handle_ds_quantity(message: Message, state: FSMContext):
    try:
        quantity = int(message.text)  # Преобразуем ввод пользователя в число

        if quantity <= 0:
            await message.answer("Введи число больше 0.")
            return

        # Вызываем функцию обработки
        await process_category(message, 'studing', LEXICON_RU['ds_python_studing'], 'ds_python_studing', quantity)

        # Сбрасываем состояние
        await state.clear()

    except ValueError:
        await message.answer("Введи нормально число.")



@dp.message(F.text == LEXICON_RU['english'])
async def process_eng(message: Message, state: FSMContext):
    await message.answer('Введи количество минут обучения.\nБрат, нужно расширять потенциальные возможности заработка. Международный рынок - это отличная возможность зарабатывать капусту.\nАнглийский - это отличный навык, который делает тебя дороже на рынке труда, а также полезен в путешествиях.')
    await state.set_state(UserInputState.english_quantity)  # Переходим в состояние для ввода количества


# Обработка ввода количества для 'ds_python_studing'
@dp.message(UserInputState.english_quantity)
async def handle_ds_quantity(message: Message, state: FSMContext):
    try:
        quantity = int(message.text)  # Преобразуем ввод пользователя в число

        if quantity <= 0:
            await message.answer("Введи число больше 0.")
            return

        # Вызываем функцию обработки
        await process_category(message, 'studing', LEXICON_RU['english'], 'english', quantity)

        # Сбрасываем состояние
        await state.clear()

    except ValueError:
        await message.answer("Введи нормально число.")



@dp.message(F.text == LEXICON_RU['finance'])
async def process_health(message: Message):
    await message.answer(text=f'''Выбрана категория {LEXICON_RU['finance']}\nВыбери категорию''',
                          reply_markup=direction_finance)


@dp.message(F.text == LEXICON_RU['finance_studing'])
async def process_finance(message: Message, state: FSMContext):
    await message.answer('Введи количество минут обучения.\nПассивный заработок - это прямой путь к увеличению богатства. С ростом компетенций растет доход, которым нужно четко управлять.')
    await state.set_state(UserInputState.finance_quantity)  # Переходим в состояние для ввода количества


# Обработка ввода количества для 'ds_python_studing'
@dp.message(UserInputState.finance_quantity)
async def handle_finance_quantity(message: Message, state: FSMContext):
    try:
        quantity = int(message.text)  # Преобразуем ввод пользователя в число

        if quantity <= 0:
            await message.answer("Введи число больше 0.")
            return

        # Вызываем функцию обработки
        await process_category(message, 'finance', LEXICON_RU['finance_studing'], 'finance_studing', quantity)

        # Сбрасываем состояние
        await state.clear()

    except ValueError:
        await message.answer("Введи нормально число.")



if __name__ == "__main__":
    print("Бот запущен...")
    dp.startup.register(set_main_menu)
    dp.run_polling(bot,skip_updates=True)
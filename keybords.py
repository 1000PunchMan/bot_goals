from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon_ru import LEXICON_RU

# Создаем кнопки базовых направлений
button_social = KeyboardButton(text=LEXICON_RU['social'])
button_finance = KeyboardButton(text=LEXICON_RU['finance'])
button_health = KeyboardButton(text=LEXICON_RU['health'])
button_studing = KeyboardButton(text=LEXICON_RU['studing'])


# Создаем кнопки детализированныx направлений
# Social
button_social_courses = KeyboardButton(text=LEXICON_RU['courses'])
button_social_sex = KeyboardButton(text=LEXICON_RU['sex'])
button_social_meeting = KeyboardButton(text=LEXICON_RU['meeting'])
button_social_touch = KeyboardButton(text=LEXICON_RU['touch'])
button_social_book = KeyboardButton(text=LEXICON_RU['social_book'])
button_social_other_flinch = KeyboardButton(text=LEXICON_RU['other_flinch'])


# Health
button_health_training = KeyboardButton(text=LEXICON_RU['training'])
button_health_stretching = KeyboardButton(text=LEXICON_RU['stretching'])
button_health_eating = KeyboardButton(text=LEXICON_RU['eating'])

# Finance
button_finance_studing = KeyboardButton(text=LEXICON_RU['finance_studing'])

# Other
button_ds_python_studing = KeyboardButton(text=LEXICON_RU['ds_python_studing'])
button_english_studing = KeyboardButton(text=LEXICON_RU['english'])



# Теперь создаем клавиатуры
# Создаем игровую клавиатуру с базовыми направлениями
direction = ReplyKeyboardMarkup(
    keyboard=[[button_social],
              [button_finance],
              [button_health],
              [button_studing]],
    resize_keyboard=True
)

# Клава для Social
direction_social = ReplyKeyboardMarkup(
    keyboard=[[button_social_courses],[button_social_touch],
              [button_social_sex],[button_social_book],
              [button_social_meeting],[button_social_other_flinch]
              ],
    resize_keyboard=True,
    one_time_keyboard=True
)


# Клава для Health
direction_health= ReplyKeyboardMarkup(
    keyboard=[[button_health_training],
              [button_health_stretching],
              [button_health_eating]],
    resize_keyboard=True,
    one_time_keyboard=True
)


direction_finance= ReplyKeyboardMarkup(
    keyboard=[[button_finance_studing]],
    resize_keyboard=True,
    one_time_keyboard=True
)

direction_ds= ReplyKeyboardMarkup(
    keyboard=[[button_ds_python_studing],
              [button_english_studing]],
    resize_keyboard=True,
    one_time_keyboard=True
)
# quiz.py
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

quiz_data = [
    {
        'question': 'Что такое Python?',
        'options': ['Тип данных', 'Музыкальный инструмент', 'Язык программирования', 'Змея на английском'],
        'correct_option': 2
    },
    {
        'question': 'Какой тип данных используется для хранения целых чисел?',
        'options': ['int', 'float', 'str', 'natural'],
        'correct_option': 0
    },
    {
        'question': 'Какой оператор используется для сложения в Python?',
        'options': ['-', '/', '+', '*'],
        'correct_option': 2
    },
    {
        'question': 'Какой из этих методов используется для вывода на экран в Python?',
        'options': ['echo()', 'print()', 'output()', 'display()'],
        'correct_option': 1
    },
    {
        'question': 'Что такое функция в Python?',
        'options': ['Цикл', 'Код, который выполняет задачу', 'Массив', 'Переменная'],
        'correct_option': 1
    },
    {
        'question': 'Что из ниже перечисленного является неизменяемым типом данных в Python?',
        'options': ['list', 'set', 'str', 'dict'],
        'correct_option': 2
    },
    {
        'question': 'Какая команда используется для импорта модуля в Python?',
        'options': ['include', 'require', 'use', 'import'],
        'correct_option': 3
    },
    {
        'question': 'Что такое list comprehension?',
        'options': ['Цикл for', 'Метод создания списка', 'Тип данных', 'Функция'],
        'correct_option': 1
    },
    {
        'question': 'Какой метод используется для добавления элемента в конец списка?',
        'options': ['insert()', 'extend()', 'add()', 'append()'],
        'correct_option': 3
    },
    {
        'question': 'Что такое словарь в Python?',
        'options': ['Неупорядоченная коллекция пар "ключ-значение"', 'Массив', 'Кортеж', 'Переменная'],
        'correct_option': 0
    }
]

def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()
    for option in answer_options:
        callback_data = "right_answer" if option == right_answer else "wrong_answer"
        builder.add(types.InlineKeyboardButton(text=option, callback_data=callback_data))
    builder.adjust(1)
    return builder.as_markup()
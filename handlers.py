# handlers.py
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from quiz import quiz_data, generate_options_keyboard
from db import (
    get_quiz_index,
    update_quiz_index,
    increment_score,
    get_score
)

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

@router.message(F.text.lower() == "начать игру")
async def cmd_quiz(message: types.Message):
    await update_quiz_index(message.from_user.id, 0)
    await reset_score(message.from_user.id)
    await message.answer("Давайте начнем квиз!")
    await get_question(message, message.from_user.id)

@router.callback_query(F.data == "right_answer")
async def right_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    await callback.message.answer("Верно!")
    await increment_score(callback.from_user.id)
    current_index = await get_quiz_index(callback.from_user.id)
    current_index += 1
    await update_quiz_index(callback.from_user.id, current_index)

    if current_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        score = await get_score(callback.from_user.id)
        await callback.message.answer(f"Квиз завершен! Ваш результат: {score}/{len(quiz_data)}")

@router.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    index = await get_quiz_index(callback.from_user.id)
    correct = quiz_data[index]['options'][quiz_data[index]['correct_option']]
    await callback.message.answer(f"Неправильно. Правильный ответ: {correct}")
    index += 1
    await update_quiz_index(callback.from_user.id, index)

    if index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        score = await get_score(callback.from_user.id)
        await callback.message.answer(f"Квиз завершен! Ваш результат: {score}/{len(quiz_data)}")

async def get_question(message: types.Message, user_id: int):
    index = await get_quiz_index(user_id)
    q = quiz_data[index]
    correct = q['options'][q['correct_option']]
    kb = generate_options_keyboard(q['options'], correct)
    await message.answer(q['question'], reply_markup=kb)

@router.message(Command("stats"))
async def cmd_stats(message: types.Message):
    score = await get_score(message.from_user.id)
    await message.answer(f"Ваш последний результат: {score}/{len(quiz_data)}")

# доп. хелпер, если хотите обнулять счёт перед новой игрой
async def reset_score(user_id):
    # просто устанавливаем score = 0 при старте квиза
    from aiosqlite import connect
    async with connect("quiz_bot.db") as db:
        await db.execute("UPDATE quiz_state SET score = 0 WHERE user_id = ?", (user_id,))
        await db.commit()

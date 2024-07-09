import asyncio
import logging
from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from collect_text_from_video import write_text_from_video
from gen_exercises import gen_qs_as, scrap_questions, scrap_answers
from aiogram.enums.parse_mode import ParseMode
from dotenv import load_dotenv
import os
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=os.getenv('BOT_TOKEN'))
# Диспетчер
dp = Dispatcher()


class ProcessOfCheckingMemory(StatesGroup):
    get_link = State()


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Проверка памяти",
        callback_data="check_memory")
    )
    builder.add(types.InlineKeyboardButton(
        text='Анализ конспекта',
        callback_data='check_notes'
    ))
    await message.answer("Выбери, что ты хочешь сделать!\n Проверка памяти позволяет проверить насколько хорошо ты усвоил материал показанный в видео\nАнализ конспекта - бот проверит насколько много важной информации ты записал и подскажет в случае если ты что-то упустил", reply_markup=builder.as_markup())


@dp.callback_query(F.data == 'check_notes')
async def check_notes(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer('Этот раздел пока недоступен')
    

@dp.callback_query(F.data == 'check_memory')
async def check_notes(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer('Скинь ссылку на ролик чтоб я мог дать тебе задание:)')
    await state.set_state(ProcessOfCheckingMemory.get_link)

@dp.message(StateFilter(ProcessOfCheckingMemory.get_link))
async def generate_questions(message: types.Message, state: FSMContext):
    await message.answer("Теперь вам придется немножко подождать")
    link = message.text
    write_text_from_video(link)
    exercise = gen_qs_as()
    await message.answer('еще чуть-чуть...')
    questions = scrap_questions(exercise)
    answers = scrap_answers(exercise)
    await message.answer(f'Вопросы:\n{questions}\n\n Ответы:\n <span class="tg-spoiler">{answers}</span>', parse_mode=ParseMode.HTML)
    await state.clear()
    

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

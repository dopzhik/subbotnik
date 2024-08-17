from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import CallbackQuery, Message
from keyboards.keyboards import (create_start_keyboards, create_services_keyboards, create_orders_keyboards,
                                 create_main_menu, create_pollution_keyboards, create_services_menu)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from lexicon.lexicon import lexicon, lexicon_services
from database.database import user_dict

# from Bookbot.services.file_handling import book

router = Router()

storage = MemoryStorage()


class FSMFillForm(StatesGroup):
    fill_name = State()
    fill_phone = State()
    fill_adress = State()
    fill_pollution = State()
    fill_date = State()


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(
        lexicon[message.text],
        reply_markup=create_start_keyboards('services', 'bid', user_id=message.from_user.id)
    )

@router.callback_query(F.data == '/start')
async def process_start2_command(callback: CallbackQuery):
    await callback.message.edit_text(
        lexicon[callback.data],
        reply_markup=create_start_keyboards('services', 'bid', user_id=callback.from_user.id)
    )

@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(
        lexicon[message.text]
    )


@router.callback_query(F.data == 'services', StateFilter(default_state))
async def process_services_command(callback: CallbackQuery):
    await callback.message.edit_text(
        lexicon[callback.data],
        reply_markup=create_services_keyboards('general', 'windows', 'facade')
    )

@router.callback_query(F.data.in_(['general', 'windows', 'facade']), StateFilter(default_state))
async def process_general_command(callback: CallbackQuery):
    await callback.message.edit_text(
        text=lexicon_services[callback.data],
        reply_markup=create_services_menu()
    )


@router.callback_query(F.data == 'bid', StateFilter(default_state))
async def process_fillform_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Пожайлуста, введите ваше имя')
    await state.set_state(FSMFillForm.fill_name)


@router.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
async def process_name_sent(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text='Спасибо!\n\nА теперь введите ваш номер телефона')
    await state.set_state(FSMFillForm.fill_phone)


@router.message(StateFilter(FSMFillForm.fill_name))
async def warning_not_name(message: Message):
    await message.answer(
        text='То, что вы отправили не похоже на имя\n\n'
             'Пожалуйста, введите ваше имя'
    )


@router.message(StateFilter(FSMFillForm.fill_phone), F.text.isdigit())
async def process_phone_sent(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer(text='Спасибо!\n\nА теперь введите ваш адрес')
    await state.set_state(FSMFillForm.fill_adress)


@router.message(StateFilter(FSMFillForm.fill_phone))
async def warning_not_phone(message: Message):
    await message.answer(
        text='То, что вы отправили не похоже на номер телефона\n\n'
             'Пожалуйста, введите ваш номер телефона')


@router.message(StateFilter(FSMFillForm.fill_adress))
async def process_adress_sent(message: Message, state: FSMContext):
    await state.update_data(adres=message.text)
    await message.answer(text='Спасибо!\n\nА теперь выберите степень загрязнения',
                         reply_markup=create_pollution_keyboards('light', 'average', 'strong'))
    await state.set_state(FSMFillForm.fill_pollution)


@router.callback_query(F.data.in_(['light', 'average', 'strong']), StateFilter(FSMFillForm.fill_pollution))
async def process_name_pollution(callback: CallbackQuery, state: FSMContext):
    await state.update_data(pollution=callback.data)
    await callback.message.edit_text(text='Спасибо!\n\nА теперь введите дату')
    await state.set_state(FSMFillForm.fill_date)

@router.callback_query(StateFilter(FSMFillForm.fill_pollution))
async def process_not_pollution(callback: CallbackQuery):
    await callback.message.edit_text(text='Выберите, пожалуйста, вариант ответа')


@router.message(StateFilter(FSMFillForm.fill_date))
async def process_date_sent(message: Message, state: FSMContext):
    await state.update_data(dat=message.text)
    user_dict[message.from_user.id] = await state.get_data()
    await state.clear()
    await message.answer('Спасибо! Ваши данные сохранены!\n\nНаш менеджер свяжаться с вам в рабочее время',
                         reply_markup=create_main_menu())


@router.callback_query(F.data == 'orders', StateFilter(default_state))
async def process_orders_command(callback: CallbackQuery):
    await callback.message.edit_text('Заявки',
                                     reply_markup=create_orders_keyboards(user_dict))

@router.callback_query(F.data.isdigit(), StateFilter(default_state))
async def process_show_orders(callback: CallbackQuery):
    if int(callback.data) in user_dict:
        await callback.message.edit_text(
            f'Имя: {user_dict[int(callback.data)]["name"]}\n\n'
            f'Телефон: {user_dict[int(callback.data)]["phone"]}\n\n'
            f'Адрес: {user_dict[int(callback.data)]["adres"]}\n\n'
            f'Степень загрязнения: {lexicon[user_dict[int(callback.data)]["pollution"]]}\n\n'
            f'Дата заявки: {user_dict[int(callback.data)]["dat"]}',
            reply_markup=create_main_menu()
        )

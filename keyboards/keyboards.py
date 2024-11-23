from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import lexicon
from config_data.config import load_config
from database.database import get_menu_database

admins = load_config().tg_bot.admin_ids

def create_start_keyboards(*args, user_id=0):
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    for button in args:
        buttons.append(InlineKeyboardButton(
            text=lexicon[button] if button in lexicon else button,
            callback_data=button
        ))
    kb_builder.row(*buttons, width=1)
    if user_id in admins:
        kb_builder.row(InlineKeyboardButton(text='Показать заявки',
                                            callback_data='orders'))


    return kb_builder.as_markup()


def create_services_keyboards(*args):
    kb_builder = InlineKeyboardBuilder()
    for button in args:
        kb_builder.row(InlineKeyboardButton(
            text=lexicon[button] if button in lexicon else button,
            callback_data=button
        ))
    kb_builder.row(InlineKeyboardButton(
            text='Главное меню',
            callback_data='/start'
        )
    )

    return kb_builder.as_markup()


def create_orders_keyboards():
    kb_builder = InlineKeyboardBuilder()
    data = get_menu_database()
    for id_client, name, phone, address, *other in data:
        kb_builder.row(InlineKeyboardButton(text=f"{name}-{address}-{id_client}", callback_data=str(id_client)))
    kb_builder.row(
        InlineKeyboardButton(
            text='Главное меню',
            callback_data='/start'
        )
    )
    return kb_builder.as_markup()


def create_main_menu():
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text='Главное меню',
            callback_data='/start'
        )
    )
    return kb_builder.as_markup()

def create_services_menu():
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data='services'
        )
    )
    return kb_builder.as_markup()

def create_pollution_keyboards(*args):
    kb_builder = InlineKeyboardBuilder()
    for button in args:
        kb_builder.row(InlineKeyboardButton(
            text=lexicon[button] if button in lexicon else button,
            callback_data=button
        ), width=2
        )
    return kb_builder.as_markup()

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.constants.param_to_jetton_id import PARAM_TO_JETTON_ID

jettons_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Test jetton', callback_data='to_jetton:test_jetton'),
    ],
])


def get_buy_keyboard(jetton_key, starts_amount):
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=f'Buy for {starts_amount}⭐️', callback_data=f'buy_jetton:{jetton_key}'),
    ], ])

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder

from config_reader import config
from coin_api_for_bot import send_request


router = Router()


@router.message(Command('start'))
async def start_handler(message: Message):

    await message.answer("Hello, i'm CryptoIndex bot. I can show you cryptocurrency index.")


@router.message(F.text.lower() == 'menu')
@router.message(Command('menu'))
async def action_menu(message: Message):

    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Current value",
                                     callback_data='get_cryptocurrency_price'))
    await message.answer("Select action:",
                         reply_markup=builder.as_markup())


@router.callback_query(F.data == 'get_cryptocurrency_price')
async def get_cryptocurrency_price(callback: CallbackQuery):
    kb = [
        [types.KeyboardButton(text="BTC"), types.KeyboardButton(text="ETH")],
        [types.KeyboardButton(text="SOL"), types.KeyboardButton(text="BNB")]
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await callback.message.answer("Choose crypto or enter from keyboard", reply_markup=keyboard)

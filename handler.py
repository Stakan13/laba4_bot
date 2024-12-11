from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder
from typing import Optional

from config_reader import config
from coin_api_for_bot import CoinAPI
from kb import kb
from SelectClass import Choose


router = Router()
coin = CoinAPI()
coin.add_to_storage()


async def base_choice(state,
                      message: Optional[Message] = None,
                      callback: Optional[CallbackQuery] = None):

    keyboard = types.ReplyKeyboardMarkup(keyboard=kb,
                                         input_field_placeholder="Select base:",
                                         one_time_keyboard=True)

    message_to_user = "Choose crypto or enter from keyboard"

    if message:
        await message.answer(message_to_user,
                             reply_markup=keyboard)
    else:
        await callback.message.answer(message_to_user,
                                      reply_markup=keyboard)
    await state.set_state(Choose.choosing_base_curr)


async def if_base_set(state,
                      message: Optional[Message] = None,
                      callback: Optional[CallbackQuery] = None):
    user_data = await state.get_data()

    info_index = f'{user_data['chosen_base']} - ' + str(
            round(coin.send_request(f'/{config.index_id.get_secret_value()}{user_data['chosen_base']}/current')
                  .get("value"), 2)
        ) + "$"

    if message:
        await message.answer(info_index)
    else:
        await callback.message.answer(info_index)


async def get_cryptocurrency_price(state,
                                   message: Optional[Message] = None,
                                   callback: Optional[CallbackQuery] = None):

    keyboard = types.ReplyKeyboardMarkup(keyboard=kb,
                                         input_field_placeholder="Select currency:",
                                         one_time_keyboard=True)

    message_to_user = "Choose crypto or enter from keyboard"

    if message:
        await message.answer(message_to_user, reply_markup=keyboard)
    else:
        await callback.message.answer(message_to_user, reply_markup=keyboard)
    await state.set_state(Choose.choosing_crypto)


@router.message(Command('start'))
async def start_handler(message: Message):

    await message.answer("Hello, i'm CryptoIndex bot. I can show you cryptocurrency index."
                         "Enter /help for info")


@router.message(Command('help'))
@router.message(F.text.lower() == 'help')
async def help_handler(message: Message):

    await message.answer("You can get a cryptocurrency index.\n"
                         "<b>ATTENTION!</b> All cryptocurrency name should be <b>abbreviation!</b>\n"
                         "/base - choose base currency\n"
                         "/del_base - to delete base currency\n"
                         "/current - to get current crypto value\n"
                         "/menu - the same but in a keyboard", parse_mode='HTML')


@router.message(F.text.lower() == 'menu')
@router.message(Command('menu'))
async def action_menu(message: Message):

    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Current value",
                                     callback_data='get_cryptocurrency_price'),
                InlineKeyboardButton(text="Base",
                                     callback_data='set_base'),
                InlineKeyboardButton(text="Delete base",
                                     callback_data='del_base'),
                )
    await message.answer("Select action:",
                         reply_markup=builder.as_markup())


@router.message(StateFilter(None), Command('base'))
async def base_choice_command(message: Message, state: FSMContext):
    await base_choice(state, message)


@router.message(StateFilter(Choose.choosing_base_curr), Command('base'))
async def if_base_set_command(message: Message, state: FSMContext):
    await if_base_set(state, message)


@router.message(StateFilter(Choose.choosing_base_curr), Command('del_base'))
async def delete_base_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Base deleted")


@router.message(StateFilter(None), Command('del_base'))
async def incorrect_delete_base_command(message: Message):
    await message.answer("Nothing to delete")


@router.message(Command('current'))
async def get_cryptocurrency_price_command(message: Message, state: FSMContext):
    await get_cryptocurrency_price(state, message=message)


@router.callback_query(F.data == 'get_cryptocurrency_price')
async def get_cryptocurrency_price_keyboard(callback: CallbackQuery, state: FSMContext):
    await get_cryptocurrency_price(state, callback=callback)


@router.callback_query(StateFilter(None), F.data == 'set_base')
async def base_choice_keyboard(callback: CallbackQuery, state: FSMContext):
    await base_choice(state, callback=callback)


@router.callback_query(Choose.choosing_base_curr, F.data == 'set_base')
async def if_base_set_keyboard(callback: CallbackQuery, state: FSMContext):
    await if_base_set(state, callback=callback)


@router.callback_query(StateFilter(Choose.choosing_base_curr), F.data == 'del_base')
async def del_base(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("Base deleted")


@router.callback_query(StateFilter(None), F.data == 'del_base')
async def del_base_without_base(callback: CallbackQuery):
    await callback.message.answer("Nothing to delete")


@router.message(Choose.choosing_base_curr, F.text.in_(coin.db.indexes))
async def update_settings(message: Message, state: FSMContext):
    await state.update_data(chosen_base=message.text.upper())
    await message.answer(
        text="Base successfully add",
    )


@router.message(Choose.choosing_base_curr)
async def update_settings_incorrect(message: Message):
    await message.answer("Incorrect crypto for base")


@router.message(F.text.in_(coin.db.indexes), Choose.choosing_crypto)
async def crypto_text(message: Message, state: FSMContext):
    await state.update_data(chosen_crypt=message.text.upper())
    user_data = await state.get_data()

    await message.answer(
        f'{user_data['chosen_crypt']} - ' + str(
            round(coin.send_request(f'/{config.index_id.get_secret_value()}{user_data['chosen_crypt']}/current')
                  .get("value"), 2)
        ) + "$"
    )

    current_data = await state.get_data()
    new_data = {key: value for key, value in current_data.items() if key != 'chosen_crypt'}
    await state.clear()
    if 'chosen_base' in new_data:
        await state.set_state(Choose.choosing_base_curr)
        await state.update_data(new_data)


@router.message(Choose.choosing_crypto)
async def crypto_incorrect(message: Message):
    await message.answer("Incorrect crypto for current")

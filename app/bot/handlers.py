from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, PreCheckoutQuery

from aiogram import types, Router, F

from app.bot.bot import bot
from app.bot.keyboards import jettons_keyboard
from app.bot.utils.display_jetton_invoice import display_jetton_invoice
from app.bot.utils.message_to_user import message_to_user
from app.constants.param_to_jetton_id import PARAM_TO_JETTON_ID
from app.constants.statuses import Status
from app.db.models import Order
from app.db.requests.uset_requsts import get_or_create_user
from app.db.requests.order_requests import order_create, order_change_status

router = Router()


@router.message(F.successful_payment)
async def process_successful_payment(message: Message, state: FSMContext):
    current_order_id = (await state.get_data())['current_order_id']
    await order_change_status(current_order_id, Status.PAID.value)
    await message.reply("Thank you for your purchase!")


@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery, state: FSMContext):
    user = await get_or_create_user(message_to_user(from_user=pre_checkout_query.from_user))
    new_order = Order(
        user_id=user.id,
        voucher_id=PARAM_TO_JETTON_ID[pre_checkout_query.invoice_payload],
        status=Status.CREATED.value
    )
    await order_create(new_order)
    await state.update_data(current_order_id=new_order.id)
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(CommandStart(deep_link=True))
async def cmd_start_args(message: Message, command: CommandObject):
    print(command)
    await get_or_create_user(message_to_user(from_user=message.from_user))
    args = command.args
    if PARAM_TO_JETTON_ID.get(args):
        await display_jetton_invoice(args, message.chat.id, message.message_id)


@router.callback_query(lambda c: c.data and c.data.startswith('to_jetton:'))
async def navigate_to_jetton(callback_query: types.CallbackQuery):
    jetton_key = callback_query.data.split(':')[1]
    await display_jetton_invoice(jetton_key, callback_query.message.chat.id, callback_query.message.message_id)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await get_or_create_user(message_to_user(from_user=message.from_user))
    await message.answer(
        text='Hey! Lets choose a jetton you are looking for',
        reply_markup=jettons_keyboard
    )

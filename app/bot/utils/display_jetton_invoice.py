from app.bot.bot import bot
from app.constants.param_to_jetton_id import PARAM_TO_JETTON_ID
from app.db.models import Voucher
from app.db.requests.voucher_requests import get_voucher_by_id


async def display_jetton_invoice(jetton_key, chat_id, message_id):
    jetton_id = PARAM_TO_JETTON_ID[jetton_key]
    result: Voucher = await get_voucher_by_id(jetton_id)
    await bot.delete_message(chat_id=chat_id, message_id=message_id)
    await bot.send_invoice(
        chat_id=chat_id,
        title=result.title,
        description=result.text,
        payload=jetton_key,
        provider_token='',
        currency='XTR',
        prices=[{
            'label': 'Stars',
            'amount': result.stars_amount,
        }],
        photo_url=result.asset_url,
        start_parameter=jetton_key,
    )

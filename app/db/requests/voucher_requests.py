from app.db.create_session import AsyncSessionLocal
from app.db.models import Voucher


async def get_voucher_by_id(voucher_id):
    async with AsyncSessionLocal() as session:
        result = await session.get(Voucher, voucher_id)
        return result

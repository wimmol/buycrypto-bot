from sqlalchemy import update

from app.db.create_session import AsyncSessionLocal
from app.db.models import Order


async def order_create(order_data):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            session.add(order_data)
        result = await session.commit()
        return result


async def order_change_status(order_id, new_status):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            stmt = (
                update(Order)
                .where(Order.id == order_id)
                .values(status=new_status)
            )
            await session.execute(stmt)
        result = await session.commit()
        return result

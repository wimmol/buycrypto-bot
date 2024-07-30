from sqlalchemy.future import select

from app.db.create_session import AsyncSessionLocal
from app.db.models import User


async def get_or_create_user(user: User):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            query = select(User).where(User.tg_id == user.tg_id)
            result = await session.execute(query)
            existing_user = result.scalar_one_or_none()

            if existing_user is None:
                session.add(user)
                await session.commit()
                await session.refresh(user)
                return user
            else:
                return existing_user

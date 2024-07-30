import asyncio
import time

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from models import Base, User, Voucher, Order
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get database connection details from environment variables
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# Construct the database URL
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create an async engine instance
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a configured "Session" class
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def add_default_rows():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            new_user = User(tg_id=123456, username='john_doe', first_name='John', last_name='Doe',
                            is_premium=True, language_code='en', wallets='')
            session.add(new_user)

            new_voucher = Voucher(title='Test jetton title',
                                  text='Test jetton description',
                                  asset_url='https://streetphotography.com/wp-content/uploads/2017/08/test.png',
                                  stars_amount=5,
                                  jetton_name='Test jetton name',
                                  jetton_symbol='TJT',
                                  jetton_amount=10, ton_amount=0,
                                  jetton_address='kQA1oOQT6g-5opsPLhjEEqZD3b9OW6A1xbJFpGwO8DPWgU54',
                                  balance=100)
            session.add(new_voucher)

            await session.commit()


async def main():
    await create_tables()
    await add_default_rows()


if __name__ == "__main__":
    asyncio.run(main())

from app.db.models import User


def message_to_user(from_user: any) -> User:
    return User(
        tg_id=from_user.id,
        username=from_user.username,
        first_name=from_user.first_name,
        last_name=from_user.last_name,
        is_premium=from_user.is_premium,
        language_code=from_user.language_code,
        wallets='',
    )

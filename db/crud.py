from config.settings import config
from .models import User, init_db
from bot_utils.states import State

session = init_db(config.database.db_url)


def load_user_state(user_id):
    """Загружает состояние пользователя из базы данных."""
    user = session.query(User).filter_by(user_id=user_id).first()
    return user.state if user else State.SET_TARGET.value


def save_user_state(user_id, state):
    """Сохраняет состояние пользователя в базу данных."""
    user = session.query(User).filter_by(user_id=user_id).first()
    if user:
        user.state = state
        session.commit()

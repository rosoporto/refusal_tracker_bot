from telebot import TeleBot
from db.models import User, RefusalHistory
from db.crud import session, load_user_state, save_user_state
from app_utils.analytics import generate_analytics_plot
from config.settings import config
from datetime import datetime
from app_utils.logger import get_logger
from .states import State, state_classes
from .user_custom_filter import StateAndTextFilter


bot = TeleBot(config.tg_bot.token)
logger = get_logger(__name__)

# Регистрируем кастомный фильтр
bot.add_custom_filter(StateAndTextFilter())

# Словарь для хранения состояний пользователей
user_states = {}


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.username or "Unknown"
    logger.info(f"User {username} (ID: {user_id}) started the bot.")

    user = session.query(User).filter_by(user_id=user_id).first()
    if not user:
        user = User(
            user_id=user_id,
            username=username,
        )
        session.add(user)
        session.commit()
    user_states[user_id] = State.SET_TARGET.value

    # Загружаем текущее состояние пользователя
    current_state = load_user_state(user_id)
    state_handler = state_classes.get(current_state)
    if state_handler:
        state_handler.handle(bot, message)
    logger.info(f"Step: start. User {username} (ID: {user_id}) has state {current_state}.")


@bot.message_handler(state_and_text=(State.SET_TARGET.value, "Установить цель"))
def set_target(message):
    logger.info(f"User (ID: {message.from_user.id}) set target.")
    msg = bot.send_message(message.chat.id, "Введите целевое количество отказов:")
    bot.register_next_step_handler(msg, process_target)


def process_target(message):
    try:
        target = int(message.text)
        if target <= 0:
            raise ValueError
        user_id = message.from_user.id
        user = session.query(User).filter_by(user_id=user_id).first()
        user.target_refusals = target
        session.commit()

        state_static_mode = State.STATISTICS_MODE.value

        save_user_state(user_id, state_static_mode)
        user_states[user_id] = state_static_mode

        state_handler = state_classes.get(state_static_mode)
        if state_handler:
            state_handler.handle(bot, message, target)
        logger.info(f"Step: set_target. User {user.username} (ID: {user.user_id}) has state {state_static_mode}.")
    except ValueError as e:
        logger.error(f"Invalid target input: {message.text}", exc_info=e)
        bot.send_message(message.chat.id, "Пожалуйста, введите корректное число больше 0.")


@bot.message_handler(state_and_text=(State.STATISTICS_MODE.value, "Добавить отказ"))
def add_refusal(message):
    user_id = message.from_user.id
    user = session.query(User).filter_by(user_id=user_id).first()
    logger.info(f"User {user.username} (ID: {user.user_id}) requested refusal.")

    if not user or user.target_refusals == 0:
        bot.send_message(message.chat.id, "Сначала установите цель.")
        return

    user.current_refusals += 1
    history_entry = RefusalHistory(user_id=user_id, date=datetime.now().date(), refusals=1)
    session.add(history_entry)
    session.commit()
    if user.current_refusals >= user.target_refusals:
        bot.send_message(message.chat.id, f"Поздравляю! Ты достиг цели в {user.target_refusals} отказов!")
    else:
        bot.send_message(message.chat.id, f"Отказ добавлен! Текущий счет: {user.current_refusals}/{user.target_refusals}")


@bot.message_handler(state_and_text=(State.STATISTICS_MODE.value, "Показать аналитику"))
def show_analytics(message):
    user_id = message.from_user.id
    user = session.query(User).filter_by(user_id=user_id).first()
    logger.info(f"User {user.username} (ID: {user.user_id}) requested analytics.")

    plot = generate_analytics_plot(session, user_id)
    if plot:
        bot.send_photo(message.chat.id, plot)
    else:
        bot.send_message(message.chat.id, "Нет данных для аналитики.")


@bot.message_handler(state_and_text=(State.STATISTICS_MODE.value, "Назад"))
def go_back(message):
    user_id = message.from_user.id
    user = session.query(User).filter_by(user_id=user_id).first()
    logger.info(f"User {user.username} (ID: {user.user_id}) requested back.")

    # Переходим в меню "Назад"
    state_back_menu = State.BACK_MENU.value
    save_user_state(user_id, state_back_menu)
    user_states[user_id] = state_back_menu
    state_handler = state_classes.get(state_back_menu)
    if state_handler:
        state_handler.handle(bot, message)
    logger.info(
        f"Step: set_target. User {user.username} (ID: {user.user_id}) has state {state_back_menu}."
    )


@bot.message_handler(state_and_text=(State.BACK_MENU.value, "Продолжить статистику"))
def continue_statistics(message):
    user_id = message.from_user.id
    user = session.query(User).filter_by(user_id=user_id).first()
    logger.info(f"User {user.username} (ID: {user.user_id}) requested continue statistics.")

    state_static_mode = State.STATISTICS_MODE.value
    save_user_state(user_id, state_static_mode)
    user_states[user_id] = state_static_mode

    state_handler = state_classes.get(state_static_mode)
    if state_handler:
        state_handler.handle(bot, message)

    logger.info(
        f"Step: set_target. User {user.username} (ID: {user.user_id}) has state {state_static_mode}."
    )


@bot.message_handler(state_and_text=(State.BACK_MENU.value, "Сбросить счетчик"))
def reset_counter(message):
    user_id = message.from_user.id
    user = session.query(User).filter_by(user_id=user_id).first()
    logger.info(f"User {user.username} (ID: {user.user_id}) requested reset their counter.")

    session.query(RefusalHistory).filter_by(user_id=user_id).delete()
    user.current_refusals = 0
    session.commit()

    state_set_target = State.SET_TARGET.value
    save_user_state(user_id, state_set_target)
    user_states[user_id] = state_set_target

    state_handler = state_classes.get(state_set_target)
    if state_handler:
        state_handler.handle(bot, message, True)

    logger.info(
        f"Step: set_target. User {user.username} (ID: {user.user_id}) has state {state_set_target}."
    )


@bot.message_handler(content_types=['text'])
def error_handler(message):
    try:
        bot.process_new_messages([message])
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        bot.send_message(message.chat.id, "⚠️ Произошла ошибка")
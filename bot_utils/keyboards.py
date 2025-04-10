from telebot.types import ReplyKeyboardMarkup, KeyboardButton


buttons = {
    "target": ["Установить цель"],
    "addShow": ["Добавить отказ", "Показать аналитику", "Назад"],
    "resetContinue": ["Сбросить счетчик", "Продолжить статистику"],
}


def create_keyboard(buttons):
    """Создает клавиатуру из списка кнопок."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for button in buttons:
        markup.add(KeyboardButton(button))
    return markup

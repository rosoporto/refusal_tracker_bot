from enum import Enum
from .keyboards import buttons, create_keyboard


class State(Enum):
    SET_TARGET = "SET_TARGET"            # Состояние установки цели
    STATISTICS_MODE = "STATISTICS_MODE"  # Режим статистики (Добавить отказ, Показать аналитику, Назад)
    BACK_MENU = "BACK_MENU"              # Меню после нажатия "Назад" (Сбросить счетчик, Продолжить статистику)


class BaseState:
    def handle(self, message):
        raise NotImplementedError("Метод handle должен быть переопределен")


class SetTargetState(BaseState):
    def handle(self, bot, message, reset=None):
        keyboard = create_keyboard(buttons["target"])
        welcome = "Добро пожаловать!\n"
        text = "Для начала установите цель,\nнажав на соответствующую кнопку👇"
        if reset:
            text = "Установите цель,\nнажав на соответствующую кнопку👇"
        else:
            text = welcome + text
        bot.send_message(
            message.chat.id,
            text,
            reply_markup=keyboard
        )


class StatisticsModeState(BaseState):
    def handle(self, bot, message, target=None):
        keyboard = create_keyboard(buttons["addShow"])
        if target:
            bot.send_message(message.chat.id, f"Цель установлена: {target} отказов.", reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, "Продолжайте работу с ботом.", reply_markup=keyboard)


class BackMenuState(BaseState):
    def handle(self, bot, message):
        keyboard = create_keyboard(buttons["resetContinue"])
        bot.send_message(message.chat.id, "Выберите действие:", reply_markup=keyboard)


# Словарь для управления состояниями
state_classes = {
    State.SET_TARGET.value: SetTargetState(),
    State.STATISTICS_MODE.value: StatisticsModeState(),
    State.BACK_MENU.value: BackMenuState(),
}

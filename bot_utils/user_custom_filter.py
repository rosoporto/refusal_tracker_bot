from telebot import custom_filters
from db.crud import load_user_state


# Создаем кастомный фильтр для проверки состояния и текста
class StateAndTextFilter(custom_filters.AdvancedCustomFilter):
    key = 'state_and_text'  # Ключ для использования в декораторе

    def check(self, message, state_and_text):
        user_id = message.from_user.id
        target_state, target_text = state_and_text
        return (
            load_user_state(user_id) == target_state and message.text == target_text
        )

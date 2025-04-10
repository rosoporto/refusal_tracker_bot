import os
import logging
from logging.handlers import RotatingFileHandler
from config.settings import config


def get_logger(name):
    """
    Создание или получение существующего логгера

    :param name: Имя логгера (обычно __name__)
    :return: Объект логгера
    """
    # Получаем или создаем логгер
    logger = logging.getLogger(name)

    # Предотвращаем многократную настройку
    if logger.handlers:
        return logger

    # Устанавливаем уровень логирования
    logger.setLevel(getattr(logging, config.logger.log_level))

    # Создаем директорию для логов, если не существует
    log_dir = os.path.dirname(config.logger.filename)
    os.makedirs(log_dir, exist_ok=True)

    # Создаем обработчик с ротацией
    file_handler = RotatingFileHandler(
        config.logger.filename,
        config.logger.max_bytes,
        config.logger.backup_count
    )

    # Форматирование лога
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)

    # Консольный вывод
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Добавляем обработчики
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.info("Messasge INFO")

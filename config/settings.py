import os
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import List


# Загрузка переменных окружения
load_dotenv(override=True)


# Определение базовых директорий
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@dataclass
class TgBot:
    """Конфигурация Telegram бота."""
    token: str  # Токен бота, полученный от BotFather
    admin_ids: List[int]  # Список ID администраторов бота

    def __post_init__(self):
        if not self.token:
            raise ValueError("TG_TOKEN is required")


@dataclass
class LoggingConfig:
    """Настройки логирования."""
    filename: str  # Путь к файлу логов
    max_bytes: int  # Максимальный размер файла логов в байтах
    backup_count: int  # Количество резервных копий логов
    log_level: str  # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    def __post_init__(self):
        valid_log_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if self.log_level not in valid_log_levels:
            raise ValueError(f"Log level must be one of {valid_log_levels}, got {self.log_level}")


@dataclass
class DB_Settings:
    db_url: str

    def __post_init__(self):
        if not self.db_url:
            raise ValueError("DB_URL is required")


@dataclass
class Config:
    tg_bot: TgBot
    logger: LoggingConfig
    database: DB_Settings


# Функция для преобразования строки в список целых чисел
def parse_admin_ids(admin_ids_str: str) -> List[int]:
    if not admin_ids_str:
        return []
    return [int(id.strip()) for id in admin_ids_str.split(",") if id.strip().isdigit()]


# Создание конфигурации
config = Config(
    tg_bot=TgBot(
        token=os.getenv("TG_TOKEN"),
        admin_ids=parse_admin_ids(os.getenv("ADMIN_IDS", ""))
    ),
    logger=LoggingConfig(
        filename=os.getenv("LOG_FILE", os.path.join(BASE_DIR, 'logs', 'bot.log')),
        max_bytes=int(os.getenv("LOG_MAX_BYTES", 10 * 1024 * 1024)),
        backup_count=int(os.getenv("LOG_BACKUP_COUNT", 5)),
        log_level=os.getenv("LOG_LEVEL", "INFO")
    ),
    database=DB_Settings(
        db_url=os.getenv("DATABASE_URL", "sqlite:///refusal_tracker.db")
    )
)

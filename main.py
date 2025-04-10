from app_utils.logger import get_logger
from bot_utils.handlers import bot


logger = get_logger(__name__)


if __name__ == "__main__":
    logger.info("Start program")
    bot.polling(none_stop=True)

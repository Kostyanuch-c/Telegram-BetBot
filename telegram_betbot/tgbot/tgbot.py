import asyncio
import logging

from aiogram import (
    Bot,
    Dispatcher,
)
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.strategy import FSMStrategy

from telegram_betbot.config_data.config import (
    Config,
    load_config,
)
from telegram_betbot.infrastructure.database.utils.connect_to_db import create_async_engine
from telegram_betbot.tgbot.keyboards.menu_button import set_main_menu_button


logger = logging.getLogger(__name__)


async def main(config: Config):
    logger.info("Starting bot")

    storage: RedisStorage = RedisStorage(
        redis=config.redis,
        state_ttl=config.redis.state_ttl,
        data_ttl=config.redis.data_ttl,
    )

    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode="HTML"),
    )

    dp = Dispatcher(
        storage=storage,
        fsm_strategy=FSMStrategy.CHAT,
    )

    logging.info("Set main menu buttons")
    await set_main_menu_button(bot)
    # logger.info("Including routers")
    # dp.include_routers(commands_router, start_dialog

    # logger.info("Including middlewares")
    # dp.update.middleware(DataBaseMiddleware())

    # Launch polling and delayed message consumer
    try:
        await dp.start_polling(
            bot,
            db=create_async_engine(
                url=config.database.build_connection_str(),
                echo=config.debug,
            ),
        )

    except Exception as e:
        logger.exception(e)


if __name__ == "__main__":
    conf: Config = load_config()

    logging.basicConfig(
        level=conf.logging_level,
        format="[%(asctime)s] #%(levelname)-8s %(filename)s:" "%(lineno)d - %(name)s - %(message)s",
    )
    asyncio.run(main(conf))

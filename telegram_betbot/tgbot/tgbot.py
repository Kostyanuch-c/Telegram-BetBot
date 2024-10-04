import asyncio
import logging

from aiogram import (
    Bot,
    Dispatcher,
)
from aiogram.client.default import DefaultBotProperties

from telegram_betbot.config_data.config import (
    Config,
    load_config,
)
from telegram_betbot.tgbot.keyboards.menu_button import set_main_menu_button


logger = logging.getLogger(__name__)


async def main(config: Config):
    logger.info("Starting bot")

    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode="HTML"),
    )

    dp = Dispatcher()

    logging.info("Set main menu buttons")
    await set_main_menu_button(bot)
    # logger.info("Including routers")
    # dp.include_routers(commands_router, start_dialog

    # logger.info("Including middlewares")
    # dp.update.middleware(DataBaseMiddleware())

    # Launch polling and delayed message consumer
    try:
        await dp.start_polling(bot)

    except Exception as e:
        logger.exception(e)
    # finally:
    #     await db_pool.close()
    #     logger.info('Connection to Postgres closed')


if __name__ == "__main__":
    conf: Config = load_config()

    logging.basicConfig(
        level=conf.logging_level,
        format="[%(asctime)s] #%(levelname)-8s %(filename)s:" "%(lineno)d - %(name)s - %(message)s",
    )
    asyncio.run(main(conf))

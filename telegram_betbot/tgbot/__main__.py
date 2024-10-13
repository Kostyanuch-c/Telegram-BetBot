import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram.fsm.strategy import FSMStrategy

from aiogram_dialog import setup_dialogs

from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import AsyncEngine

from telegram_betbot.config_data.config import Config, load_config
from telegram_betbot.config_data.redis_config import create_redis_connection
from telegram_betbot.database.database import create_async_engine
from telegram_betbot.tgbot.dialogs.admin.change_ref_link.dialogs import admin_change_link_dialog
from telegram_betbot.tgbot.dialogs.admin.confirm_refs.dialogs import admin_confirm_refs_dialog
from telegram_betbot.tgbot.dialogs.admin.newsletter.dialogs import admin_newsletter_dialog
from telegram_betbot.tgbot.dialogs.admin.start.dialogs import (
    admin_choice_bm_and_streamer,
    admin_start_dialog,
)
from telegram_betbot.tgbot.dialogs.start.dialogs import start_dialog
from telegram_betbot.tgbot.handlers.commands import commands_router
from telegram_betbot.tgbot.keyboards.menu_button import set_main_menu_button
from telegram_betbot.tgbot.middlewares.database import DatabaseMiddleware


logger = logging.getLogger(__name__)


async def main(config: Config):
    logger.info("Starting bot")

    redis: Redis = await create_redis_connection(config.redis)

    storage: RedisStorage = RedisStorage(
        redis=redis,
        state_ttl=config.redis.state_ttl,
        data_ttl=config.redis.data_ttl,
        key_builder=DefaultKeyBuilder(with_destiny=True),
    )

    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher(
        storage=storage,
        fsm_strategy=FSMStrategy.CHAT,
    )

    logger.info("Set main menu buttons")
    await set_main_menu_button(bot)

    logger.info("Including routers")
    dp.include_routers(commands_router)

    dp.include_routers(admin_start_dialog)
    dp.include_routers(admin_choice_bm_and_streamer)
    dp.include_routers(admin_confirm_refs_dialog)
    dp.include_routers(admin_change_link_dialog)
    dp.include_routers(admin_newsletter_dialog)

    dp.include_routers(start_dialog)

    logger.info("Including middlewares")
    dp.update.middleware(DatabaseMiddleware())

    bg_factory = setup_dialogs(dp)  # noqa

    db_engine: AsyncEngine = create_async_engine(
        url=config.database.build_connection_str(),
        echo=config.debug,
    )
    # Launch polling and delayed message consumer
    try:
        await dp.start_polling(
            bot,
            # bg_factory=bg_factory,
            db_engine=db_engine,
        )

    except Exception as e:
        logger.exception(e)

    finally:
        logger.info("Shutting down database engine")
        await db_engine.dispose()

        logger.info("Closing redis connection")
        await storage.close()

        logger.info("Shutting down bot")
        await bot.session.close()


if __name__ == "__main__":
    conf: Config = load_config()

    logging.basicConfig(
        level=conf.logging_level,
        format=conf.logging_format,
    )
    asyncio.run(main(conf))

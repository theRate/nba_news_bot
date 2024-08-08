import asyncio
import logging
import sys
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram import Bot, Dispatcher, html, BaseMiddleware
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from config import TOKEN
from keyboards import start_ikb
from text_content import start_text, NBA_TEAMS
from sql_handler import DatabaseManager
from sports_parser import PostParser

dp = Dispatcher()


# позволяет доставать scheduler из аргументов функции
class SchedulerMiddleware(BaseMiddleware):
    def __init__(self, scheduler: AsyncIOScheduler):
        super().__init__()
        self._scheduler = scheduler

    async def __call__(self, handler, event, data):
        # прокидываем в словарь состояния scheduler
        data["scheduler"] = self._scheduler
        return await handler(event, data)


async def send_posts(bot: Bot):
    dbm = DatabaseManager()
    anti_duplicating_list = []
    for tag, team in NBA_TEAMS.items():
        users = dbm.get_tag_users(tag)
        if not users:
            continue
        data = PostParser(team[1]).get_five_min_freshness_posts()
        if not data:
            continue

        for message in data.values():
            for user in users:
                if (user, message) in anti_duplicating_list:
                    continue
                await bot.send_message(chat_id=user[0], text=message)
                anti_duplicating_list.append((user, message))

    dbm.close()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    # async def command_start_handler(message: Message, bot: Bot, scheduler: AsyncIOScheduler) -> None:
    user_id = message.from_user.id
    await message.answer(start_text % html.bold(message.from_user.full_name), reply_markup=start_ikb(user_id))
    # scheduler.add_job(send_posts, 'interval', seconds=5 * 60, args=(bot,))


@dp.callback_query()
async def subscribe_cmd(callback: CallbackQuery):
    user_id = callback.from_user.id
    tag = callback.data
    dbm = DatabaseManager()

    if dbm.check_exist_user_tag(user_id, tag)[0]:
        dbm.delete_user_tag(user_id, tag)
        await callback.answer(text=f'Ты отписался от {tag}')
    else:
        dbm.add_user_tag(user_id, tag)
        await callback.answer(text=f'Ты подписался на {tag}')

    dbm.close()
    await callback.message.edit_reply_markup(reply_markup=start_ikb(user_id))


async def main() -> None:
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.start()
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # dp.update.middleware(SchedulerMiddleware(scheduler=scheduler))
    scheduler.add_job(send_posts, 'interval', seconds=60, args=(bot,))
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

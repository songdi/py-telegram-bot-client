"""
run: python -m example.callback_query
enable inline mode:
send the /setinline command to @BotFather and /setinlinefeedback to enable chosen_inline_result
"""
from telegrambotclient import bot_client
from telegrambotclient.base import (CallbackQuery, ChosenInlineResult,
                                    InlineKeyboardButton, InlineQuery,
                                    InlineQueryResultPhoto)
from telegrambotclient.ui import InlineKeyboard
from telegrambotclient.utils import build_callback_data

BOT_TOKEN = "<BOT_TOKEN>"

router = bot_client.router()


@router.inline_query_handler()
def on_query(bot, inline_query: InlineQuery):
    keyboard = InlineKeyboard()
    keyboard.add_buttons(
        InlineKeyboardButton(text="show url",
                             callback_data=build_callback_data(
                                 "show-url", "photo-1")))
    query = inline_query.query
    results = (InlineQueryResultPhoto(
        id="photo-1",
        photo_url=
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Telegram_logo.svg/1200px-Telegram_logo.svg.png",
        thumb_url=
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Telegram_logo.svg/1200px-Telegram_logo.svg.png",
        title="results",
        description="find out with: {0}".format(query),
        caption="telegram photo",
        reply_markup=keyboard.markup(),
    ), )
    bot.answer_inline_query(inline_query_id=inline_query.id, results=results)


@router.chosen_inline_result_handler()
def on_chosen_inline_result(bot, chosen_inline_result):
    bot.send_message(
        chat_id=chosen_inline_result.from_user.id,
        text="you select: {0}".format(chosen_inline_result.result_id),
    )


@router.callback_query_handler(callback_data_name="show-url")
def on_show_url(bot, callback_query, query_result_id: str):
    print(query_result_id)
    bot.send_message(
        chat_id=callback_query.from_user.id,
        text=
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Telegram_logo.svg/1200px-Telegram_logo.svg.png",
    )


bot = bot_client.create_bot(token=BOT_TOKEN, router=router)
bot.delete_webhook(drop_pending_updates=True)
bot.run_polling(timeout=10)

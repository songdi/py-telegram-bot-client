"""
run in cli: python -m example.keyboard.py
"""
import logging
from simplebot.utils import parse_callback_data
from simplebot import bot_proxy, SimpleBot
from simplebot.base import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from simplebot.ui import Keyboard, MultiSelect, RadioGroup
from example.settings import BOT_TOKEN

logger = logging.getLogger("simple-bot")
logger.setLevel(logging.DEBUG)

router = bot_proxy.router()
example_bot = bot_proxy.create_bot(token=BOT_TOKEN, router=router)
example_bot.delete_webhook(drop_pending_updates=True)


@router.command_handler(cmds=("/reply",))
def on_reply_keyboard(bot: SimpleBot, message: Message):
    btn_text = KeyboardButton("click me")
    btn_contact = KeyboardButton("share your contact", request_contact=True)
    btn_location = KeyboardButton("share your location", request_location=True)
    keyboard = Keyboard()
    keyboard.add_buttons(btn_text, btn_contact, btn_location)
    keyboard.add_line(btn_text, btn_contact, btn_location)
    bot.send_message(
        chat_id=message.chat.id,
        text=message.text,
        reply_markup=ReplyKeyboardMarkup(keyboard=keyboard.layout, selective=True),
    )
    bot.join_force_reply(user_id=message.from_user.id, callback=on_reply_button_click)


@router.force_reply_handler()
def on_reply_button_click(bot: SimpleBot, message: Message):
    bot.force_reply_done(message.from_user.id)
    if message.text:
        bot.send_message(
            chat_id=message.chat.id,
            text="you click: {0}".format(message.text),
            reply_markup=ReplyKeyboardRemove(),
        )
        return
    if message.location:
        bot.send_message(
            chat_id=message.chat.id,
            text="a location is received",
            reply_markup=ReplyKeyboardRemove(),
        )
        return
    if message.contact:
        bot.send_message(
            chat_id=message.chat.id,
            text="a contact is received",
            reply_markup=ReplyKeyboardRemove(),
        )
        return


@router.command_handler(cmds=("/select",))
def on_select_keyboard(bot: SimpleBot, message: Message):
    radio_group = RadioGroup(name="radio-select")
    radio_group.add_options((True, "key1", "value1"), ("key2", "value2", True), ("key3", "value3"))
    multi_select = MultiSelect(name="mulit-select")
    multi_select.add_options(
        (True, "select1", "select-value1"),
        ("select2", "select-value2"),
        ("select3", "select-value3"),
    )
    radio_group.add_layout(multi_select.layout)
    radio_group.add_buttons(InlineKeyboardButton(text="submit", callback_data="submit"))
    bot.send_message(
        chat_id=message.chat.id,
        text=message.text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=radio_group.layout),
    )


@router.callback_query_handler(callable_match=parse_callback_data, name="mulit-select")
def on_select_button_click(bot, callback_query, *callback_data_args):
    mulit_select = MultiSelect(
        name="mulit-select", layout=callback_query.message.reply_markup.inline_keyboard
    )
    mulit_select.toggle(callback_data_args)
    bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=mulit_select.layout),
    )


@router.callback_query_handler(callable_match=parse_callback_data, name="radio-select")
def on_radio_button_click(bot, callback_query, *callback_data_args):
    radio_group = RadioGroup(
        name="radio-select", layout=callback_query.message.reply_markup.inline_keyboard
    )
    if radio_group.toggle(callback_data_args):
        bot.edit_message_reply_markup(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=radio_group.layout),
        )


@router.callback_query_handler(static_match="submit")
def on_submit(bot, callback_query):
    radio_group = RadioGroup(
        name="radio-select", layout=callback_query.message.reply_markup.inline_keyboard
    )
    multi_select = MultiSelect(
        name="mulit-select", layout=callback_query.message.reply_markup.inline_keyboard
    )
    bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=None,
    )
    bot.send_message(
        chat_id=callback_query.from_user.id,
        text="you select: {0} {1}".format(
            radio_group.selected_option, multi_select.selected_options
        ),
    )


example_bot.run_polling(timeout=10)

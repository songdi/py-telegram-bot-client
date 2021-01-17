"""
run in terminal: python -m example.media_group.py
"""
from example.settings import BOT_TOKEN
from simplebot import bot_proxy, SimpleBot
from simplebot.base import (
    Message,
    InputFile,
    InputMediaAudio,
    InputMediaPhoto,
    InputMediaVideo,
    InputMediaDocument,
)

router = bot_proxy.router()


@router.message_handler()
def on_reply_media_group(bot: SimpleBot, message: Message):
    thumb = InputFile("sample.jpg", "sample/sample.jpg")
    video = InputMediaVideo(media=InputFile("sample.mp4", "sample/sample.mp4"), thumb=thumb)
    photo = InputMediaPhoto(media=InputFile("sample.png", "sample/sample.png"))
    # Documents and audio files can be only grouped in an album with messages of the same type.
    document = InputMediaDocument(media=InputFile("sample.txt", "sample/sample.txt"), thumb=thumb)
    audio = InputMediaAudio(media=InputFile("sample.mp3", "sample/sample.mp3"), thumb=thumb)
    bot.send_media_group(message, media=(audio, audio))
    bot.reply_media_group(message, media=(video, photo))
    bot.reply_media_group(message, media=(document, document))


example_bot = bot_proxy.create_bot(token=BOT_TOKEN, router=router)
example_bot.delete_webhook(drop_pending_updates=True)
example_bot.run_polling(timeout=10)

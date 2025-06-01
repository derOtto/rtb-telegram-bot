import asyncio
import datetime
import logging
import os

from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
QUESTION = os.getenv(
    "QUESTION", "Bist du nächste Woche ({datetime}) zur Bandprobe anwesend?"
)
DAYS = os.getenv("DAYS", 7)
HOUR = os.getenv("HOUR", 18)
MINUTE = os.getenv("MINUTE", 0)
OPTIONS = os.getenv("OPTIONS", "Ja,Nein").split(",")

bot = Bot(token=BOT_TOKEN)


async def send_poll():
    try:
        next_date = datetime.datetime.now() + datetime.timedelta(days=DAYS)
        next_datetime = datetime.datetime.combine(
            next_date, datetime.time(hour=HOUR, minute=MINUTE)
        )
        await bot.send_poll(
            chat_id=CHAT_ID,
            question=QUESTION.format(
                datetime=next_datetime.strftime("%d.%m %H:%M Uhr")
            ),
            options=OPTIONS,
            is_anonymous=False,
            allows_multiple_answers=False,
        )
        logging.info("Poll sent successfully.")
    except TelegramError as e:
        logging.error(f"Error sending poll: {e}")


def main():
    asyncio.run(send_poll())

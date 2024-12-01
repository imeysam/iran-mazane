from telebot import TeleBot
from dotenv import load_dotenv
import os
from telebot.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from utils import get_jalali_datetime, Coin, Currency
from database import get_db
from models import User, Record
from sqlalchemy.orm import Session


load_dotenv()
bot = TeleBot(os.getenv("TOKEN"))
CHANNEL_SIGN = f"{os.getenv('CHANNEL_ID')} | {os.getenv('CHANNEL_TITLE')}"


def send_waiting_message(chat_id):
    bot.send_message(
        chat_id=chat_id,
        text=f"🔎 لطفا چند لحظه شکیبا باشید، ربات در حال جمع‌آوری اطلاعات است 🧐",
        parse_mode="Markdown",
    )


def send_price_list_message(chat_id, rows_header, rows):
    table_headers = [
        f"*{get_jalali_datetime()}*",
        rows_header
        # "*قیمت‌ها به تومان است «فروش --- خرید»*"
    ]

    table_rows = [row for row in rows]

    table = (
        "\n\n".join(table_headers) + 
        "\n\n" + 
        "\n".join(table_rows)+
        "\n\n" + CHANNEL_SIGN
    )

    db: Session = next(get_db())
    user = db.query(User).filter(User.chat_id == chat_id).first()
    user.api_call_count += 1
    user.step = 1
    db.commit()

    bot.send_message(
        chat_id=chat_id,
        text=f"\n{table}\n",
        parse_mode="Markdown",
        reply_markup=create_inline_buttons(),
    )


def create_inline_buttons():
    inline_keyboard = InlineKeyboardMarkup(row_width=2)
    inline_keyboard.add(
        InlineKeyboardButton(text="🌟 نرخ طلا و سکه", callback_data="btn_coin"),
        InlineKeyboardButton(text="💵 نرخ ارز", callback_data="btn_currency"),
    )
    return inline_keyboard


@bot.message_handler(commands=["start"])
def start(message):
    user_chat_id = message.chat.id
    db: Session = next(get_db())
    user = db.query(User).filter(User.chat_id == user_chat_id).first()
    if user is None:
        user = User(
            chat_id=user_chat_id,
            username=message.chat.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )
        db.add(user)
        db.commit()

    username = user
    text = "\n\n".join(
        [
            f"به *ایران مزنه* خوش اومدی"
            + (f"، @{user.username} عزیز" if user.username else ""),
            "برای نمایش نرخ آنلاین طلا، سکه و ارز 🌐💵 ",
            "از طریق این 👇 داشبورد ادامه بدید\n",
            CHANNEL_SIGN,
        ]
    )
    
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=create_inline_buttons(),
        parse_mode="Markdown",
    )


@bot.callback_query_handler(func=lambda call: call.data == "btn_coin")
def callback_btn_coin(call):
    send_waiting_message(call.message.chat.id)
    db_record = Record.get_record()
    
    gold = db_record.gold()
    emami = db_record.coin_emami()
    bahar = db_record.coin_bahar()
    nim = db_record.coin_nim()
    rob = db_record.coin_rob()
    gerami = db_record.coin_gerami()
    usd = db_record.currency_usd()
    ounce = gold.ounce
    
    
    rows = [
        str(gold),
        emami.show(ounce=ounce, usd=usd.sell),
        bahar.show(ounce=ounce, usd=usd.sell),
        nim.show(ounce=ounce, usd=usd.sell),
        rob.show(ounce=ounce, usd=usd.sell),
        gerami.show(ounce=ounce, usd=usd.sell),
    ]
    send_price_list_message(call.message.chat.id, Coin.message_header(), rows)


@bot.callback_query_handler(func=lambda call: call.data == "btn_currency")
def callback_btn_currency(call):
    send_waiting_message(call.message.chat.id)
    db_record = Record.get_record()
    rows = [
        str(db_record.currency_usd()),
        str(db_record.currency_eur()),
        str(db_record.currency_aed()),
        str(db_record.currency_gbp()),
        str(db_record.currency_try()),
        str(db_record.currency_chf()),
        str(db_record.currency_cny()),
        str(db_record.currency_jpy()),
        str(db_record.currency_cad()),
        str(db_record.currency_aud()),
        str(db_record.currency_sgd()),
        str(db_record.currency_inr()),
        str(db_record.currency_iqd()),
        str(db_record.currency_afn()),
        str(db_record.currency_dkk()),
        str(db_record.currency_sek()),
        str(db_record.currency_nok()),
        str(db_record.currency_sar()),
        str(db_record.currency_qar()),
        str(db_record.currency_omr()),
        str(db_record.currency_kwd()),
        str(db_record.currency_bhd()),
        str(db_record.currency_myr()),
        str(db_record.currency_thb()),
        str(db_record.currency_hkd()),
        str(db_record.currency_rub()),
        str(db_record.currency_azn()),
        str(db_record.currency_amd()),
    ]
    send_price_list_message(call.message.chat.id, Currency.message_header(), rows)


if __name__ == "__main__":
    from models import Base
    from database import engine

    Base.metadata.create_all(bind=engine)

    bot.polling()

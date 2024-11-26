from telebot import TeleBot
from dotenv import load_dotenv
import os
from telebot.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from crawler import get_mazane
from utils import get_jalali_datetime, to_persian_and_format
from database import get_db
from models import User
from sqlalchemy.orm import Session


load_dotenv()
bot = TeleBot(os.getenv("TOKEN"))


def prepare_title(title):
    return f"*{title}*".ljust(20)


def prepare_value_currency(key, data):
    return [
        "*" + to_persian_and_format(int(data.get(f"{key}1", 0))) + "*---" + to_persian_and_format(int(data.get(f"{key}2", 0))),
    ]
    # return [
    #     to_persian_and_format(int(json_data.get(f"{key}1", 0))),
    #     "\t",
    #     to_persian_and_format(int(json_data.get(f"{key}2", 0))),
    # ]


def prepare_value_coin(key, data):
    return [
        "*" + to_persian_and_format(int(data.get(f"{key}", 0))) + "*---" + to_persian_and_format(int(data.get(f"{key}2", 0))),
    ]
    # return [
    #     to_persian_and_format(int(json_data.get(f"{key}", 0))),
    #     "\t",
    #     to_persian_and_format(int(json_data.get(f"{key}2", 0))),
    # ]


def send_waiting_message(chat_id):
    bot.send_message(
        chat_id=chat_id,
        text=f"🔎 لطفا چند لحظه شکیبا باشید، ربات در حال جمع‌آوری اطلاعات است 🧐",
        parse_mode="Markdown",
    )


def send_cost(chat_id, rows):
    # Define your table data
    header = "*قیمت‌ها به تومان است* " + "*(فروش -- خرید)*"
    # Build a formatted string
    formatted_table = "\n\n".join([get_jalali_datetime(), header, ""])
    # formatted_table += "-" * 70 + "\n"  # A divider line
    for row in rows:
        formatted_table += "      ".join(row) + "\n"

    # Send the formatted table as a message
    # bot.send_message(chat_id, f"\n{formatted_table}\n", parse_mode="Markdown")

    db: Session = next(get_db())
    user = db.query(User).filter(User.chat_id == chat_id).first()
    user.api_call_count += 1
    user.step = 1
    db.commit()

    bot.send_message(
        chat_id=chat_id,
        text=f"\n{formatted_table}\n",
        parse_mode="Markdown",
        reply_markup=create_inline_button(),
    )


def create_inline_button():
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
        ]
    )

    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=create_inline_button(),
        parse_mode="Markdown",
    )


@bot.callback_query_handler(func=lambda call: call.data == "btn_coin")
def callback_btn_coin(call):
    send_waiting_message(call.message.chat.id)
    json_data = get_mazane()
    rows = [
        [
            prepare_title("طلا"),
            "*" + to_persian_and_format(int(json_data.get("gol18", 0))) + "*",
        ],
        [prepare_title("امامی"), *prepare_value_coin("emami1", data=json_data)],
        [prepare_title("بهار"), *prepare_value_coin("azadi1", data=json_data)],
        [prepare_title("نیم"), *prepare_value_coin("azadi1_2", data=json_data)],
        [prepare_title("ربع"), *prepare_value_coin("azadi1_4", data=json_data)],
        [prepare_title("گرمی"), *prepare_value_coin("azadi1g", data=json_data)],
    ]
    send_cost(call.message.chat.id, rows)


@bot.callback_query_handler(func=lambda call: call.data == "btn_currency")
def callback_btn_currency(call):
    send_waiting_message(call.message.chat.id)
    json_data = get_mazane()
    rows = [
        [prepare_title("دلار 🇺🇸"), *prepare_value_currency("usd", data=json_data)],
        [prepare_title("یورو 🇪🇺"), *prepare_value_currency("eur", data=json_data)],
        [
            prepare_title("درهم امارات 🇦🇪"),
            *prepare_value_currency("aed", data=json_data),
        ],
        [
            prepare_title("پوند انگلیس 🏴󠁧󠁢󠁥󠁮󠁧󠁿"),
            *prepare_value_currency("gbp", data=json_data),
        ],
        [prepare_title("لیر ترکیه 🇹🇷"), *prepare_value_currency("try", data=json_data)],
        [
            prepare_title("فرانک سوئیس 🇨🇭"),
            *prepare_value_currency("chf", data=json_data),
        ],
        [prepare_title("یوان چین 🇨🇳"), *prepare_value_currency("cny", data=json_data)],
        [prepare_title("ین ژاپن 🇯🇵"), *prepare_value_currency("jpy", data=json_data)],
        [
            prepare_title("دلار کانادا 🇨🇦"),
            *prepare_value_currency("cad", data=json_data),
        ],
        [
            prepare_title("دلار استرالیا 🇦🇺"),
            *prepare_value_currency("aud", data=json_data),
        ],
        [
            prepare_title("دلار سنگاپور 🇸🇬"),
            *prepare_value_currency("sgd", data=json_data),
        ],
        [prepare_title("روپیه هند 🇮🇳"), *prepare_value_currency("inr", data=json_data)],
        [
            prepare_title("دینار عراق 🇮🇶"),
            *prepare_value_currency("iqd", data=json_data),
        ],
        [prepare_title("افغانی 🇦🇫"), *prepare_value_currency("afn", data=json_data)],
        [
            prepare_title("کرون دانمارک 🇩🇰"),
            *prepare_value_currency("dkk", data=json_data),
        ],
        [prepare_title("کرون سوئد 🇸🇪"), *prepare_value_currency("sek", data=json_data)],
        [prepare_title("کرون نروژ 🇳🇴"), *prepare_value_currency("nok", data=json_data)],
        [
            prepare_title("ریال عربستان 🇸🇦"),
            *prepare_value_currency("sar", data=json_data),
        ],
        [prepare_title("ریال قطر 🇶🇦"), *prepare_value_currency("qar", data=json_data)],
        [prepare_title("ریال عمان 🇴🇲"), *prepare_value_currency("omr", data=json_data)],
        [
            prepare_title("دینار کویت 🇰🇼"),
            *prepare_value_currency("kwd", data=json_data),
        ],
        [
            prepare_title("دینار بحرین 🇧🇭"),
            *prepare_value_currency("bhd", data=json_data),
        ],
        [
            prepare_title("رینگیت مالزی 🇲🇾"),
            *prepare_value_currency("myr", data=json_data),
        ],
        [
            prepare_title("بات تایلند 🇹🇭"),
            *prepare_value_currency("thb", data=json_data),
        ],
        [
            prepare_title("دلار هنگ‌کنگ 🇭🇰"),
            *prepare_value_currency("hkd", data=json_data),
        ],
        [
            prepare_title("روبل روسیه 🇷🇺"),
            *prepare_value_currency("rub", data=json_data),
        ],
        [
            prepare_title("منات آذربایجان 🇦🇿"),
            *prepare_value_currency("azn", data=json_data),
        ],
        [
            prepare_title("درام ارمنستان 🇦🇲"),
            *prepare_value_currency("amd", data=json_data),
        ],
    ]
    send_cost(call.message.chat.id, rows)


if __name__ == "__main__":
    from models import Base
    from database import engine

    Base.metadata.create_all(bind=engine)

    bot.polling()

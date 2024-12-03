from database import Base, get_db
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timedelta
from typing import List
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Boolean,
    ForeignKey,
    Enum,
    JSON,
    DateTime,
    create_engine,
    desc,
    event,
)
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import func
from crawler import crawl_data
from utils import (
    Coin,
    Emami,
    Bahar,
    Nim,
    Rob,
    Gerami,
    Gold,
    USD,
    EUR,
    AED,
    GBP,
    TRY,
    CHF,
    CNY,
    JPY,
    CAD,
    AUD,
    SGD,
    INR,
    IQD,
    AFN,
    DKK,
    SEK,
    NOK,
    SAR,
    QAR,
    OMR,
    KWD,
    BHD,
    MYR,
    THB,
    HKD,
    RUB,
    AZN,
    AMD,
)

from dotenv import load_dotenv
import os
from services import Redis
import json

load_dotenv()
crawl_threshold_min = int(os.getenv("CRAWL_THRESHOLD_MIN", 1))


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    value = Column(JSON, nullable=False)  # JSON column for storing structured data
    created_at = Column(DateTime, server_default=func.now())

    def serializer_redis(self):
        return {
            "id": self.id,
            "value": self.value,
            "created_at": str(self.created_at),
        }

    @classmethod
    def crawl_and_store(cls, minutes):
        value = crawl_data()
        db: Session = next(get_db())
        if value != False:
            last_valid_record = cls(value=value)
            db.add(last_valid_record)
            db.commit()
            db.refresh(last_valid_record)
        else:
            last_valid_record = db.query(cls).order_by(desc(cls.created_at)).first()
        return last_valid_record

        # f = open("test_data.json", "r")
        # return f.read()

    @classmethod
    def fetch_or_crawl(cls, minutes=crawl_threshold_min):
        threshold_minutes_ago = datetime.utcnow() - timedelta(minutes=minutes)

        db: Session = next(get_db())

        # Query to get the last record within the time threshold
        last_valid_record = (
            db.query(cls)
            .filter(cls.created_at >= threshold_minutes_ago)
            .order_by(desc(cls.created_at))
            .first()
        )

        if last_valid_record is None:
            last_valid_record = cls.crawl_and_store(minutes=minutes)

        return last_valid_record

    @classmethod
    def get_record(cls):
        redis = Redis.client()
        if redis.exists("data"):
            redis_data = json.loads(redis.get("data"))
            return cls(**redis_data)
        record = cls.fetch_or_crawl()
        result = redis.setex("data", 60, json.dumps(record.serializer_redis()))
        return record

    def gold(self):
        price = int(self.value.get("gol18"))
        ounce = float(self.value.get("ounce"))
        return Gold(price=price, ounce=ounce)

    def coin_emami(self):
        sell = int(self.value.get("emami1"))
        buy = int(self.value.get("emami12"))
        bubble = int(self.value.get("emami1_bubble"))
        return Emami(sell=sell, buy=buy, bubble=bubble)

    def coin_bahar(self):
        sell = int(self.value.get("azadi1"))
        buy = int(self.value.get("azadi12"))
        bubble = int(self.value.get("azadi1_bubble"))
        return Bahar(sell=sell, buy=buy, bubble=bubble)

    def coin_nim(self):
        sell = int(self.value.get("azadi1_2"))
        buy = int(self.value.get("azadi1_22"))
        bubble = int(self.value.get("azadi1_2_bubble"))
        return Nim(sell=sell, buy=buy, bubble=bubble)

    def coin_rob(self):
        sell = int(self.value.get("azadi1_4"))
        buy = int(self.value.get("azadi1_42"))
        bubble = int(self.value.get("azadi1_4_bubble"))
        return Rob(sell=sell, buy=buy, bubble=bubble)

    def coin_gerami(self):
        sell = int(self.value.get("azadi1g"))
        buy = int(self.value.get("azadi1g2"))
        bubble = int(self.value.get("azadi1g_bubble"))
        return Gerami(sell=sell, buy=buy, bubble=bubble)

    def currency_usd(self):
        sell = int(self.value.get("usd1"))
        buy = int(self.value.get("usd2"))
        return USD(sell=sell, buy=buy)

    def currency_eur(self):
        sell = int(self.value.get("eur1"))
        buy = int(self.value.get("eur2"))
        return EUR(sell=sell, buy=buy)

    def currency_aed(self):
        sell = int(self.value.get("aed1"))
        buy = int(self.value.get("aed2"))
        return AED(sell=sell, buy=buy)

    def currency_gbp(self):
        sell = int(self.value.get("gbp1"))
        buy = int(self.value.get("gbp2"))
        return GBP(sell=sell, buy=buy)

    def currency_try(self):
        sell = int(self.value.get("try1"))
        buy = int(self.value.get("try2"))
        return TRY(sell=sell, buy=buy)

    def currency_chf(self):
        sell = int(self.value.get("chf1"))
        buy = int(self.value.get("chf2"))
        return CHF(sell=sell, buy=buy)

    def currency_cny(self):
        sell = int(self.value.get("cny1"))
        buy = int(self.value.get("cny2"))
        return CNY(sell=sell, buy=buy)

    def currency_jpy(self):
        sell = int(self.value.get("jpy1"))
        buy = int(self.value.get("jpy2"))
        return JPY(sell=sell, buy=buy)

    def currency_cad(self):
        sell = int(self.value.get("cad1"))
        buy = int(self.value.get("cad2"))
        return CAD(sell=sell, buy=buy)

    def currency_aud(self):
        sell = int(self.value.get("aud1"))
        buy = int(self.value.get("aud2"))
        return AUD(sell=sell, buy=buy)

    def currency_sgd(self):
        sell = int(self.value.get("sgd1"))
        buy = int(self.value.get("sgd2"))
        return SGD(sell=sell, buy=buy)

    def currency_inr(self):
        sell = int(self.value.get("inr1"))
        buy = int(self.value.get("inr2"))
        return INR(sell=sell, buy=buy)

    def currency_iqd(self):
        sell = int(self.value.get("iqd1"))
        buy = int(self.value.get("iqd2"))
        return IQD(sell=sell, buy=buy)

    def currency_afn(self):
        sell = int(self.value.get("afn1"))
        buy = int(self.value.get("afn2"))
        return AFN(sell=sell, buy=buy)

    def currency_dkk(self):
        sell = int(self.value.get("dkk1"))
        buy = int(self.value.get("dkk2"))
        return DKK(sell=sell, buy=buy)

    def currency_sek(self):
        sell = int(self.value.get("sek1"))
        buy = int(self.value.get("sek2"))
        return SEK(sell=sell, buy=buy)

    def currency_nok(self):
        sell = int(self.value.get("nok1"))
        buy = int(self.value.get("nok2"))
        return NOK(sell=sell, buy=buy)

    def currency_sar(self):
        sell = int(self.value.get("sar1"))
        buy = int(self.value.get("sar2"))
        return SAR(sell=sell, buy=buy)

    def currency_qar(self):
        sell = int(self.value.get("qar1"))
        buy = int(self.value.get("qar2"))
        return QAR(sell=sell, buy=buy)

    def currency_omr(self):
        sell = int(self.value.get("omr1"))
        buy = int(self.value.get("omr2"))
        return OMR(sell=sell, buy=buy)

    def currency_kwd(self):
        sell = int(self.value.get("kwd1"))
        buy = int(self.value.get("kwd2"))
        return KWD(sell=sell, buy=buy)

    def currency_bhd(self):
        sell = int(self.value.get("bhd1"))
        buy = int(self.value.get("bhd2"))
        return BHD(sell=sell, buy=buy)

    def currency_myr(self):
        sell = int(self.value.get("myr1"))
        buy = int(self.value.get("myr2"))
        return MYR(sell=sell, buy=buy)

    def currency_thb(self):
        sell = int(self.value.get("thb1"))
        buy = int(self.value.get("thb2"))
        return THB(sell=sell, buy=buy)

    def currency_hkd(self):
        sell = int(self.value.get("hkd1"))
        buy = int(self.value.get("hkd2"))
        return HKD(sell=sell, buy=buy)

    def currency_rub(self):
        sell = int(self.value.get("rub1"))
        buy = int(self.value.get("rub2"))
        return RUB(sell=sell, buy=buy)

    def currency_azn(self):
        sell = int(self.value.get("azn1"))
        buy = int(self.value.get("azn2"))
        return AZN(sell=sell, buy=buy)

    def currency_amd(self):
        sell = int(self.value.get("amd1"))
        buy = int(self.value.get("amd2"))
        return AMD(sell=sell, buy=buy)


@event.listens_for(Record, "before_insert")
def before_insert_calc_bubbles(mapper, connect, target):
    def calculate(sell_price, weight, ounce, usd):
        return sell_price - int(round((weight * 0.9 * ounce * usd) / 31.1035, -3))

    print(target.value)
    record_values = (
        json.loads(target.value) if type(target.value) is str else target.value
    )
    usd1 = int(record_values.get("usd1"))
    ounce = float(record_values.get("ounce"))

    bubbles = {}
    coins = {
        "emami1": 8.133,
        "azadi1": 8.133,
        "azadi1_2": 4.066,
        "azadi1_4": 2.033,
        "azadi1g": 1,
    }
    for coin_key, coin_weight in coins.items():
        sell_price = int(record_values.get(coin_key))
        weight = coin_weight
        bubbles[f"{coin_key}_bubble"] = calculate(sell_price, weight, ounce, usd1)

    target.value = {**bubbles, **record_values}


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    api_call_count = Column(Integer, default=0)
    
    
    @classmethod
    def find_or_create(cls, message):
        user_chat_id = message.chat.id
        db: Session = next(get_db())
        user = db.query(cls).filter(cls.chat_id == user_chat_id).first()
        if user is None:
            user = cls(
                chat_id=user_chat_id,
                username=message.chat.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        db.close()
        return user

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
    desc
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

load_dotenv()
crawl_threshold_min = int(os.getenv("CRAWL_THRESHOLD_MIN", 1))



class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    value = Column(JSON, nullable=False)  # JSON column for storing structured data
    created_at = Column(DateTime, server_default=func.now())

    @classmethod
    def get_record(cls, minutes=crawl_threshold_min):
        five_minutes_ago = datetime.utcnow() - timedelta(minutes=minutes)

        db: Session = next(get_db())

        # Query to get the last record within the time threshold
        last_valid_record = (
            db.query(cls)
            .filter(cls.created_at >= five_minutes_ago)
            .order_by(desc(cls.created_at))
            .first()
        )

        if last_valid_record is None:
            value = crawl_data()
            if value != False:
                last_valid_record = cls(value=value)
                db.add(last_valid_record)
                db.commit()
                db.refresh(last_valid_record)
            else:
                last_valid_record = (
                    db.query(cls).order_by(desc(cls.created_at)).first()
                )

        return last_valid_record
    
        # f = open("test_data.json", "r")
        # return f.read()

    def gold(self):
        price = int(self.value.get("gol18"))
        ounce = float(self.value.get("ounce"))
        return Gold(price=price, ounce=ounce)

    def coin_emami(self):
        sell = int(self.value.get("emami1"))
        buy = int(self.value.get("emami12"))
        return Emami(sell=sell, buy=buy)

    def coin_bahar(self):
        sell = int(self.value.get("azadi1"))
        buy = int(self.value.get("azadi12"))
        return Bahar(sell=sell, buy=buy)

    def coin_nim(self):
        sell = int(self.value.get("azadi1_2"))
        buy = int(self.value.get("azadi1_22"))
        return Nim(sell=sell, buy=buy)

    def coin_rob(self):
        sell = int(self.value.get("azadi1_4"))
        buy = int(self.value.get("azadi1_42"))
        return Rob(sell=sell, buy=buy)

    def coin_gerami(self):
        sell = int(self.value.get("azadi1g"))
        buy = int(self.value.get("azadi1g2"))
        return Gerami(sell=sell, buy=buy)

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


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    api_call_count = Column(Integer, default=0)

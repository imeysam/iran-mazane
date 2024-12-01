import jdatetime
import pytz


def get_jalali_datetime():
    # Define Tehran timezone
    tehran_tz = pytz.timezone('Asia/Tehran')
    # Get the current datetime in Tehran timezone
    tehran_time = jdatetime.datetime.now(tehran_tz)
    # Format the date and time
    jalali_date = tehran_time.strftime("%Y/%m/%d")
    jalali_time = tehran_time.strftime("%H:%M:%S")
    return f"📅 {to_persian_number(jalali_date + ' ' + jalali_time)}"



def to_persian_number(number):
    # Map English digits to Persian digits
    persian_digits = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
    
    # Replace English digits with Persian digits
    return number.translate(persian_digits)


def to_persian_and_format(number):
    # Ensure the input is an integer
    if not isinstance(number, (int, float)):
        raise ValueError("Input must be a numeric type.")

    # Format the number with commas
    number_str = f"{int(number):,}"  # Add commas for thousands separator
    
    # Map English digits to Persian digits
    persian_digits = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
    
    # Replace English digits with Persian digits
    return number_str.translate(persian_digits)


class Gold:
    def __init__(self, price, ounce):
        self.price = price
        self.ounce = ounce
        self.title = "طلا"
    
    def __str__(self):
        return "".join([
            f"*{self.title}*".ljust(20),
            "*" + to_persian_and_format(int(self.price)) + "*",
        ])
        
class Coin:
    def __init__(self, sell, buy):
        self.sell = sell
        self.buy = buy
    
    @staticmethod
    def message_header():
        return "*قیمت‌ها به تومان است «فروش --- خرید --- حباب»*"
        
    def bubble(self, ounce, usd) -> int :
        # (8.133*0.916*2649.87*70420/31.1035)
        print(self.weight , 0.9 , ounce , usd, 31.1035)
        return self.sell - int(
            round(
                (self.weight * 0.9 * ounce * usd) / 31.1035, -3
            )
        )
    
    def show(self, ounce, usd):
        return "".join([
            f"*{self.title}*".ljust(20),
            (
                "*" + to_persian_and_format(int(self.sell)) + 
                "* --- " + to_persian_and_format(int(self.buy)) + 
                " --- *" + to_persian_and_format(self.bubble(ounce, usd)) + "*"
            )
        ])
        
    def __str__(self):
        return "".join([
            f"*{self.title}*".ljust(20),
            "*" + to_persian_and_format(int(self.sell)) + "* --- " + to_persian_and_format(int(self.buy))
        ])
        # return f"sell:{self.sell},\tbuy:{self.buy}"
        
    def __repr__(self):
        return str(self)
        # return f"sell:{self.sell},\tbuy:{self.buy}"


class Emami(Coin):
    def __init__(self, sell, buy):
        super().__init__(sell, buy)
        self.title = "امامی"
        self.weight = 8.133
    

class Bahar(Coin):
    def __init__(self, sell, buy):
        super().__init__(sell, buy)
        self.title = "بهار"
        self.weight = 8.133
        
    
class Nim(Coin):
    def __init__(self, sell, buy):
        super().__init__(sell, buy)
        self.title = "نیم"
        self.weight = 4.066
        
    
class Rob(Coin):
    def __init__(self, sell, buy):
        super().__init__(sell, buy)
        self.title = "ربع"
        self.weight = 2.033
        
    
class Gerami(Coin):
    def __init__(self, sell, buy):
        super().__init__(sell, buy)
        self.title = "گرمی"
        self.weight = 1


     
class Currency:
    def __init__(self, sell, buy):
        self.sell = sell
        self.buy = buy
    
    @staticmethod
    def message_header():
        return "*قیمت‌ها به تومان است «فروش --- خرید»*"
    
    def __str__(self):
        return "".join([
            f"*{self.title}*".ljust(25),
            "*" + to_persian_and_format(int(self.sell)) + "* --- " + to_persian_and_format(int(self.buy))
        ])

class USD(Currency):
    def __init__(self, sell, buy):
        super().__init__(sell, buy)
        self.title = "دلار 🇺🇸"

class EUR(Currency):
    def __init__(self, sell, buy):
        super().__init__(sell, buy)
        self.title = "یورو 🇪🇺"

class AED(Currency):
    def __init__(self, sell, buy):
        super().__init__(sell, buy)
        self.title = "درهم امارات 🇦🇪"

class GBP(Currency):
    def __init__(self, sell, buy):
        super().__init__(sell, buy)
        self.title = "پوند انگلیس 🏴󠁧󠁢󠁥󠁮󠁧󠁿"

class TRY(Currency):
    def __init__(self, sell, buy):
        super().__init__(sell, buy)
        self.title = "لیر ترکیه 🇹🇷"

class CHF(Currency):
    def __init__(self, sell, buy):
        super().__init__(sell, buy)
        self.title = "فرانک سوئیس 🇨🇭"

class CNY(Currency):
    def __init__(self, sell, buy):
        super().__init__(sell, buy)
        self.title = "یوان چین 🇨🇳"

class JPY(Currency):
    def __init__(self, sell, buy):
        super().__init__(sell, buy)
        self.title = "ین ژاپن 🇯🇵"

class CAD(Currency):
    def __init__(self, sell, buy):
        super().__init__(sell, buy)
        self.title = "دلار کانادا 🇨🇦"

class AUD(Currency):
    def __init__(self, sell, buy):
        super().__init__(sell, buy)
        self.title = "دلار استرالیا 🇦🇺"

class SGD(Currency):
    def __init__(self, sell, buy):
        super().__init__(sell, buy)
        self.title = "دلار سنگاپور 🇸🇬"

class INR(Currency):
    def __init__(self, sell, buy):
        super().__init__(sell, buy)
        self.title = "روپیه هند 🇮🇳"

class IQD(Currency):
    def __init__(self, sell, buy):
        super().__init__(sell, buy)
        self.title = "دینار عراق 🇮🇶"

class AFN(Currency):
    def __init__(self, sell, buy):
        super().__init__(sell, buy)
        self.title = "افغانی 🇦🇫"

class DKK(Currency):
    def __init__(self, sell, buy):
        super().__init__(sell, buy)
        self.title = "کرون دانمارک 🇩🇰"

class SEK(Currency):
    def __init__(self, sell, buy):
        super().__init__(sell, buy)
        self.title = "کرون سوئد 🇸🇪"

class NOK(Currency):
    def __init__(self, sell, buy):
        super().__init__(sell, buy)
        self.title = "کرون نروژ 🇳🇴"

class SAR(Currency):
    def __init__(self, sell, buy):
        super().__init__(sell, buy)
        self.title = "ریال عربستان 🇸🇦"

class QAR(Currency):
    def __init__(self, sell, buy):
        super().__init__(sell, buy)
        self.title = "ریال قطر 🇶🇦"

class OMR(Currency):
    def __init__(self, sell, buy):
        super().__init__(sell, buy)
        self.title = "ریال عمان 🇴🇲"

class KWD(Currency):
    def __init__(self, sell, buy):
        super().__init__(sell, buy)
        self.title = "دینار کویت 🇰🇼"

class BHD(Currency):
    def __init__(self, sell, buy):
        super().__init__(sell, buy)
        self.title = "دینار بحرین 🇧🇭"

class MYR(Currency):
    def __init__(self, sell, buy):
        super().__init__(sell, buy)
        self.title = "رینگیت مالزی 🇲🇾"

class THB(Currency):
    def __init__(self, sell, buy):
        super().__init__(sell, buy)
        self.title = "بات تایلند 🇹🇭"

class HKD(Currency):
    def __init__(self, sell, buy):
        super().__init__(sell, buy)
        self.title = "دلار هنگ‌کنگ 🇭🇰"

class RUB(Currency):
    def __init__(self, sell, buy):
        super().__init__(sell, buy)
        self.title = "روبل روسیه 🇷🇺"

class AZN(Currency):
    def __init__(self, sell, buy):
        super().__init__(sell, buy)
        self.title = "منات آذربایجان 🇦🇿"

class AMD(Currency):
    def __init__(self, sell, buy):
        super().__init__(sell, buy)
        self.title = "درام ارمنستان 🇦🇲"
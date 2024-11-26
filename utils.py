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


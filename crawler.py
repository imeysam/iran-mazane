import requests
from bs4 import BeautifulSoup
import re
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, desc
from datetime import datetime, timedelta
from database import get_db
from models import User, Record
from sqlalchemy.orm import Session


def get_param():
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }

    # Full page source stored in a variable
    r = requests.get("https://www.bonbast.com", headers=headers)
    html = r.content

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Find all <script> tags
    script_tags = soup.find_all("script")

    # Define the regular expression to match the line
    pattern = r'param: "([^"]+)"'

    code = None
    # Loop through the script tags and search for the pattern
    for script in script_tags:
        if script.string:  # Check if script tag contains a string
            match = re.search(pattern, script.string)
            if match:
                extracted_line = match.group(0)  # Full matched line
                extracted_value = match.group(1)  # The value inside quotes
                code = extracted_value
                # print("Extracted Line:", extracted_line)
                # print("Extracted Value:", extracted_value)
    return code


def get_data(param):
    url = "https://www.bonbast.com/json"

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": "st_bb=0; _gid=GA1.2.742130997.1732602871; FCCDCF=%5Bnull%2Cnull%2Cnull%2C%5B%22CQIspsAQIspsAEsACBENBRFoAP_gAEPgACiQINJD7C7FbSFCwH5zaLsAMAhHRsAAQoQAAASBAmABQAKQIAQCgkAQFASgBAACAAAAICRBIQIECAAAAUAAQAAAAAAEAAAAAAAIIAAAgAEAAAAIAAACAIAAEAAIAAAAEAAAmAgAAIIACAAAgAAAAAAAAAAAAAAAAgCAAAAAAAAAAAAAAAAAAQOhSD2F2K2kKFkPCmwXYAYBCujYAAhQgAAAkCBMACgAUgQAgFJIAgCIFAAAAAAAAAQEiCQAAQABAAAIACgAAAAAAIAAAAAAAQQAABAAIAAAAAAAAEAQAAIAAQAAAAIAABEhCAAQQAEAAAAAAAQAAAAAAAAAAABAAA%22%2C%222~70.89.93.108.122.149.196.236.259.311.313.323.358.415.449.486.494.495.540.574.609.864.981.1029.1048.1051.1095.1097.1126.1205.1276.1301.1365.1415.1449.1514.1570.1577.1598.1651.1716.1735.1753.1765.1870.1878.1889.1958.1960.2072.2253.2299.2373.2415.2506.2526.2531.2568.2571.2575.2624.2677.2778~dv.%22%2C%2286D2D715-C9DA-4B89-881F-1BD539332CCA%22%5D%5D; _ga=GA1.2.1007187138.1732602870; __gads=ID=ca8408a92c923e57:T=1732602871:RT=1732606826:S=ALNI_MbCYJ2i1lWuqJWoYS3SBHAWQpuUDQ; __gpi=UID=00000f5a9eb4848f:T=1732602871:RT=1732606826:S=ALNI_Mb_fjZoreh6aHV_erRc2fVppde4KA; __eoi=ID=59301d48b57726ec:T=1732602871:RT=1732606826:S=AA-AfjbR-pJ8bWZvL4LWb_xjQcS0; FCNEC=%5B%5B%22AKsRol8_D2lwpfdkUf1xW08_f2fOHNI_WvfCTSpbZoPdwyDjQXKFisFMt40LpQIfbdaKtUTDsWtshKSimsBeWjlP5i8_9QRC8Cw_-LbHJHWg72Mr7ff5toFyb6tKSW29FUC3u0exkYwQmYJt8QVDmYYmTAH8qGQ0tw%3D%3D%22%5D%5D; _ga_PZF6SDPF22=GS1.1.1732602869.1.1.1732606941.0.0.0",
        "origin": "https://www.bonbast.com",
        "priority": "u=1, i",
        "referer": "https://www.bonbast.com/",
        "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }

    data = {"param": param}

    response = requests.post(url, headers=headers, data=data)

    return response.json()



def crawl_data():
    param = get_param()

    if param is None:
        return False
    return get_data(param=param)


def get_mazane():
    # Calculate the time threshold
    five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)

    db: Session = next(get_db())

    # Query to get the last record within the time threshold
    last_valid_record = (
        db.query(Record)
        .filter(Record.created_at >= five_minutes_ago)
        .order_by(desc(Record.created_at))
        .first()
    )

    if last_valid_record is None:
        value = crawl_data()
        if value != False:
            last_valid_record = Record(value=value)
            db.add(last_valid_record)
            db.commit()
        else:
            last_valid_record = (
                db.query(Record).order_by(desc(Record.created_at)).first()
            )

    return last_valid_record.value

    # f = open("test_data.json", "r")
    # return f.read()


if __name__ == "__main__":
    print(get_mazane())

import re
import os
import requests
import uuid
import datetime
from dateutil.relativedelta import relativedelta
from RPA.Excel.Files import Files

def create_image_folder() -> None:
    dir = "./images"
    if not os.path.exists(dir):
        os.makedirs(dir)

def write_csv_data(data: list) -> None:
    lib = Files()
    lib.create_workbook()
    lib.append_rows_to_worksheet(data)
    lib.save_workbook("result.xlsx")

def download_image_from_url(image_url: str) -> str:
    image_name = str(uuid.uuid4())
    if image_url == "":
        return ""
    img_data = requests.get(image_url).content
    with open(f"./images/{image_name}.jpg", "wb") as handler:
        handler.write(img_data)
    return image_name

def count_matches(pattern: str, text: str, count=0) -> int:
    full_pattern= r"\b" + pattern + r"\b"
    matches = len(re.findall(full_pattern, text, flags=re.IGNORECASE))
    return matches

def check_for_dolar_sign(text: str) -> bool:
    pattern = r'\$\d{1,3}(?:,\d{3})*(?:\.\d{1,2})|\b\d+\s*(?:dollars|USD)\b'

    if re.search(pattern, text):
        return True
    return False

def format_date(news_date: str) -> str:
    general_pattern = r'\b\d+\s*(seconds?|minutes?|hours?|days?|weeks?)\s+ago\b'
    singular_pattern = r'\b\d+\s*(second|minute|hour|day|week)\s+ago\b'
    try:
        if re.search(general_pattern, news_date):
            parsed_s = [news_date.split()[:2]]
            if re.search(singular_pattern, news_date):
                parsed_s[0][1] = parsed_s[0][1] + "s"
            time_dict = dict((fmt,float(amount)) for amount,fmt in parsed_s)
            dt = datetime.timedelta(**time_dict)
            formated_date = datetime.datetime.now() - dt
            print(formated_date)
            return formated_date
        else:
            formated_date = datetime.datetime.strptime(news_date,'%B %d, %Y')
            return formated_date
    except ValueError as e:
        raise f"Error on execution of format_date -> {e}"

def date_limit(n_months: int) -> str:
    if n_months in (0,1):
        limit_date = datetime.datetime.today().replace(day=1)     
    else:
        limit_date = datetime.datetime.today().replace(day=1) - relativedelta(months =n_months)
    return limit_date  
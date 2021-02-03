import requests
from bs4 import BeautifulSoup
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

AMAZON_URL = os.getenv("AMAZON_URL")
ACCEPT_LANGUAGE = os.getenv("ACCEPT_LANGUAGE")
USER_AGENT = os.getenv("USER_AGENT")

my_email = os.getenv("SMTP_MY_EMAIL")
my_password = os.getenv("SMTP_MY_PASSWORD")
recipient_email = os.getenv("SMTP_RECEPIENT")

HEADERS = {
    "Accept-Language": ACCEPT_LANGUAGE,
    "User-Agent": USER_AGENT,
}

response = requests.get(url=AMAZON_URL, headers=HEADERS)

soup = BeautifulSoup(response.text, "html.parser")

price_tag = soup.find("span", id="priceblock_ourprice")
product_title = soup.find("span", id="productTitle")

price = \
    str(price_tag).split(
        '<span class="a-size-medium a-color-price priceBlockBuyingPriceString" id="priceblock_ourprice">')[
        1].split("</span>")[0]

product = \
    str(product_title).split('<span class="a-size-large product-title-word-break" id="productTitle">')[
        1].split("</span>")[0]

product = product.strip()

price = float(price.split("£")[1])

if price < 400:
    with smtplib.SMTP("smtp.mail.yahoo.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(from_addr=my_email,
                            to_addrs=recipient_email,
                            msg=f"Amazon Price Alert\n\n{product} is now £{price}\n{AMAZON_URL}".encode("utf-8"))
else:
    print("Price has not hit target yet.")

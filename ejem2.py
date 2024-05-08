from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json

ruta_chromedriver = ChromeDriverManager().install()
s = Service(ruta_chromedriver)
driver = webdriver.Chrome(service=s)

print(ruta_chromedriver)

url = "https://portal.tutorialsdojo.com/product/aws-certified-sysops-administrator-associate-practice-exams/"
ua = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
}

driver.get(url)

soup = BeautifulSoup(driver.page_source, "html.parser")

print(soup.title.text)
print(soup.select_one("p.price span.woocommerce-Price-currencySymbol"))

price_element = soup.select_one("p.price span.woocommerce-Price-currencySymbol")
precio = price_element.find_next("bdi").text.strip()
print("Precio:", precio)


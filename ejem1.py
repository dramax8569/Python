from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import json

ruta_chromedriver = ChromeDriverManager().install()
s = Service(ruta_chromedriver)
driver = webdriver.Chrome(service=s)

print(ruta_chromedriver)

url = "https://www.udemy.com/course/ultimate-aws-certified-sysops-administrator-associate/?couponCode=LETSLEARNNOW"
ua = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
}

driver.get(url)

soup = BeautifulSoup(driver.page_source, "html.parser")

script = soup.find("script", {"data-purpose": "safely-set-inner-html:course-landing-page/seo-info"})
script_content = script.string
data = json.loads(script_content)
precio = data[0]["offers"][0]["price"]
print("Precio del curso:", precio)



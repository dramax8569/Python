from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from config_amazon import *
import time
import pickle
import os
import sys


def iniciar_chrome():
    ruta = ChromeDriverManager().install()
    
    options = Options()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    options.add_argument(f"user-agent={user_agent}")
    #options.add_argument("--headless") # no se abra la ventana de chrome
    options.add_argument("--windows-size=970,1080") # alto y ancho de la ventana
    options.add_argument("--start-maximized") # maximizar la ventana
    options.add_argument("--disable-web-security") # deshabilita la politica del mismo origen
    options.add_argument("--disable-extensions") # para que no cargue las extensiones
    options.add_argument("--disable-notifications") # para bloquear las notificaciones de chrome
    options.add_argument("--ignore-certificate-errors") # para ignorar el aviso (la conexion no es privada)
    options.add_argument("--no-sandbox") # deshabilita el modo sandboc
    options.add_argument("--log-level=3") # para que chromedriver no muestre nada en la terminal
    options.add_argument("--allow-running-insecure-content") # desactiva el aviso "contenido no seguro"
    options.add_argument("--no-default-browser-check") # 
    options.add_argument("--no-first-run") # 
    options.add_argument("--no-proxy-server") # para no usar proxy, si no, conexiones directas
    options.add_argument("--disable-blink-features=AutomationControlled") # evita el aviso "navegador por defecto"
    # options.add_argument("") # 

    # parametros a omitir en el inicio de chromedriver
    exp_opt = [
        'enable-automation'
        'ingore-certificated-errors'
        'enable-logging'
    ]
    options.add_experimental_option("excludeSwitches", exp_opt)
    #parametros que definen preferencias en chromedriver
    prefs = {
        "profile.default_content_setting_values.notifications" : 2,
        "intl.accept_languajes" : ["es-ES", "es"],
        "credentials_enable_service" : False
    }
    options.add_experimental_option("prefs", prefs)
    s = Service(ruta)
    driver = webdriver.Chrome(service=s, options=options)
    driver.set_window_position(0,0)
    return driver


def login_amazon():
    #realiza login

    #comprobamos si existe el archivo de cookies
    
    if os.path.isfile("amazon.cookies"):
        print('Login en Amazon por Cookies')
        cookies=pickle.load(open("amazon.cookies", "rb"))
        driver.get("https://www.amazon.com/robots.txt")
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get("https://www.amazon.com/-/es/gp/css/order-history?ref_=nav_orders_first")
        print("OK 1")
    else: 
        print('Login Amazon con Inicio de Sesion')
        driver.get("https://www.amazon.com/your-orders/orders?_encoding=UTF8&language=es&ref_=nav_orders_first")
        try:
            elemento = wait.until(ec.visibility_of_element_located((By.NAME, "email")))
        except TimeoutException:
            print("ERROR: Elemento 'email' no disponible")
            return "ERROR"
        elemento.send_keys(USER_AMAZON_1)
        elemento = wait.until(ec.visibility_of_element_located((By.NAME, "password")))
        elemento.send_keys(PASS_AMAZON_1)
        input("Pulsa Enter para salir")
        elemento = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "input#signInSubmit.a-button-input")))
        elemento.click()

        #guardamos las cookies con pickle
        cookies = driver.get_cookies()
        pickle.dump(cookies, open("amazon.cookies", "wb"))
        print('Cookies guardadas')
        return "OK 2"

def cambiar_estado():
    num_pagina = 1  # Inicializamos el contador de páginas
    while num_pagina <= 3:  # Modificamos la condición del bucle
        try:
            # Buscamos el elemento "Revisar la forma de pago" en la página actual
            elemento = wait.until(ec.visibility_of_element_located((By.XPATH, "//a[contains(text(),'Revisar la forma de pago')]")))
            print("Elemento encontrado en la página actual")
            elemento.click()  # Hacemos clic en el elemento
            elemento = wait.until(ec.visibility_of_element_located((By.NAME, "ppw-widgetEvent:SetPaymentPlanSelectContinueEvent")))
            elemento.click()  # Continuamos con la acción requerida
            print("Visitando página-:", num_pagina)
            driver.get(f"https://www.amazon.com/-/es/your-orders/orders?_encoding=UTF8&language=es&startIndex={num_pagina}0")
        except TimeoutException:
            # Si no se encuentra el elemento en la página actual, pasamos a la siguiente página
            print("Elemento no encontrado en la página actual")
            driver.get(f"https://www.amazon.com/-/es/your-orders/orders?_encoding=UTF8&language=es&startIndex={num_pagina}0")
            print("Visitando página:", num_pagina)
            num_pagina += 1  # Incrementamos el contador de página

    print("Se ha alcanzado el límite de páginas sin encontrar el elemento.")


if __name__ == '__main__':
    driver = iniciar_chrome()
    wait = WebDriverWait(driver, 10)
    res = login_amazon()
    if res == "ERROR 1":
        input("Pulsa Enter para salir")
        driver.quit()
        sys.exit(1)
    else: 
        cambiar_estado()
        driver.quit()
    
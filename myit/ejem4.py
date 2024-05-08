from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from config_myit import *
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


def login_myit():
        print('Login Myit con Inicio de Sesion')
        driver.get("https://myit.claro.com.co:8443/dwp/app/#/srm/profile/SRGlbtarmdevapPEGAFDPDJ68FGSFA/srm")
        try:
            elemento = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "input#adapt-textfield-0_input")))        
        except TimeoutException:
            print("ERROR: Elemento 'Nombre de usuario' no disponible")
            return "ERROR"
        elemento.send_keys(USER_MYIT_1)
        elemento = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "input#adapt-textfield-1_input")))
        elemento.send_keys(PASS_MYIT_1)
        elemento = wait.until(ec.visibility_of_element_located((By.XPATH, "//button[contains(text(),' Iniciar sesión ')]")))
        elemento.click()


def llenar_formulario():
    input("Pulsa Enter para salir")

    #boton sede
    # Hacer clic en el botón de alternancia para mostrar las opciones
    elemento_alternancia = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "button#adapt-select-1_button")))
    elemento_alternancia.click()

    # Esperar un breve momento para que las opciones se carguen, ajusta según sea necesario
    time.sleep(2)

    # Verificar si las opciones están presentes en el DOM
    opciones_presentes = driver.find_elements(By.XPATH, "//div[@class='dropdown_select__menu-content']//button[contains(@class, 'dropdown-item')]")
    if opciones_presentes:
        print("Las opciones están presentes:")
        for opcion in opciones_presentes:
            print(opcion.text)
    else:
        print("No se encontraron opciones.")




    input("Pulsa Enter para salir")
    #boton Tipo de Operación
    elemento = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "button#adapt-select-3_button")))
    elemento.click()

    
    elemento = wait.until(ec.visibility_of_element_located((By.XPATH, "//button[contains(text(),'Transversal')]")))
    elemento.click()

    input("Pulsa Enter para salir")
    

if __name__ == '__main__':
    driver = iniciar_chrome()
    wait = WebDriverWait(driver, 10)
    res = login_myit()
    res = llenar_formulario()
    if res == "ERROR":
        input("Pulsa Enter para salir")
        driver.quit()
        sys.exit(1)
    input("Pulsa Enter para salir")
    driver.quit()
import os
import time

import requests
import undetected_chromedriver as uc
from apscheduler.schedulers.blocking import BlockingScheduler
from selenium.webdriver.common.by import By

CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH')
BOT_NUMBER = os.getenv('BOT_NUMBER')
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')
CHAT_ID = os.getenv('CHAT_ID')

sched = BlockingScheduler()


def sendStockMessage():
    message = "Hay Stock de figus pack 25"
    URL = "https://api.telegram.org/" + BOT_NUMBER + ":" + TELEGRAM_API_KEY + "/sendMessage?chat_id=" + CHAT_ID + "&text=" + message
    requests.get(url=URL)


@sched.scheduled_job('interval', minutes=1)
def searchFigusStock():
    print("Arranca Panini")
    chrome_options = uc.ChromeOptions()
    chrome_options.headless = True
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = uc.Chrome(options=chrome_options,
                       driver_executable_path=CHROMEDRIVER_PATH)
    driver.get("https://www.zonakids.com/productos/pack-x-25-sobres-de-figuritas-fifa-world-cup-qatar-2022/")

    time.sleep(5)
    print(driver.title)
    try:
        stock = driver.find_element(By.XPATH, "(//span[@class='label-text'])[1]").text
        print("Encontramos la palabra: ", stock)
        sendStockMessage()
        if (stock != 'SIN STOCK'):
            sendStockMessage()
    except:
        print("Hubo un error, entonces hay stock")
        sendStockMessage()
    driver.close()
    driver.quit()


sched.start()

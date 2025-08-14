from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import os
import glob


def click_button(url, xpath_buttom):

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        driver.get(url)

        wait = WebDriverWait(driver, 5)

        download_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, xpath_buttom))
        )

        driver.execute_script(
            "arguments[0].scrollIntoView();", download_button)

        download_button.click()

        time.sleep(5)

        print("Скачивание начато успешно!")

    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
    finally:
        driver.quit()


def find_latest_added_file(directory):
    try:
        # Получаем список файлов с проверкой существования директории
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Директория {directory} не существует")

        files = [f for f in glob.glob(os.path.join(directory, '*'))
                 if os.path.isfile(f)]

        if not files:
            return None

        latest_file = max(files, key=os.path.getctime)

        return latest_file

    except Exception as e:
        print(f"Ошибка: {e}")
        return None


target_dir = '/Users/ushakovalex/Downloads/'

urls_dic = {
    'https://abit.itmo.ru/program/master/ai': '//*[@id="__next"]/div/main/div[3]/div[4]/div/div/button',
    'https://abit.itmo.ru/program/master/ai_product': '//*[@id="__next"]/div/main/div[3]/div[4]/div/div/button'
}

file_path_dic = {}

for url in urls_dic.keys():

    click_button(url, urls_dic[url])

    latest = find_latest_added_file(target_dir)

    if latest:
        file_path_dic[url] = latest
        ctime = os.path.getctime(latest)
        print(f"\nПоследний добавленный файл: {os.path.basename(latest)}")
        print(f"Полный путь: {latest}")
        print(
            f"Создан: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ctime))}")
        print(f"Размер: {os.path.getsize(latest)} байт")
    else:
        print("Файлы не найдены")

file_path_dic

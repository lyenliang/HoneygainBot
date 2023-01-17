import json
import logging
import os
import time
from logging.handlers import RotatingFileHandler

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

import config
import secrets

class HoneygainBot:
    def __init__(self):
        self.init_logger()
        self.target_url = "https://dashboard.honeygain.com/"
        options = webdriver.ChromeOptions()
        options.add_argument("disable-dev-shm-usage")
        options.add_argument("no-sandbox")
        options.add_argument('headless')
        options.add_argument("--nogpu")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280,1280")
        options.add_argument("--enable-javascript")
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
        options.add_argument('user-agent={0}'.format(user_agent))
        options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=chrome_service, options=options)
        self.driver.implicitly_wait(10)

    def init_logger(self):
        self.logger = logging.getLogger("honeygain_bot")
        self.logger.setLevel(logging.INFO)
        file_handler = RotatingFileHandler(
            "honeygain_bot.log",
            mode="a",
            maxBytes=config.LogSetting.max_bytes,
            backupCount=config.LogSetting.backup_count,
            encoding=None,
            delay=0,
        )
        file_handler.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def claim_lucky_pot(self):
        self.login()
        self.click_lucky_pot_button()

    def login(self):
        self.logger.info(f"Logging in ...")
        self.driver.get("https://dashboard.honeygain.com/")
        if os.path.exists(config.cookie_path):
            self.logger.info("Found previous cookies. Use cookies and local storages to login")
            self.load_cookies()
            self.load_local_storages()
            self.driver.refresh()
        else:
            # Ref: https://www.selenium.dev/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.expected_conditions.html
            # accept cookie
            self.logger.info("Previous cookies not found. Use email and password to login")
            self.driver.find_element(
                By.XPATH, "//div[@id='root']/div[3]/div/div/div[2]/div[2]/button[2]"
            ).click()
            # email
            self.driver.find_element(By.XPATH, "//input[@value='']").send_keys(
                secrets.email
            )
            # Password
            self.driver.find_element(By.XPATH, "//input[@value='']").send_keys(
                secrets.password
            )
            # Login with email
            self.driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/main/div[2]/div/div[2]/div/form/button/span').click()
            time.sleep(3)
            self.save_cookies()
            self.save_local_storages()

    def click_lucky_pot_button(self):
        self.logger.info(f"Clicking lucky pot button ...")
        # A screenshot is required for headless mode to work
        self.driver.get_screenshot_as_file('/tmp/screenshot.png')
        try:
            # Open Lucky Pot
            WebDriverWait(self.driver, 15).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div[2]/div[2]/div/main/div/div/div[2]/div/div[1]/div/div/div/div[5]/div/div/button'))).click()

        except TimeoutException as e:
            # lucky pot button not found
            self.logger.warning(
                f"Lucky pot button not found. You may have opened lucky pot, or you haven't shared enough traffic today. {e}"
            )
            exit()
        self.logger.info("Lucky pot was opened.")

    def save_cookies(self):
        self.logger.info(f"Saving cookies ...")
        cookies = self.driver.get_cookies()
        with open("cookies.json", "w") as file_out:
            json.dump(cookies, file_out)

    def load_cookies(self):
        self.logger.info(f"Loading cookies ...")
        with open(config.cookie_path) as json_file:
            cookies = json.load(json_file)
            for cookie in cookies:
                self.driver.add_cookie(cookie)

    def save_local_storages(self):
        self.logger.info(f"Saving local storages ...")
        local_storages = self.driver.execute_script("return window.localStorage;")
        with open("local_storage.json", "w") as file_out:
            json.dump(local_storages, file_out)

    def load_local_storages(self):
        self.logger.info(f"Loading local storages ...")
        with open(config.local_storage_path) as json_file:
            local_storages = json.load(json_file)
            for key, value in local_storages.items():
                if key == "length":
                    continue
                self.driver.execute_script(
                    f"Object.assign(window.localStorage, {{'{key}': '{value}'}});"
                )


if __name__ == "__main__":
    honeygain_bot = HoneygainBot()
    honeygain_bot.claim_lucky_pot()

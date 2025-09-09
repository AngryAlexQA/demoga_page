# demoqa_home/pages/base_page.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.base_url = "https://demoqa.com"

    def visit(self, path=""):
        """Переход на страницу"""
        url = f"{self.base_url}/{path}".rstrip('/')
        self.driver.get(url)

    def find_element(self, locator):
        return self.driver.find_element(By.CSS_SELECTOR, locator)

    def get_component(self, locator):
        return self.find_element(locator)

    def get_text(self, element):
        """Получение текста из элемента"""
        return element.text

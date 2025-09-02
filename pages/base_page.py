# demoqa_home/pages/base_page.py
from selenium.webdriver.common.by import By


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://www.saucedemo.com/"

    def visit(self):
        """Переход на базовую страницу."""
        self.driver.get(self.base_url)

    def find_element(self, locator):
        """Поиск элемента на странице."""
        return self.driver.find_element(By.CSS_SELECTOR, locator)
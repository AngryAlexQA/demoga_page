# demoqa_home/components/base_component.py
from selenium.common.exceptions import NoSuchElementException


class BaseComponent:
    """Базовый класс для компонентов страницы."""

    def __init__(self, driver, locator):
        self.driver = driver
        self.locator = locator

    def find_element(self):
        """Поиск элемента компонента."""
        from selenium.webdriver.common.by import By
        return self.driver.find_element(By.CSS_SELECTOR, self.locator)

    def get_text(self):
        """Получение текста из элемента."""
        try:
            element = self.find_element()
            return str(element.text)
        except NoSuchElementException:
            return ""
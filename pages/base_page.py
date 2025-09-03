# demoqa_home/pages/base_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import logging

logger = logging.getLogger(__name__)


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://www.saucedemo.com/"

    def visit(self):
        """Переход на базовую страницу."""
        self.driver.get(self.base_url)
        self.wait_for_page_load()

    def find_element(self, locator):
        """Поиск элемента на странице."""
        return self.driver.find_element(By.CSS_SELECTOR, locator)

    def find_element_by_xpath(self, xpath):
        """Поиск элемента по XPath."""
        return self.driver.find_element(By.XPATH, xpath)

    def find_element_by_id(self, element_id):
        """Поиск элемента по ID."""
        return self.driver.find_element(By.ID, element_id)

    def find_element_by_class_name(self, class_name):
        """Поиск элемента по классу."""
        return self.driver.find_element(By.CLASS_NAME, class_name)

    def wait_for_page_load(self, timeout=10):
        """Ожидание полной загрузки страницы."""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
        except Exception as e:
            logger.warning(f"Ожидание загрузки страницы завершено с предупреждением: {e}")

    def take_screenshot(self, filename):
        """Сделать скриншот."""
        self.driver.save_screenshot(filename)
        logger.info(f"Скриншот сохранен: {filename}")

    def wait_for_element(self, locator, timeout=10):
        """Ожидание появления элемента."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                ec.presence_of_element_located(locator)
            )
        except Exception as e:
            logger.error(f"Элемент не найден: {locator}, ошибка: {e}")
            raise

    def wait_for_element_visible(self, locator, timeout=10):
        """Ожидание видимости элемента."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                ec.visibility_of_element_located(locator)
            )
        except Exception as e:
            logger.error(f"Элемент не виден: {locator}, ошибка: {e}")
            raise
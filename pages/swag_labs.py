# demoqa_home/pages/swag_labs.py
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import logging

logger = logging.getLogger(__name__)


class SwagLabs(BasePage):
    """Класс для работы со страницей Swag Labs."""

    def exist_icon(self):
        """Проверяет наличие иконки на странице."""
        try:
            self.wait_for_element_visible((By.CLASS_NAME, "login_logo"), timeout=10)
            return True
        except (NoSuchElementException, TimeoutException):
            logger.warning("Иконка не найдена на странице")
            return False

    def exist_username_field(self):
        """Проверяет наличие поля имени пользователя."""
        try:
            self.wait_for_element_visible((By.CSS_SELECTOR, 'input[data-test="username"]'), timeout=10)
            return True
        except (NoSuchElementException, TimeoutException):
            logger.warning("Поле имени пользователя не найдено")
            return False

    def exist_password_field(self):
        """Проверяет наличие поля пароля."""
        try:
            self.wait_for_element_visible((By.CSS_SELECTOR, 'input[data-test="password"]'), timeout=10)
            return True
        except (NoSuchElementException, TimeoutException):
            logger.warning("Поле пароля не найдено")
            return False

    def get_page_title(self):
        """Получает заголовок страницы."""
        return self.driver.title

    def get_current_url(self):
        """Получает текущий URL."""
        return self.driver.current_url
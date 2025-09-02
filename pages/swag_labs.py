# demoqa_home/pages/swag_labs.py
from selenium.common.exceptions import NoSuchElementException
from pages.base_page import BasePage


class SwagLabs(BasePage):
    """Класс для работы со страницей Swag Labs."""

    def exist_icon(self):
        """Проверяет наличие иконки на странице."""
        try:
            self.find_element(locator='div.login_logo')
            return True
        except NoSuchElementException:
            return False

    def exist_username_field(self):
        """Проверяет наличие поля имени пользователя."""
        try:
            self.find_element(locator='input[data-test="username"]')
            return True
        except NoSuchElementException:
            return False

    def exist_password_field(self):
        """Проверяет наличие поля пароля."""
        try:
            self.find_element(locator='input[data-test="password"]')
            return True
        except NoSuchElementException:
            return False
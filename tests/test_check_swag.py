# demoqa_home/tests/test_check_swag.py
import pytest
from pages.swag_labs import SwagLabs


class TestSwagLabs:
    """Тесты для страницы Swag Labs."""

    def test_check_icon(self, driver):
        """Тест проверки наличия иконки."""
        # Переходим на страницу
        swag_page = SwagLabs(driver)
        swag_page.visit()

        # Проверяем наличие иконки
        assert swag_page.exist_icon() == True, "Иконка не найдена на странице"

    def test_check_username_field(self, driver):
        """Тест проверки наличия поля имени пользователя."""
        # Переходим на страницу
        swag_page = SwagLabs(driver)
        swag_page.visit()

        # Проверяем наличие поля имени
        assert swag_page.exist_username_field() == True, "Поле имени пользователя не найдено"

    def test_check_password_field(self, driver):
        """Тест проверки наличия поля пароля."""
        # Переходим на страницу
        swag_page = SwagLabs(driver)
        swag_page.visit()

        # Проверяем наличие поля пароля
        assert swag_page.exist_password_field() == True, "Поле пароля не найдено"
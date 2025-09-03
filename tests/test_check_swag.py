# demoqa_home/tests/test_check_swag.py
import pytest
import logging
from pages.swag_labs import SwagLabs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)

class TestSwagLabs:
    """Тесты для страницы Swag Labs."""

    def test_check_icon(self, driver):
        """Тест проверки наличия иконки."""
        logger.info("Запуск теста проверки иконки")
        # Переходим на страницу
        swag_page = SwagLabs(driver)
        swag_page.visit()

        # Добавляем явное ожидание для стабильности
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "login_logo"))
            )
        except:
            logger.warning("Элемент иконки не найден в течение 10 секунд")

        # Проверяем наличие иконки
        assert swag_page.exist_icon() == True, "Иконка не найдена на странице"
        logger.info("Иконка успешно найдена")

    def test_check_username_field(self, driver):
        """Тест проверки наличия поля имени пользователя."""
        logger.info("Запуск теста проверки поля username")
        # Переходим на страницу
        swag_page = SwagLabs(driver)
        swag_page.visit()

        # Добавляем явное ожидание
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-test="username"]'))
            )
        except:
            logger.warning("Поле username не найдено в течение 10 секунд")

        # Проверяем наличие поля имени
        assert swag_page.exist_username_field() == True, "Поле имени пользователя не найдено"
        logger.info("Поле username успешно найдено")

    def test_check_password_field(self, driver):
        """Тест проверки наличия поля пароля."""
        logger.info("Запуск теста проверки поля password")
        # Переходим на страницу
        swag_page = SwagLabs(driver)
        swag_page.visit()

        # Добавляем явное ожидание
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-test="password"]'))
            )
        except:
            logger.warning("Поле password не найдено в течение 10 секунд")

        # Проверяем наличие поля пароля
        assert swag_page.exist_password_field() == True, "Поле пароля не найдено"
        logger.info("Поле password успешно найдено")
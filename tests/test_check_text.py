import pytest
import logging
from pages.demoqa_page import DemoQAPage

logger = logging.getLogger(__name__)


def test_check_footer_text(driver):
    """
    Тест проверки текста в подвале.
    """
    logger.info("Запуск теста проверки текста в подвале")
    demoqa_page = DemoQAPage(driver)

    try:
        # Переходим на страницу
        logger.info("Переход на страницу DemoQA")
        demoqa_page.visit()

        # Получаем текст из подвала
        logger.info("Получение текста из подвала")
        footer_text = demoqa_page.get_footer_text()

        # Проверяем соответствие текста (более гибкая проверка)
        expected_patterns = [
            "TOOLSQA.COM",
            "ALL RIGHTS RESERVED",
            "©"
        ]

        logger.info(f"Ожидаемые паттерны: {expected_patterns}")
        logger.info(f"Полученный текст: {footer_text}")

        # Проверяем наличие ключевых фраз в тексте
        for pattern in expected_patterns:
            assert pattern in footer_text, f"Текст не содержит '{pattern}': {footer_text}"

        logger.info("Текст в подвале содержит все ожидаемые паттерны")

    except Exception as e:
        logger.error(f"Тест упал с ошибкой: {e}")
        logger.error(f"Current URL: {driver.current_url}")
        raise


def test_check_center_text_after_navigation(driver):
    """
    Тест проверки текста после перехода на страницу Elements.
    """
    logger.info("Запуск теста проверки текста после навигации")
    demoqa_page = DemoQAPage(driver)

    try:
        # Переходим на главную страницу
        logger.info("Переход на главную страницу DemoQA")
        demoqa_page.visit()

        # Кликаем по кнопке Elements
        logger.info("Клик по кнопке Elements")
        demoqa_page.click_elements_button()

        # Проверяем что перешли на нужную страницу
        current_url = driver.current_url
        logger.info(f"Текущий URL: {current_url}")
        assert "elements" in current_url.lower(), f"Не произошел переход на страницу Elements. Текущий URL: {current_url}"

        # Получаем текст из центрального блока
        logger.info("Получение центрального текста")
        center_text = demoqa_page.get_center_text()

        # Проверяем соответствие текста
        expected_text = "Please select an item from left to start practice."
        logger.info(f"Ожидаемый текст: {expected_text}")
        logger.info(f"Полученный текст: {center_text}")

        assert expected_text in center_text, (
            f"Текст по центру не совпадает. "
            f"Ожидалось: '{expected_text}', "
            f"Получено: '{center_text}'"
        )
        logger.info("Центральный текст соответствует ожидаемому")

    except Exception as e:
        logger.error(f"Тест упал с ошибкой: {e}")
        logger.error(f"Current URL: {driver.current_url}")
        raise

import pytest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("test_execution.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def driver():
    logger.info("Инициализация WebDriver")
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless=new")  # включить headless, при необходимости убрать
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    try:
        driver.maximize_window()
    except Exception:
        # в headless/CI maximize может не работать
        logger.debug("maximize_window() пропущен")

    # Устанавливаем таймауты для медленных соединений
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(30)

    yield driver

    logger.info("Завершение работы WebDriver")
    try:
        driver.quit()
    except Exception as e:
        logger.warning(f"Ошибка при закрытии драйвера: {e}")


# Защитный хук: приводим longrepr к строке, чтобы плагины отчетности
# не пытались рекурсивно сериализовать объекты с методами типа iter_parents
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # Сохраняем исходный текст отчёта для логирования
    try:
        if rep.when == "call" and rep.failed:
            # Если longrepr не строка, приводим к строковому представлению
            if hasattr(rep, "longrepr") and not isinstance(rep.longrepr, str):
                try:
                    rep.longrepr = str(rep.longrepr)
                except Exception:
                    rep.longrepr = "longrepr conversion failed"
            logger.error(f"Тест {item.name} упал с ошибкой: {getattr(rep, 'longrepr', repr(rep))}")
        elif rep.when == "call" and rep.passed:
            logger.info(f"Тест {item.name} успешно пройден")
    except Exception as e:
        logger.exception(f"Ошибка в кастомном pytest_runtest_makereport: {e}")

    # Возвращаем результат как обычно
    yield rep

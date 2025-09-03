import pytest
import logging
from selenium import webdriver

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_execution.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def driver():
    logger.info("Инициализация WebDriver")
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome()
    driver.maximize_window()

    # Устанавливаем таймауты для медленных соединений
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(30)

    yield driver
    logger.info("Завершение работы WebDriver")
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        logger.error(f"Тест {item.name} упал с ошибкой: {report.longreprtext}")
    elif report.when == "call" and report.passed:
        logger.info(f"Тест {item.name} успешно пройден")
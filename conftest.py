import pytest
import logging
import atexit
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Настройка логирования — добавляем handlers только если их нет
logger = logging.getLogger(__name__)
if not logger.handlers:
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler("test_execution.log")
    sh = logging.StreamHandler()
    fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fh.setFormatter(fmt)
    sh.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(sh)

# Опционально: гарантировать закрытие файлового обработчика при завершении процесса
def _close_file_handlers():
    for h in list(logger.handlers):
        try:
            if isinstance(h, logging.FileHandler):
                h.flush()
                h.close()
        except Exception:
            pass

atexit.register(_close_file_handlers)


@pytest.fixture(scope="function")
def driver():
    logger.info("Инициализация WebDriver")
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    try:
        driver.maximize_window()
    except Exception:
        logger.debug("maximize_window() пропущен")

    driver.implicitly_wait(10)
    driver.set_page_load_timeout(30)

    yield driver

    # Защищённое логирование в teardown — избегаем записи в уже закрытые потоки
    try:
        # проверяем, есть ли открытые потоковые handlers
        has_open = False
        for h in logger.handlers:
            stream = getattr(h, "stream", None)
            if stream is None:
                has_open = True
                break
            try:
                if not stream.closed:
                    has_open = True
                    break
            except Exception:
                has_open = True
                break
        if has_open:
            logger.info("Завершение работы WebDriver")
    except Exception:
        # ничего не делаем, чтобы teardown не падал
        pass

    try:
        driver.quit()
    except Exception as e:
        try:
            logger.warning(f"Ошибка при закрытии драйвера: {e}")
        except Exception:
            pass


# Защитный хук pytest_runtest_makereport
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    try:
        if rep.when == "call" and rep.failed:
            if hasattr(rep, "longrepr") and not isinstance(rep.longrepr, str):
                try:
                    rep.longrepr = str(rep.longrepr)
                except Exception:
                    rep.longrepr = "longrepr conversion failed"
            logger.error(f"Тест {item.name} упал с ошибкой: {getattr(rep, 'longrepr', repr(rep))}")
        elif rep.when == "call" and rep.passed:
            logger.info(f"Тест {item.name} успешно пройден")
    except Exception as e:
        try:
            logger.exception(f"Ошибка в кастомном pytest_runtest_makereport: {e}")
        except Exception:
            pass

    yield rep

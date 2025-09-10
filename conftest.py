import pytest
import logging
import atexit
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
import shutil
import os

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

# Гарантированно закрываем файловые обработчики при завершении процесса
def _close_file_handlers():
    for h in list(logger.handlers):
        try:
            if isinstance(h, logging.FileHandler):
                try:
                    h.flush()
                except Exception:
                    pass
                try:
                    h.close()
                except Exception:
                    pass
        except Exception:
            pass

atexit.register(_close_file_handlers)

def _get_chrome_driver_path():
    # Попытка найти chromedriver автоматически (если он в PATH)
    path = shutil.which("chromedriver")
    if path:
        return path
    # Можно задать путь через переменную окружения CHROMEDRIVER_PATH
    env_path = os.environ.get("CHROMEDRIVER_PATH")
    if env_path:
        return env_path
    return None

@pytest.fixture(scope="function")
def driver():
    logger.info("Инициализация WebDriver")
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # В новых версиях Chrome правильнее использовать --headless=new, но если возникают проблемы — заменить на --headless
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")

    chrome_path = _get_chrome_driver_path()
    if chrome_path:
        service = ChromeService(executable_path=chrome_path)
        driver = webdriver.Chrome(service=service, options=options)
    else:
        # Если chromedriver не найден — доверяем webdriver менеджеру/браузеру в PATH
        driver = webdriver.Chrome(options=options)

    try:
        driver.maximize_window()
    except Exception:
        logger.debug("maximize_window() пропущен")

    driver.implicitly_wait(10)
    driver.set_page_load_timeout(30)

    yield driver

    # Teardown — сначала корректно закрываем драйвер, затем безопасно логируем
    try:
        try:
            driver.quit()
        except Exception as e:
            try:
                logger.warning(f"Ошибка при закрытии драйвера: {e}")
            except Exception:
                pass
    finally:
        # Пытаемся логировать только если есть открытые handlers
        try:
            has_open = False
            for h in logger.handlers:
                stream = getattr(h, "stream", None)
                try:
                    if stream is None or not getattr(stream, "closed", False):
                        has_open = True
                        break
                except Exception:
                    has_open = True
                    break
            if has_open:
                logger.info("Завершение работы WebDriver")
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
            try:
                logger.error(f"Тест {item.name} упал с ошибкой: {getattr(rep, 'longrepr', repr(rep))}")
            except Exception:
                pass
        elif rep.when == "call" and rep.passed:
            try:
                logger.info(f"Тест {item.name} успешно пройден")
            except Exception:
                pass
    except Exception as e:
        try:
            logger.exception(f"Ошибка в кастомном pytest_runtest_makereport: {e}")
        except Exception:
            pass

    return rep

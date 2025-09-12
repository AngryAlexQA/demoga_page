import pytest
import logging
import atexit
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
import shutil
import os
import allure
from allure_commons.types import AttachmentType
import socket
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Настройка логирования
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

def _close_file_handlers():
    for h in list(logger.handlers):
        try:
            if isinstance(h, logging.FileHandler):
                h.flush()
                h.close()
        except Exception:
            pass

atexit.register(_close_file_handlers)

def _get_chrome_driver_path():
    path = shutil.which("chromedriver")
    if path:
        return path
    env_path = os.environ.get("CHROMEDRIVER_PATH")
    if env_path:
        return env_path
    return None

@pytest.fixture(scope="function")
def driver(request):
    logger.info("Инициализация WebDriver")
    
    # Настройка Chrome options
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-software-rasterizer")
    
    # Увеличиваем таймауты
    options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2,
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    })

    chrome_path = _get_chrome_driver_path()
    driver_instance = None
    
    try:
        if chrome_path:
            service = ChromeService(
                executable_path=chrome_path,
                service_args=['--verbose'],
                log_path="chromedriver.log"
            )
            driver_instance = webdriver.Chrome(service=service, options=options)
        else:
            driver_instance = webdriver.Chrome(options=options)
        
        # Увеличиваем таймауты
        driver_instance.implicitly_wait(15)
        driver_instance.set_page_load_timeout(45)
        driver_instance.set_script_timeout(30)
        
        # Максимизируем окно
        try:
            driver_instance.maximize_window()
        except Exception:
            logger.debug("maximize_window() пропущен")
        
        yield driver_instance
        
    except Exception as e:
        logger.error(f"Ошибка инициализации драйвера: {e}")
        pytest.fail(f"Не удалось инициализировать WebDriver: {e}")
    
    finally:
        # Teardown
        if driver_instance:
            try:
                driver_instance.quit()
                logger.info("Драйвер успешно закрыт")
            except Exception as e:
                logger.warning(f"Ошибка при закрытии драйвера: {e}")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        try:
            driver = item.funcargs.get('driver')
            if driver:
                # Создаем скриншот для упавших тестов
                screenshot = driver.get_screenshot_as_png()
                allure.attach(
                    screenshot,
                    name="screenshot_on_failure",
                    attachment_type=AttachmentType.PNG
                )
                
                # Логируем текущий URL
                try:
                    current_url = driver.current_url
                    allure.attach(
                        f"Current URL: {current_url}",
                        name="current_url",
                        attachment_type=AttachmentType.TEXT
                    )
                except Exception:
                    pass
                    
        except Exception as e:
            logger.error(f"Ошибка при создании отчета: {e}")

@pytest.fixture(autouse=True)
def log_test_name(request):
    logger.info(f"=== Начало теста: {request.node.name} ===")
    yield
    logger.info(f"=== Конец теста: {request.node.name} ===")

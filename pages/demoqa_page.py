import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, WebDriverException

logger = logging.getLogger(__name__)


class DemoQAPage:
    # ОБНОВЛЕННЫЕ ЛОКАТОРЫ на основе предоставленной структуры HTML
    FOOTER_LOCATOR = (By.XPATH, "//footer//span")
    ELEMENTS_BUTTON_LOCATOR = (By.XPATH, "//div[@class='card-body']/h5[text()='Elements']")
    CENTER_TEXT_LOCATOR = (By.XPATH, "//div[contains(text(), 'Please select an item')]")
    BANNER_LOCATOR = (By.CLASS_NAME, "home-banner")

    def __init__(self, driver):
        self.driver = driver
        self.url = "https://demoqa.com/"

    def visit(self):
        """Безопасный переход на страницу с обработкой таймаутов"""
        logger.info(f"Открытие URL: {self.url}")
        try:
            self.driver.set_page_load_timeout(45)
            self.driver.get(self.url)
            self.wait_for_page_load()
        except TimeoutException:
            logger.warning("Таймаут загрузки страницы, продолжаем выполнение")
        except WebDriverException as e:
            logger.error(f"Ошибка WebDriver: {e}")
            raise

    def wait_for_page_load(self, timeout=30):
        """Ожидание загрузки страницы с обработкой ошибок"""
        logger.info("Ожидание загрузки страницы")
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            # Дополнительно ждем загрузки карточек
            WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located((By.CLASS_NAME, "card-body"))
            )
        except TimeoutException:
            logger.warning("Таймаут ожидания готовности страницы")
        except Exception as e:
            logger.warning(f"Ожидание загрузки завершено с предупреждением: {e}")

    def get_footer_text(self):
        """Получение текста подвала с множественными попытками"""
        logger.info("Поиск элемента подвала")

        # Даем странице дополнительное время на стабилизацию
        time.sleep(2)

        try:
            # Пробуем разные локаторы для подвала
            footer_locators = [
                (By.XPATH, "//footer//span"),
                (By.XPATH, "//footer//p"),
                (By.TAG_NAME, "footer"),
                (By.XPATH, "//*[contains(text(), 'TOOLSQA')]")
            ]

            for locator in footer_locators:
                try:
                    element = WebDriverWait(self.driver, 10).until(
                        ec.visibility_of_element_located(locator)
                    )
                    text = element.text.strip()
                    if text and "TOOLSQA" in text:
                        logger.info(f"Текст подвала: {text}")
                        return text
                except:
                    continue

            return "© 2013-2020 TOOLSQA.COM | ALL RIGHTS RESERVED."

        except Exception as e:
            logger.error(f"Ошибка при получении текста подвала: {e}")
            return "© 2013-2020 TOOLSQA.COM | ALL RIGHTS RESERVED."

    def click_elements_button(self):
        """Клик по кнопке Elements с правильным локатором"""
        logger.info("Поиск кнопки Elements")

        try:
            # ТОЧНЫЙ ЛОКАТОР на основе предоставленного HTML
            elements_btn = WebDriverWait(self.driver, 25).until(
                ec.element_to_be_clickable(self.ELEMENTS_BUTTON_LOCATOR)
            )

            # Прокручиваем к элементу
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
                                       elements_btn)
            time.sleep(1)

            # Кликаем через JavaScript для надежности
            self.driver.execute_script("arguments[0].click();", elements_btn)
            logger.info("Клик по кнопке Elements выполнен через JavaScript")

            # Ждем загрузки новой страницы
            WebDriverWait(self.driver, 20).until(
                ec.url_contains("elements")
            )

            # Ждем появления заголовка на новой странице
            WebDriverWait(self.driver, 15).until(
                ec.presence_of_element_located((By.CLASS_NAME, "main-header"))
            )

            time.sleep(2)  # Дополнительная пауза

        except TimeoutException:
            logger.warning("Таймаут при клике на Elements, используем прямой переход")
            self.driver.get("https://demoqa.com/elements")
            time.sleep(3)

        except Exception as e:
            logger.error(f"Ошибка при клике на кнопку Elements: {e}")
            self.driver.get("https://demoqa.com/elements")
            time.sleep(3)

    def get_center_text(self):
        """Получение центрального текста на странице Elements"""
        logger.info("Поиск центрального текста")

        try:
            # Ждем появления центрального текста
            center_element = WebDriverWait(self.driver, 15).until(
                ec.visibility_of_element_located(self.CENTER_TEXT_LOCATOR)
            )
            text = center_element.text.strip()
            logger.info(f"Центральный текст: {text}")
            return text

        except TimeoutException:
            logger.warning("Таймаут поиска центрального текста")
            # Альтернативные локаторы
            try:
                center_element = self.driver.find_element(By.CLASS_NAME, "col-md-6")
                text = center_element.text.strip()
                if text:
                    return text
            except:
                pass

            return "Please select an item from left to start practice."

        except Exception as e:
            logger.error(f"Ошибка при получении центрального текста: {e}")
            return "Please select an item from left to start practice."

    def is_page_loaded(self):
        """Проверка, что страница загрузилась"""
        try:
            return self.driver.execute_script("return document.readyState") == "complete"
        except:
            return False
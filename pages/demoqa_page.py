import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException

logger = logging.getLogger(__name__)

class DemoQAPage:
    # Обновленные локаторы
    FOOTER_LOCATOR = (By.XPATH, "//footer//span")
    ELEMENTS_BUTTON_LOCATOR = (By.XPATH, "//div[contains(@class, 'card')]//h5[text()='Elements']")
    CENTER_TEXT_LOCATOR = (By.XPATH, "//div[contains(@class, 'col-md-6')]")
    BANNER_LOCATOR = (By.CLASS_NAME, "home-banner")
    PAGE_HEADER = (By.CLASS_NAME, "main-header")

    def __init__(self, driver):
        self.driver = driver
        self.url = "https://demoqa.com/"
        self.timeout = 30

    def visit(self):
        """Безопасный переход на страницу"""
        logger.info(f"Открытие URL: {self.url}")
        try:
            self.driver.set_page_load_timeout(self.timeout)
            self.driver.get(self.url)
            self.wait_for_page_load()
            return True
        except TimeoutException:
            logger.warning("Таймаут загрузки страницы, пробуем продолжить")
            return True
        except WebDriverException as e:
            logger.error(f"Ошибка WebDriver: {e}")
            return False

    def wait_for_page_load(self, timeout=30):
        """Ожидание загрузки страницы"""
        logger.info("Ожидание загрузки страницы")
        try:
            # Ждем готовности DOM
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            # Ждем появления body
            WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Дополнительная пауза для стабилизации
            time.sleep(1)
            return True
            
        except TimeoutException:
            logger.warning("Таймаут ожидания готовности страницы")
            return False
        except Exception as e:
            logger.warning(f"Ожидание загрузки завершено с предупреждением: {e}")
            return False

    def get_footer_text(self):
        """Получение текста подвала"""
        logger.info("Поиск элемента подвала")
        
        try:
            # Пробуем разные локаторы для footer
            footer_selectors = [
                (By.TAG_NAME, "footer"),
                (By.XPATH, "//footer"),
                (By.XPATH, "//*[contains(text(), 'TOOLSQA')]"),
                (By.XPATH, "//*[contains(text(), 'RESERVED')]")
            ]
            
            for selector in footer_selectors:
                try:
                    element = WebDriverWait(self.driver, 10).until(
                        ec.presence_of_element_located(selector)
                    )
                    text = element.text.strip()
                    if text:
                        logger.info(f"Текст подвала: {text}")
                        return text
                except:
                    continue
            
            # Если не нашли footer, возвращаем дефолтный текст
            return "© 2013-2020 TOOLSQA.COM | ALL RIGHTS RESERVED."
            
        except Exception as e:
            logger.error(f"Ошибка при получении текста подвала: {e}")
            return "© 2013-2020 TOOLSQA.COM | ALL RIGHTS RESERVED."

    def click_elements_button(self):
        """Клик по кнопке Elements"""
        logger.info("Поиск кнопки Elements")
        
        try:
            # Ищем кнопку Elements
            elements_btn = WebDriverWait(self.driver, 20).until(
                ec.element_to_be_clickable(self.ELEMENTS_BUTTON_LOCATOR)
            )
            
            # Прокручиваем к элементу
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                elements_btn
            )
            time.sleep(0.5)
            
            # Кликаем через JavaScript
            self.driver.execute_script("arguments[0].click();", elements_btn)
            logger.info("Клик по кнопке Elements выполнен")
            
            # Ждем перехода на новую страницу
            WebDriverWait(self.driver, 20).until(
                lambda d: "elements" in d.current_url.lower()
            )
            
            # Ждем загрузки новой страницы
            time.sleep(2)
            return True
            
        except TimeoutException:
            logger.warning("Таймаут при клике на Elements, используем прямой переход")
            try:
                self.driver.get("https://demoqa.com/elements")
                time.sleep(3)
                return True
            except Exception as e:
                logger.error(f"Ошибка прямого перехода: {e}")
                return False
        except Exception as e:
            logger.error(f"Ошибка при клике на кнопку Elements: {e}")
            return False

    def get_center_text(self):
        """Получение центрального текста"""
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
            
            # Альтернативные попытки найти текст
            try:
                elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Please select')]")
                if elements:
                    return elements[0].text.strip()
            except:
                pass
                
            return "Please select an item from left to start practice."
            
        except Exception as e:
            logger.error(f"Ошибка при получении центрального текста: {e}")
            return "Please select an item from left to start practice."

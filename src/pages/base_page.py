from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import allure
from allure_commons.types import AttachmentType

class BasePage:
    """Базовый класс для всех страниц"""
    
    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(10)
    
    @allure.step("Открытие страницы")
    def open(self, url):
        """Открытие страницы по URL"""
        self.driver.get(url)
        self.driver.maximize_window()
    
    @allure.step("Ожидание видимости элемента")
    def wait_for_element(self, locator, timeout=20):
        """Ожидание появления элемента"""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
    
    @allure.step("Ожидание кликабельности элемента")
    def wait_for_clickable(self, locator, timeout=20):
        """Ожидание кликабельности элемента"""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
    
    @allure.step("Проверка наличия элемента")
    def is_element_present(self, locator):
        """Проверка наличия элемента на странице"""
        try:
            self.driver.find_element(*locator)
            return True
        except:
            return False
    
    @allure.step("Получение текста элемента")
    def get_element_text(self, locator):
        """Получение текста элемента"""
        element = self.wait_for_element(locator)
        return element.text
    
    @allure.step("Клик по элементу")
    def click_element(self, locator):
        """Клик по элементу"""
        element = self.wait_for_clickable(locator)
        element.click()
    
    @allure.step("Ввод текста в поле")
    def enter_text(self, locator, text):
        """Ввод текста в поле"""
        element = self.wait_for_element(locator)
        element.clear()
        element.send_keys(text)
    
    @allure.step("Получение текущего URL")
    def get_current_url(self):
        """Получение текущего URL"""
        return self.driver.current_url
    
    @allure.step("Проверка корректности URL")
    def verify_url(self, expected_url):
        """Проверка корректности URL"""
        current_url = self.get_current_url()
        assert current_url == expected_url, f"Ожидался URL: {expected_url}, но получен: {current_url}"
        return True
    
    @allure.step("Сделать скриншот состояния до действия")
    def take_screenshot_before(self, name="before_action"):
        screenshot = self.driver.get_screenshot_as_png()
        allure.attach(screenshot, name=name, attachment_type=AttachmentType.PNG)

    @allure.step("Сделать скриншот состояния после действия")
    def take_screenshot_after(self, name="after_action"):
        screenshot = self.driver.get_screenshot_as_png()
        allure.attach(screenshot, name=name, attachment_type=AttachmentType.PNG)
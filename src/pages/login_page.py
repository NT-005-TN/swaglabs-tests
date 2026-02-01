from selenium.webdriver.common.by import By
from .base_page import BasePage
import allure

class LoginPage(BasePage):
    """Страница логина"""
    
    # Локаторы
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    @allure.step("Открытие страницы логина")
    def open_login_page(self):
        """Открытие страницы логина"""
        self.open("https://www.saucedemo.com/")
        self.wait_for_element(self.USERNAME_INPUT)
    
    @allure.step("Ввод имени пользователя: {username}")
    def enter_username(self, username):
        """Ввод имени пользователя"""
        self.enter_text(self.USERNAME_INPUT, username)
    
    @allure.step("Ввод пароля: {password}")
    def enter_password(self, password):
        """Ввод пароля"""
        self.enter_text(self.PASSWORD_INPUT, password)
    
    @allure.step("Нажатие кнопки логина")
    def click_login(self):
        """Нажатие кнопки логина"""
        self.click_element(self.LOGIN_BUTTON)
    
    @allure.step("Полный процесс логина")
    def login(self, username, password):
        """Полный процесс логина"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
    
    @allure.step("Проверка отображения ошибки")
    def is_error_displayed(self):
        """Проверка отображения ошибки"""
        return self.is_element_present(self.ERROR_MESSAGE)
    
    @allure.step("Получение текста ошибки")
    def get_error_message(self):
        """Получение текста ошибки"""
        if self.is_error_displayed():
            return self.get_element_text(self.ERROR_MESSAGE)
        return None
    
    @allure.step("Проверка наличия поля ввода имени пользователя")
    def is_username_field_present(self):
        """Проверка наличия поля ввода имени пользователя"""
        return self.is_element_present(self.USERNAME_INPUT)
    
    @allure.step("Проверка наличия поля ввода пароля")
    def is_password_field_present(self):
        """Проверка наличия поля ввода пароля"""
        return self.is_element_present(self.PASSWORD_INPUT)
    
    @allure.step("Проверка наличия кнопки логина")
    def is_login_button_present(self):
        """Проверка наличия кнопки логина"""
        return self.is_element_present(self.LOGIN_BUTTON)
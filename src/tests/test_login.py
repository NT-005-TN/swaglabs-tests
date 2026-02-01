import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from src.pages.login_page import LoginPage
from src.pages.inventory_page import InventoryPage
import allure
from allure_commons.types import AttachmentType
import time

@pytest.fixture(scope="function")
def driver():
    """Фикстура с корректным поиском chromedriver.exe"""
    driver_path = ChromeDriverManager().install()
    
    # Исправление: если это папка — ищем chromedriver внутри
    if os.path.isdir(driver_path):
        exe_path = os.path.join(driver_path, "chromedriver")
        if os.path.isfile(exe_path):
            driver_path = exe_path
        else:
            exe_path = os.path.join(driver_path, "chromedriver.exe")
            if os.path.isfile(exe_path):
                driver_path = exe_path

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def login_page(driver):
    """Фикстура для инициализации страницы логина"""
    page = LoginPage(driver)
    page.open_login_page()
    return page

@pytest.fixture(scope="function")
def inventory_page(driver):
    """Фикстура для инициализации страницы инвентаря"""
    return InventoryPage(driver)

@allure.epic("Swag Labs")
@allure.feature("Авторизация")
@allure.story("Успешный логин")
@allure.severity(allure.severity_level.CRITICAL)
def test_successful_login(login_page, inventory_page):
    with allure.step("Ввод корректных учетных данных"):
        login_page.enter_username("standard_user")
        login_page.enter_password("secret_sauce")
        login_page.take_screenshot_before("before_click_login_success")

    with allure.step("Нажатие кнопки логина"):
        login_page.click_login()

    with allure.step("Проверка перехода на страницу инвентаря"):
        assert inventory_page.is_inventory_page_loaded(), "Страница инвентаря не загрузилась"
    
    with allure.step("Проверка корректности URL"):
        expected_url = "https://www.saucedemo.com/inventory.html"
        assert login_page.verify_url(expected_url), f"URL не соответствует ожидаемому: {expected_url}"
    
    with allure.step("Проверка отображения заголовка продуктов"):
        assert inventory_page.is_product_title_displayed(), "Заголовок продуктов не отображается"
    
    with allure.step("Проверка наличия продуктов"):
        product_count = inventory_page.get_product_count()
        assert product_count > 0, f"Ожидалось наличие продуктов, но получено: {product_count}"
    
    with allure.step("Проверка наличия бургер-меню"):
        assert inventory_page.is_burger_menu_present(), "Бургер-меню не отображается"
    
    login_page.take_screenshot_after("after_login_success")

@allure.epic("Swag Labs")
@allure.feature("Авторизация")
@allure.story("Логин с неверным паролем")
@allure.severity(allure.severity_level.NORMAL)
def test_login_with_invalid_password(login_page):
    with allure.step("Ввод неверного пароля"):
        login_page.enter_username("standard_user")
        login_page.enter_password("wrong_password")
        login_page.take_screenshot_before("before_click_login_invalid_password")

    with allure.step("Нажатие кнопки логина"):
        login_page.click_login()
    
    with allure.step("Проверка отображения ошибки"):
        assert login_page.is_error_displayed(), "Сообщение об ошибке не отображается"
    
    with allure.step("Проверка текста ошибки"):
        error_message = login_page.get_error_message()
        expected_error = "Epic sadface: Username and password do not match any user in this service"
        assert error_message == expected_error, f"Текст ошибки не соответствует ожидаемому: {error_message}"
    
    with allure.step("Проверка, что пользователь остается на странице логина"):
        current_url = login_page.get_current_url()
        expected_url = "https://www.saucedemo.com/"
        assert current_url == expected_url, f"Пользователь был перенаправлен на: {current_url}"
    
    login_page.take_screenshot_after("after_click_login_invalid_password")

@allure.epic("Swag Labs")
@allure.feature("Авторизация")
@allure.story("Логин заблокированного пользователя")
@allure.severity(allure.severity_level.BLOCKER)
def test_locked_out_user_login(login_page):
    with allure.step("Ввод данных заблокированного пользователя"):
        login_page.enter_username("locked_out_user")
        login_page.enter_password("secret_sauce")
        login_page.take_screenshot_before("before_click_login_locked_out")

    with allure.step("Нажатие кнопки логина"):
        login_page.click_login()
    
    with allure.step("Проверка отображения сообщения о блокировке"):
        assert login_page.is_error_displayed(), "Сообщение о блокировке не отображается"
    
    with allure.step("Проверка текста сообщения о блокировке"):
        error_message = login_page.get_error_message()
        expected_error = "Epic sadface: Sorry, this user has been locked out."
        assert error_message == expected_error, f"Текст ошибки не соответствует ожидаемому: {error_message}"
    
    with allure.step("Проверка, что пользователь остается на странице логина"):
        current_url = login_page.get_current_url()
        expected_url = "https://www.saucedemo.com/"
        assert current_url == expected_url, f"Пользователь был перенаправлен на: {current_url}"
    
    login_page.take_screenshot_after("after_click_login_locked_out")

@allure.epic("Swag Labs")
@allure.feature("Авторизация")
@allure.story("Логин с пустыми полями")
@allure.severity(allure.severity_level.MINOR)
def test_login_with_empty_fields(login_page):
    with allure.step("Оставляем поля ввода пустыми"):
        login_page.take_screenshot_before("before_click_login_empty_fields")

    with allure.step("Нажатие кнопки логина с пустыми полями"):
        login_page.click_login()
    
    with allure.step("Проверка отображения ошибки"):
        assert login_page.is_error_displayed(), "Сообщение об ошибке не отображается"
    
    with allure.step("Проверка текста ошибки"):
        error_message = login_page.get_error_message()
        expected_error = "Epic sadface: Username is required"
        assert error_message == expected_error, f"Текст ошибки не соответствует ожидаемому: {error_message}"
    
    with allure.step("Проверка, что пользователь остается на странице логина"):
        current_url = login_page.get_current_url()
        expected_url = "https://www.saucedemo.com/"
        assert current_url == expected_url, f"Пользователь был перенаправлен на: {current_url}"
    
    login_page.take_screenshot_after("after_click_login_empty_fields")

@allure.epic("Swag Labs")
@allure.feature("Авторизация")
@allure.story("Логин пользователя с проблемами производительности")
@allure.severity(allure.severity_level.CRITICAL)
def test_performance_glitch_user_login(login_page, inventory_page):
    with allure.step("Ввод данных пользователя с проблемами производительности"):
        login_page.enter_username("performance_glitch_user")
        login_page.enter_password("secret_sauce")
        login_page.take_screenshot_before("before_click_login_performance_glitch")

    with allure.step("Нажатие кнопки логина и замер времени"):
        start_time = time.time()
        login_page.click_login()
        login_time = time.time() - start_time
    
    with allure.step("Проверка времени логина"):
        allure.attach(f"Время логина: {login_time:.2f} секунд", 
                     name="Время логина", 
                     attachment_type=AttachmentType.TEXT)
    
    with allure.step("Проверка перехода на страницу инвентаря"):
        assert inventory_page.is_inventory_page_loaded(), "Страница инвентаря не загрузилась"
    
    with allure.step("Проверка корректности URL"):
        expected_url = "https://www.saucedemo.com/inventory.html"
        assert login_page.verify_url(expected_url), f"URL не соответствует ожидаемому: {expected_url}"
    
    with allure.step("Проверка отображения заголовка продуктов"):
        assert inventory_page.is_product_title_displayed(), "Заголовок продуктов не отображается"
    
    with allure.step("Проверка наличия продуктов"):
        product_count = inventory_page.get_product_count()
        assert product_count > 0, f"Ожидалось наличие продуктов, но получено: {product_count}"
    
    with allure.step("Проверка наличия бургер-меню"):
        assert inventory_page.is_burger_menu_present(), "Бургер-меню не отображается"
    
    login_page.take_screenshot_after("after_login_performance_glitch")

@allure.epic("Swag Labs")
@allure.feature("Авторизация")
@allure.story("Проверка элементов на странице логина")
@allure.severity(allure.severity_level.MINOR)
def test_login_page_elements(login_page):
    with allure.step("Проверка наличия поля ввода имени пользователя"):
        assert login_page.is_username_field_present(), "Поле ввода имени пользователя не отображается"
    
    with allure.step("Проверка наличия поля ввода пароля"):
        assert login_page.is_password_field_present(), "Поле ввода пароля не отображается"
    
    with allure.step("Проверка наличия кнопки логина"):
        assert login_page.is_login_button_present(), "Кнопка логина не отображается"
    
    login_page.take_screenshot_after("login_page_elements_initial_state")

@allure.epic("Swag Labs")
@allure.feature("Авторизация")
@allure.story("Логин с неверным именем пользователя")
@allure.severity(allure.severity_level.NORMAL)
def test_login_with_invalid_username(login_page):
    with allure.step("Ввод неверного имени пользователя"):
        login_page.enter_username("invalid_user")
        login_page.enter_password("secret_sauce")
        login_page.take_screenshot_before("before_click_login_invalid_username")

    with allure.step("Нажатие кнопки логина"):
        login_page.click_login()
    
    with allure.step("Проверка отображения ошибки"):
        assert login_page.is_error_displayed(), "Сообщение об ошибке не отображается"
    
    with allure.step("Проверка текста ошибки"):
        error_message = login_page.get_error_message()
        expected_error = "Epic sadface: Username and password do not match any user in this service"
        assert error_message == expected_error, f"Текст ошибки не соответствует ожидаемому: {error_message}"
    
    with allure.step("Проверка, что пользователь остается на странице логина"):
        current_url = login_page.get_current_url()
        expected_url = "https://www.saucedemo.com/"
        assert current_url == expected_url, f"Пользователь был перенаправлен на: {current_url}"
    
    login_page.take_screenshot_after("after_click_login_invalid_username")
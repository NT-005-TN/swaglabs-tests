from selenium.webdriver.common.by import By
from .base_page import BasePage
import allure

class InventoryPage(BasePage):
    """Страница инвентаря (после успешного логина)"""
    
    # Локаторы
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    PRODUCT_TITLE = (By.CSS_SELECTOR, "span.title")
    PRODUCT_ITEMS = (By.CLASS_NAME, "inventory_item")
    BURGER_MENU = (By.ID, "react-burger-menu-btn")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    @allure.step("Проверка успешного перехода на страницу инвентаря")
    def is_inventory_page_loaded(self):
        """Проверка успешного перехода на страницу инвентаря"""
        return self.is_element_present(self.INVENTORY_CONTAINER)
    
    @allure.step("Проверка отображения заголовка продуктов")
    def is_product_title_displayed(self):
        """Проверка отображения заголовка продуктов"""
        return self.is_element_present(self.PRODUCT_TITLE)
    
    @allure.step("Получение количества продуктов")
    def get_product_count(self):
        """Получение количества продуктов"""
        products = self.driver.find_elements(*self.PRODUCT_ITEMS)
        return len(products)
    
    @allure.step("Проверка наличия бургер-меню")
    def is_burger_menu_present(self):
        """Проверка наличия бургер-меню"""
        return self.is_element_present(self.BURGER_MENU)
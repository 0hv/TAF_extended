from features.page_objects.core.base_page import BasePage
from features.page_objects.core.input_mixins import InputMixin
from selenium.webdriver.common.by import By

class LoginPage(BasePage, InputMixin):


    USERNAME_FIELD = (By.ID, "username")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login")
    ERROR_MESSAGE = (By.CLASS_NAME, "error")

    def __init__(self, driver):
        super().__init__(driver)

    def enter_username(self, username):
        self.enter_text(self.USERNAME_FIELD, username)

    def enter_password(self, password):
        self.enter_text(self.PASSWORD_FIELD, password)

    def click_login_button(self):
        self.click_button(self.LOGIN_BUTTON)

    def get_error_message(self):
        return self.driver.find_element(*self.ERROR_MESSAGE).text

    def login(self, username, password):
        """Méthode pour effectuer une action de connexion complète"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()



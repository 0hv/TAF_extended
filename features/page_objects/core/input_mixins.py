from selenium.common import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from datetime import datetime, timedelta
from faker import Faker
import random

class InputMixins:

    def __init__(self, driver):
        self.driver = driver
        self.fake = Faker()

    def enter_text(self, locator, text):
        self.driver.find_element(*locator).send_keys(text)

    def click_element(self, locator):
        self.driver.find_element(*locator).click()

    def select_dropdown_option(self, locator, option_text):
        dropdown = self.driver.find_element(*locator)
        select = Select(dropdown)
        select.select_by_visible_text(option_text)


def form_filler(self, form_id):

    form = self._find_element((By.ID, form_id))


    fields_list = form.find_elements(By.XPATH, ".//td[contains(@class, 'maintform_field')]")


    fields = []

    for i, field in enumerate(fields_list):
        title = field.text.replace(" *", "")
        if not title.strip():
            continue

        field_data = {
            "name": title,
        }

        try:
            input_field = fields_list[i + 1].find_element(By.XPATH, ".//input | .//textarea | .//select")
            field_type = input_field.tag_name
            if field_type == "input":
                field_type = input_field.get_attribute("type")
        except Exception as e:
            continue

        field_data["type"] = field_type
        field_data["default_value"] = input_field.get_attribute("value")
        field_data["mandatory"] = "mandatoryfield" in input_field.get_attribute("class")

        if field_type == "select":
            field_data["options_list"] = [opt.text for opt in input_field.find_elements(By.XPATH, "./option")]

        fields.append(field_data)

    for field in fields:
        if field["type"] == "checkbox" or field["type"] == "radio":
            choice = random.choice(field.get("options_list", []))
            self.click_element((By.XPATH, f"//label[text()='{choice}']"))
        elif field["type"] in ["input", "textarea"]:
            self.enter_text((By.ID, field["name"]), self.fake.text())
        elif field["type"] == "date":
            date = (datetime.today() + timedelta(days=13)).strftime("%Y-%m-%d")
            self.enter_text((By.ID, field["name"]), date)
        elif field["type"] == "select":
            select = Select(self._find_element((By.ID, field["name"])))
            select.select_by_index(random.randint(0, len(field.get("options_list", [])) - 1))


def _find_element(self, locator):
    return self.driver.find_element(*locator)


def enter_text(self, locator, text):
    self._find_element(locator).send_keys(text)


def click_element(self, locator):
    self._find_element(locator).click()


def select_dropdown_option(self, locator, option_text):
    select = Select(self._find_element(locator))
    select.select_by_visible_text(option_text)


def _search_within_iframes(self, xpath, multiple_elements=False, max_depth=2):
    self.driver.switch_to.default_content()
    elements = self.driver.find_elements(By.XPATH, xpath)

    if elements:
        return elements[0] if not multiple_elements else elements

    if max_depth == 0:
        return None

    iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
    for iframe in iframes:
        self.driver.switch_to.frame(iframe)
        element = self._search_within_iframes(xpath, multiple_elements, max_depth - 1)
        if element:
            return element
        self.driver.switch_to.default_content()

    return None


def search_element_within_iframes(self, xpath):
    return self._search_within_iframes(xpath, False)


def search_elements_within_iframes(self, xpath):
    return self._search_within_iframes(xpath, True)


class ElementsToBeRetrieved:
    def __init__(self, locator, max_retries=5):
        self.locator = locator
        self.max_retries = max_retries

    def __call__(self, driver):
        retries = 0
        while retries < self.max_retries:
            elements = InputMixins.search_elements_within_iframes(driver, *self.locator)
            if elements:
                return elements
            retries += 1
        return None



def wait_for_page_load(self, timeout=30):
    old_page = self.search_element_within_iframes("/html")
    yield
    WebDriverWait(self.driver, timeout).until(EC.staleness_of(old_page))
import os
import yaml
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

log = Logger(__name__, logging.INFO)
appdata = os.getenv('LOCALAPPDATA')
homep = os.getenv('HOMEPATH')

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.selectors = {}

    def load_selectors(self, platform, page_name):
        with open(f"TAA_extended/selectors/{platform}/{page_name}.yaml", "r") as file:
            self.selectors = yaml.safe_load(file)

    def navigate_to_url(self, url):
        self.driver.get(url)

    def get_title(self):
        return self.driver.title

    def read_yaml(self, file_path):
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)

    def find_file(self, filename, directory):
        for root, dirs, files in os.walk(directory):
            if filename in files:
                return os.path.join(root, filename)
        return None

    def find_element(self, locator_type, locator_value):
        locator_map = {
            "XPATH": By.XPATH,
            "CSS": By.CSS_SELECTOR,
            "ID": By.ID
        }
        return self.driver.find_element(locator_map.get(locator_type), locator_value)

    def identify_environment(self):
        driver_name = str(type(self.driver)).lower()

        web_drivers = ["chrome", "firefox", "edge", "safari", "opera"]
        mobile_drivers = ["android", "ios"]

        if any(driver in driver_name for driver in web_drivers):
            return "web"
        elif any(driver in driver_name for driver in mobile_drivers):
            return "mobile"
        else:
            return None

    def extract_from_text(self, word, locator_type, locator_name, yaml_filename):

        file_path = self.find_file(yaml_filename + ".yaml", "./selectors")
        if not file_path:
            raise FileNotFoundError(f"File {yaml_filename}.yaml not found in selectors directory.")


        env = self.identify_environment()
        if not env:
            print("Choose environment:")
            print("1. Web")
            print("2. Mobile")
            choice = input("Enter choice (1/2): ")
            env = "web" if choice == "1" else "mobile"


        correct_path = os.path.join("./selectors", env, yaml_filename + ".yaml")
        if file_path != correct_path:
            print(f"Suggested path based on environment: {correct_path}")
            file_path = correct_path


        data = self.read_yaml(file_path)


        locator_value = data[locator_name]


        element = self.find_element(locator_type, locator_value)


        txt = element.text


        extractedWord = re.search(word, txt)


        return extractedWord.group() if extractedWord else None








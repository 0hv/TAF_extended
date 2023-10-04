import inspect
import os
import subprocess
import allure
import time
from alive_progress import alive_bar
from behave import register_type, step
from tqdm import tqdm
from behave.model import Scenario, Step
from behave.runner import Context
from termcolor import colored
from colorama import Fore, Style
from PageObjects.mainPage import MainPage
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from behave.model_core import Status
from prettytable import PrettyTable
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from appium import webdriver as appium_webdriver

appdata = os.getenv('LOCALAPPDATA')
homep = os.getenv('HOMEPATH')


def before_all(context):
    # context.driver = MainPage()

    context.role = {}
    context.menu_detail = {}
    context.scenario_detail = {}

    if 'webapp' in context.tags:
        subprocess.call([r'killedge.bat'])
        edgeOptions = webdriver.EdgeOptions()
        edgeOptions.use_chromium = True
        edgeOptions.add_argument("start-maximized")
        # edgeOption.add_argument("headless")
        edgeOptions.add_argument('log-level=3')
        edgeOptions.add_argument(f'--user-data-dir={appdata}\\Microsoft\\Edge\\User Data')
        context.driver = webdriver.Edge(f"{homep}\\browsers\\msedgedriver", options=edgeOptions)
        context.driver.maximize_window()

        context.main = MainPage(context.driver)
        for driver in context.drivers.values():
            driver.maximize_window()

    else:
        # Prise en charge du mobile et des tests API
        desired_caps = {
            'platformName': 'Android',
            'deviceName': 'emulator-5554',
            'app': '[Chemin vers votre application APK]',
        }
        context.driver = appium_webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)



def after_all(context):
    if 'webapp' in context.tags:
        for driver in context.drivers.values():
            driver.close()
            driver.quit()
    else:
        context.driver.quit()


def count_step_lines(step):
    # Get the step definition and location
    step_definition = step.name
    calling_frame = inspect.currentframe().f_back
    calling_filename = calling_frame.f_globals["__file__"]
    calling_lineno = calling_frame.f_lineno

    # Open the step file, read its contents, and count the number of lines
    with open(calling_filename, "r") as f:
        step_file_contents = f.readlines()

    # Count the number of lines in the step definition
    step_lines = len(step_definition.split("\n"))

    return step_lines


def before_step(context, step):
    print('   \̅_̅/̷̚ʾ --------------------')
    print(f"Step: {step.name}")

    context.total_lines = count_step_lines(step)

    # Calculate the step increment based on the total lines
    context.step_increment = 100 / context.total_lines

    # Initialize the animated progress bar with the total number of lines and animation style
    context.progress_bar = alive_bar(context.total_lines, title=f"{step.keyword} {step.name}", spinner="waves")


def after_step(context, step):
    result = step.status.name
    print(result)
    if result == 'passed':
        col_result = colored(result, 'green')
    else:
        col_result = colored(result, 'red')
    print(f"Result of Step: {col_result}")
    if step.status == 'failed':
        allure.attach(context.driver.get_screenshot_as_png(), name='screenshot',
                      attachment_type=allure.attachment_type.PNG)

    # Increment the progress bar by the step increment
    context.progress_bar(context.step_increment)

    # If this is the last step, close the progress bar
    if step == context.scenario.steps[-1]:
        context.progress_bar.close()


def before_feature(context, feature):
    context.scenario_detail["scenario"] = 1
    context.scenario_detail["status"] = "failed"
    context.scenario_detail["role"] = ""
    print(f"\nFeature: {feature.name}\n")

    # Calculate the total number of lines in the feature
    listy = []
    for scenario in feature.scenarios:
        print(scenario)
        listy.extend(iter(scenario.steps))

    print(listy)
    context.total_lines = len(listy)
    print(context.total_lines)
    # Calculate the step increment based on the total lines
    context.step_increment = 100 / context.total_lines

    # Initialize the animated progress bar with the total number of lines and animation style
    context.progress_bar = alive_bar(context.total_lines, title=feature.name, spinner="waves")


def after_feature(context, feature):
    print(f"Result of Feature: {feature.status.name}")

    # Increment the progress bar by the step increment for each step in the feature
    for scenario in feature.scenarios:
        for step in scenario.steps:
            context.progress_bar(context.step_increment * len(step.text.split('\n')))

    # If this is the last feature, close the progress bar
    if feature == context.features[-1]:
        context.progress_bar.close()

        # Initialize the PrettyTable with the headers
        table = PrettyTable()
        table.field_names = ["Feature", "Scenario", "Status"]

        # Loop through the features, scenarios and steps to populate the PrettyTable
        for feature in context.features:
            for scenario in feature.scenarios:
                status = "Passed" if scenario.status == "passed" else "Failed"
                table.add_row([feature.name, scenario.name, status])

        # Print the PrettyTable in the logs
        print(f"\n{table}\n")


def before_scenario(context, scenario):
    context.logoff = True
    barre = '======================================================================================================'
    highlight_barre = colored(barre, 'yellow')
    print(highlight_barre)

    scen = f"Scenario: {scenario.name}"
    highlight_scen = colored(scen, 'blue', attrs=['bold', 'reverse'])
    print(highlight_scen)

    list2 = []
    for step in scenario.steps:
        print(step)
        list2.append(step)

    print(list2)
    context.total_lines = len(list2)

    # Calculate the step increment based on the total lines
    context.step_increment = 100 / context.total_lines

    # Initialize the animated progress bar with the total number of lines and animation style
    context.progress_bar = alive_bar(context.total_lines, title=scenario.name, spinner="waves")


def after_scenario(context, scenario):
    print(f"Result of Scenario: {scenario.status.name}\n")
    context.scenario_detail["scenario"] = context.scenario_detail["scenario"] + 1
    context.scenario_detail["status"] = scenario.status.name
    barre = '======================================================================================================'
    highlight_barre = colored(barre, 'yellow')
    print(highlight_barre)

    if scenario.status.name == "failed":
        print("Test failed, please press any key to continue")
        input()
        pass

    if context.logoff == True:
        context.main.log_off_from_system()
        # context.driver.switch_to.default_content()
        # # context.driver.find_element(By.XPATH,configReader.readConfig("locators", "profile_icon_XPATH")).click()
        # # context.driver.find_element(By.XPATH,configReader.readConfig("locators", "logOff_XPATH")).click()
        # action = ActionChains(context.driver)
        # action.send_keys(Keys.CONTROL,'q')
        # context.driver.close()
        # context.driver.quit()
        # for i in range(30):
        #     command = "behave --tags=@Approval1"
        #     subprocess.call(command, shell=True)

    # Increment the progress bar by the step increment for each step in the scenario
    for step in scenario.steps:
        context.progress_bar(context.step_increment * len(step.text.split('\n')))

    # If this is the last scenario, close the progress bar
    if scenario == context.feature.scenarios[-1]:
        context.progress_bar.close()

import os
import subprocess
from datetime import datetime
import shutil


import pytest

from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

# Chrome Start

# @pytest.fixture(scope="class", autouse=True)
# def browser_setup(request):
#     options = webdriver.ChromeOptions()
#     options.page_load_strategy = 'eager' 
#     service = Service(executable_path=ChromeDriverManager().install())
#     request.cls.driver = webdriver.Firefox(service=service, options=options)

# Chrome End

# Firefox Start

@pytest.fixture(scope="class", autouse=True)
def browser_setup(request):
    options = webdriver.FirefoxOptions()
    options.page_load_strategy = 'eager' 
    options.add_argument("--headless")
    options.add_argument("--new-instance")
    service = Service(executable_path=GeckoDriverManager().install())
    request.cls.driver = webdriver.Firefox(service=service, options=options)


# @pytest.fixture(scope="class", autouse=True)
# def browser_setup(request):
#     options = webdriver.FirefoxOptions()
#     options.page_load_strategy = 'eager'
#     # options.add_argument("--headless") 
#     # capabilities = webdriver.DesiredCapabilities().FIREFOX
#     # capabilities["marionette"] = False
#     # options.add_argument("--new-instance")
#     capabilities = webdriver.DesiredCapabilities.FIREFOX.copy()
#     service = Service(executable_path='/usr/local/bin/geckodriver', capabilities=capabilities)
#     request.cls.driver = webdriver.Firefox(service=service, options=options)


# Firefox End

# def pytest_collection_modifyitems(session, config, items):
#     try:
#         with open("order.txt") as f:
#             order = [line.strip() for line in f.readlines()]

#         order_abs = [os.path.abspath(path) for path in order]

#         selected_items = [item for item in items if os.path.abspath(item.fspath) in order_abs]

#         ordered_items = []
#         for path in order_abs:
#             ordered_items.extend([item for item in selected_items if os.path.abspath(item.fspath) == path])

#         items[:] = ordered_items  
        
#         if not items:
#             print("No tests matched the paths in order.txt")

#     except FileNotFoundError:
#         print("Order file not found.")
#         items[:] = []

def pytest_sessionstart(session):
    result_path = 'AllureReport'
    if os.path.exists(result_path):
        shutil.rmtree(result_path)
    os.makedirs(result_path)


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    # cur_dir = 'reports'
    today = datetime.now()
    folderName = today.strftime("%Y-%m-%d")
    fileName = today.strftime("%Y-%m-%d-%H-%M")
    result_path = os.path.join(f'AllureReport')
    report_path = os.path.join(f'reports/{folderName}/{fileName}')
    print(report_path)
    process = f'allure generate {result_path} --name Node-Flicknexs --single-file -o {report_path} ' #Change name
    s = subprocess.getstatusoutput(process)
    print(s[1])

    # Remove-Item .pytest_cache -Recurse -Force
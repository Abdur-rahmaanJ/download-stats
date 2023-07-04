from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
# from fake_useragent import UserAgent
from latest_user_agents import get_random_user_agent
from rich.console import Console
import time
import sys

console = Console()


def stats(project: str, no_rich=False) -> dict:
    options = Options()
    options.add_argument('--headless')
    options.add_argument("--incognito")
    options.add_argument("--nogpu")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,1280")
    options.add_argument("--no-sandbox")
    options.add_argument("--enable-javascript")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    #ua = UserAgent()
    #ua = get_random_user_agent()
    #userAgent = ua.random
    userAgent = get_random_user_agent()
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": userAgent})

    if no_rich:
        driver.get(f'https://pepy.tech/project/{project}')
        time.sleep(5)
    else:
        with console.status("[bold green]Getting content...") as status:
            driver.get(f'https://pepy.tech/project/{project}')
            time.sleep(5)

    try:
        elems = driver.find_elements('xpath', "//*[contains(@class,'MuiGrid-item')]")
        # for i, e in enumerate(elems):
        #     print(i, e.text)
        by_version = [e for e in elems[19].text.split('\n')]

        table_data = []
        start_version_collecting = False
        for i, x in enumerate(by_version):
            if 'Sum' in by_version[i]:
                start_version_collecting = True
            if start_version_collecting:
                table_data.append(by_version[i].split())

    except IndexError:
        sys.exit('Package could not be loaded!')

    return {
        'total': elems[5].text.replace(',',''),
        '30_days': elems[7].text.replace(',',''),
        '7_days': elems[9].text.replace(',',''),
        'by_version': table_data
    }
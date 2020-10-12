from selenium.webdriver.chrome.options import Options
from selenium import webdriver

class Driver:
    def __init__(self):
        self.driver = self.initialize_driver()

    def initialize_driver(self):
        user_data_dir = '/home/huzaifa/.config/google-chrome/selenium'

        options = Options()
        options.add_argument(f'--user-data-dir={user_data_dir}')

        driver = webdriver.Chrome(executable_path='./chromedriver', options=options, service_args=['--silent'])
        return driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from playsound import playsound

import sys

class Utils:
    def __init__(self, driver):
        self.driver = driver

    @staticmethod
    def clear_fields(*args):
        for element in args:
            element.clear()

    def navigate(self, url):
        if self.driver.current_url == url:
            return 
        self.driver.get(url)
    
    def url_starts_with(self, url):
        return self.driver.current_url.startswith(url)

    def click_js(self, element):
        self.driver.execute_script('arguments[0].click()', element)

    def scroll_to_element(self, element):
        self.driver.execute_script('window.scroll(0, arguments[0])', element)

    def quit(self):
        self.driver.close()
        sys.exit()

    def scroll_to_end(self):
        self.driver.execute_script('''
            window.scrollTo(0, document.body.scrollHeight)
        ''')

    def handle_error(self, error):
        playsound('./alert_sound.mp3')
        print(error)
        print("If error is not helpful, do the commanded action manually, and if still fails, contact the developer")
        self.quit()
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sys

from util import Utils
from twitter_common import TwitterCommon
from twitter_urls import TwitterUrls

class Login:

    def __init__(self, driver):
        self.driver = driver
        self.twitter_common = TwitterCommon(driver)
        self.utils = Utils(driver)

    def __find_elements(self):
        try:
            username_or_email_field = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, "session[username_or_email]")))
            password_field = self.driver.find_element_by_name("session[password]")
        except:
            self.utils.handle_error("Login: username or password xpath outdated")

        return (username_or_email_field, password_field)

    @property
    def logged_in(self):
        return not not self.twitter_common.get_cookie("auth_token")

    def __submit_login_credentials(self, username_or_email, password):
        username_or_email_field, password_field = self.__find_elements()

        Utils.clear_fields(username_or_email_field, password_field)

        username_or_email_field.send_keys(username_or_email)
        password_field.send_keys(password)
        password_field.send_keys(Keys.ENTER)

    def __handle_login_errors(self):
        error = self.utils.url_starts_with("https://twitter.com/login/error")
        if not error:
            return

        try:
            error = self.driver.find_element_by_css_selector('div[class="css-901oao r-daml9f r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-qvutc0"] > span[class="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0"]').text
        except Exception as err:
            error = err

        self.utils.handle_error(error)
        
    def login(self, username_or_email, password):
        if (self.logged_in):
            return

        self.utils.navigate(TwitterUrls.twitter_loginurl)
        self.__submit_login_credentials(username_or_email, password)

        self.__handle_login_errors()

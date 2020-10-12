from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from util import Utils

from login import Login

class Logout:
    def __init__(self, driver):
        self.driver = driver
        self.utils = Utils(driver)

    def logout(self):
        logged_in = Login(self.driver).logged_in
        if not logged_in:
            self.utils.quit()

        self.driver.get('https://twitter.com/logout')

        try:
            confirm_logout_btn = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="confirmationSheetConfirm"]')))
        except NoSuchElementException:
            self.utils.handle_error("Logout: confirm logout button xpath outdated")
        else:
            self.utils.click_js(confirm_logout_btn)
            self.utils.quit()

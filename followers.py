from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import sys
import random

from util import Utils
from twitter_urls import TwitterUrls

class Followers:
    def __init__(self, driver):
        self.driver = driver
        self.utils = Utils(driver)

    def __find_followable_people_element(self):
            tries = 0

            while True:
                tries += 1
                try:
                    follow_element = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@style,"position: absolute;") and .//div[contains(@data-testid, "-follow")]]')))
                except Exception as error:
                    if tries > 2:
                        self.utils.handle_error(error)

                    self.utils.scroll_to_end()
                    continue
                else:
                    return follow_element


    def __find_username_and_follow_btn(self, follow_element):
        try:
            username = follow_element.find_element_by_xpath('.//div[contains(@class, "r-1re7ezh r-18u37iz")]/span').text
            follow_btn = follow_element.find_element_by_xpath('.//div[contains(@data-testid, "-follow")]')
        except:
            self.utils.handle_error("Followers: username or follow_btn xpath outdated")


        return (username, follow_btn)

    def __handle_if_error_occured(self, username, last_followed_user):
        if username == last_followed_user:
            try:
                error = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="toast"]//div[contains(@class, "r-16dba41")]//span'))).text
            except NoSuchElementException:
                error = "Followers: Xpath for error text of followers is outdated"
            except:
                error = "Followers: Unexpected error"

            self.utils.handle_error(error)

    def __wait_before_next_follow(self):
        delay = round(random.uniform(2, 4), 3)
        print(f"Waiting {delay} seconds before next follow")
        time.sleep(delay)

    def follow(self, username_or_query, is_username=True, limit=400):
        if is_username:
            self.utils.navigate(TwitterUrls.get_link_of_user_followers(username_or_query))
        else:
            self.utils.navigate(TwitterUrls.get_twitter_users_link(username_or_query))

        current_iteration = 1
        last_followed_user = None

        while current_iteration <= limit:
            current_iteration += 1

            follow_element = self.__find_followable_people_element()
            username, follow_btn = self.__find_username_and_follow_btn(follow_element)

            self.__handle_if_error_occured(username, last_followed_user)
            self.utils.click_js(follow_btn)

            print(f"Just followed {username}")
            last_followed_user = username

            self.__wait_before_next_follow()
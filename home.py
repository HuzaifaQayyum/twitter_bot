from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from playsound import playsound
import time
import random

from util import Utils
from twitter_urls import TwitterUrls

class Home:
    def __init__(self, driver, username):
        self.driver = driver
        self.utils = Utils(driver)
        self.username = username

    def __find_post(self):
        tries = 0

        while True:
            tries += 1

            try:
                post = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, f'//div[ .//div[@data-testid="like"] and contains(@style, "position: absolute") and .//div[ contains( @class, "css-bfa6kz r-1re7ezh")]//span[text() != "{self.username}" ] ]')))
            except Exception as error:
                if (tries > 2):
                    playsound('./alert_sound.mp3')
                    print(error)

                    if input("Do you want to quitr? y/n").lower() == 'n':
                        tries = 0
                        continue

                    self.utils.quit()

                self.utils.scroll_to_end()
                continue
            else:
                return post

    def __find_required_elements(self, post):
        try:
            username = post.find_element_by_xpath('.//div[ contains( @class, "css-bfa6kz r-1re7ezh")]//span').text
            like_btn = post.find_element_by_xpath('.//div[@data-testid="like"]')
            reply_btn = post.find_element_by_xpath('.//div[@data-testid="reply"]')
        except:
            self.utils.handle_error("Home: username, likebtn or reply btn xpath outdated")

        return (username, like_btn, reply_btn)

    def __reply(self, reply_btn, comment):
        self.utils.click_js(reply_btn)
        try:
            reply_input = self.driver.find_element_by_xpath('(//div[@data-testid="tweetTextarea_0"])[1]')
        except:
            self.utils.handle_error("Home: Reply input field xpath outdated")
        else:
            reply_input.send_keys(comment, Keys.CONTROL + Keys.ENTER)

    def __get_comment(self):
        comments = [
            f"Nice post",
            f"Awesome work",
            f"Impressive work",
            f"Coool"
        ]
        return comments[random.randint(0, len(comments) -1)]


    def __handle_like_error(self, like_btn):
        print(like_btn.get_attribute('data-testid'))

        if like_btn.get_attribute('data-testid') != 'unlike':
            try:
                error = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="toast" and @role="alert"]//span'))).text
            except NoSuchElementException:
                error = """Home: Like error occured...\nPossible Reasons:\n1: Slow internet\n2: Xpath for error text of like is outdated OR error text is not displayed by twitter"""
            except:
                error = 'Home: Unexpected error'

            self.utils.handle_error(error)

    def like_and_comment(self, like_only=True, limit=1000):
        self.utils.navigate(TwitterUrls.twitter_home_url)

        current_iteration = 1
        while current_iteration <= limit:
                post = self.__find_post()
                username, like_btn, reply_btn = self.__find_required_elements(post)

                print(":"*20 + f"POST OF user {username} found" + ":"*20)

                self.utils.click_js(like_btn)
                print("-->post liked")
                time.sleep(random.uniform(.5, .8))
                self.__handle_like_error(like_btn)

                if not like_only:
                    self.__reply(reply_btn, self.__get_comment())
                    print("-->replied to the post")

                    delay = random.uniform(2, 4)
                    print(f"Waiting {delay} seconds.")
                    time.sleep(delay)


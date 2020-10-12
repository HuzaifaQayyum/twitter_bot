from twitter_urls import TwitterUrls 
from util import Utils

class TwitterCommon:
    def __init__(self, driver):
        self.driver = driver
        self.utils = Utils(driver)

    def get_cookie(self, name):
        twitter_opened = self.utils.url_starts_with(TwitterUrls.twitter_url)
        if not twitter_opened:
            self.driver.get(TwitterUrls.twitter_url)

        return self.driver.get_cookie(name)
from driver import Driver
from login import Login
from followers import Followers
from home import Home
from logout import Logout
from util import Utils

driver = Driver().driver
util = Utils(driver)

def main():
    username = ""
    password = ""

    Login(driver).login(username, password)
    # Followers(driver).follow('jannatmirza07')
    # Home(driver, username).like_and_comment()
    # Logout(driver).logout()

try:
    main()
except Exception as error:
    util.handle_error(error)
    
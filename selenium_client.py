import os

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class SeleniumClient(object):
    @classmethod
    def with_driver(cls):
        return cls(webdriver.Firefox())

    @classmethod
    def user_driver(cls):
        return cls(
            webdriver.Firefox(firefox_binary=FirefoxBinary(
                os.path.expanduser("~/Applications/Firefox.app/Contents/MacOS/firefox"))))

    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.main_window = self.webdriver.current_window_handle
        self.webdriver.implicitly_wait(1)

    def login(self, username, password):
        self.webdriver.get("http://www.huffingtonpost.com")
        self.webdriver.find_element_by_id("hp_login_bt").click()
        while True:
            try:
                self.webdriver.find_element_by_class_name("google-plus").click()
            except NoSuchElementException:
                pass
            else:
                break
        self.go_to_not_main_window()
        self.google_login(username,password)

    def go_to_not_main_window(self):
        for handle in self.webdriver.window_handles:
            if self.main_window != handle:
                self.webdriver.switch_to_window(handle)
                return

    def google_login(self, username, password):
        email = self.webdriver.find_element_by_id("Email")
        email.click()
        email.send_keys(username)
        password_element = self.webdriver.find_element_by_id("Passwd")
        # WebDriverWait(self.webdriver, 4).until(
        #     EC.element_to_be_selected(
        #         password
        #     )
        # )
        password_element.click()
        password_element.send_keys(password)
        self.webdriver.find_element_by_id("signIn").click()

    def switch_to_window(self):
        self.webdriver.switch_to_window(self.main_window)

    def article_search(self):
        self.webdriver.find_element_by_class_name("quickread_link").click()

    def share_on_google_plus(self):
        self.webdriver.find_element_by_class_name("googleplus").find_element_by_tag_name("a").click()
        self.go_to_not_main_window()
        self.webdriver.find_element_by_css_selector("div.b-c:nth-child(1)").click()

def load_credentials(filename="credentials.json"):
    import simplejson
    with open(filename, "r") as credentialfile:
        return simplejson.loads(credentialfile.read())

def main():
    credentials = load_credentials()
    selenium_client = SeleniumClient.with_driver()
    selenium_client.login(**credentials)
    selenium_client.switch_to_window()
    selenium_client.article_search()
    selenium_client.share_on_google_plus()

if __name__ == '__main__':
    main()


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select


class BasePage(object):
    def __init__(self, base_url='https://online.hcmue.edu.vn/') -> None:
        self.options = Options()
        self.options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(
            options=self.options)
        self.base_url = base_url

    def login(self, user, password):
        self.driver.get(self.base_url)
        self.driver.find_element(By.ID, 'lbtDangnhap').click()
        self.driver.find_element(
            By.ID, 'ContentPlaceHolder1_ctl00_ctl00_rbtnStaff').click()

        input_user = self.driver.find_element(
            By.ID, 'ContentPlaceHolder1_ctl00_ctl00_txtUserName')
        input_password = self.driver.find_element(
            By.ID, 'ContentPlaceHolder1_ctl00_ctl00_txtPassword')

        input_user.send_keys(user)
        input_password.send_keys(password)

        self.driver.find_element(
            By.ID, 'ContentPlaceHolder1_ctl00_ctl00_btLogin').click()

    def select_level(self):
        select = Select(self.driver.find_element(
            By.ID, 'ContentPlaceHolder1_ctl00_ctl00_ctl00_ddlGraduateLevel'))
        select.select_by_visible_text('Đại học')

    def get_list_class(self):
        select_class = Select(self.driver.find_element(
            By.ID, 'ContentPlaceHolder1_ctl00_ctl00_ctl00_ddlClass'))
        options = select_class.options

        return [option.text for option in options]

    def get_data(self):
        ...


page = BasePage()
page.login('minhlt_TCHC', 'minhlt_TCHC')
page.select_level()
page.get_list_class()

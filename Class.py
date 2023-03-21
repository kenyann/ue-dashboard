from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from typing import List
from tqdm import tqdm
import pandas as pd
import os


class BasePage(object):
    def __init__(self, _base_url='https://online.hcmue.edu.vn/') -> None:
        self.options = Options()
        self.options.add_experimental_option("detach", True)
        self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(
            options=self.options)
        self.base_url = _base_url

    def login(self, _user, _password):
        self.driver.get(self.base_url)
        self.driver.find_element(By.ID, 'lbtDangnhap').click()
        self.driver.find_element(
            By.ID, 'ContentPlaceHolder1_ctl00_ctl00_rbtnStaff').click()

        input_user = self.driver.find_element(
            By.ID, 'ContentPlaceHolder1_ctl00_ctl00_txtUserName')
        input_password = self.driver.find_element(
            By.ID, 'ContentPlaceHolder1_ctl00_ctl00_txtPassword')

        input_user.send_keys(_user)
        input_password.send_keys(_password)

        self.driver.find_element(
            By.ID, 'ContentPlaceHolder1_ctl00_ctl00_btLogin').click()

    def get_listOptions(self, _content) -> List:
        select = Select(self.driver.find_element(
            By.ID, f'ContentPlaceHolder1_ctl00_ctl00_ctl00_ddl{_content}'))
        options = select.options

        return [option.text for option in options]

    def select_content(self, _content, _option):
        select = Select(self.driver.find_element(
            By.ID, f'ContentPlaceHolder1_ctl00_ctl00_ctl00_ddl{_content}'))
        select.select_by_visible_text(_option)

    def get_studentData(self, _department='Departments', _class='Class', _courses='Courses'):
        course_options = self.get_listOptions(_content=_courses)
        for course_option in course_options:
            print(course_option)
            self.select_content(_content=_courses, _option=course_option)
            department_options = self.get_listOptions(_content=_department)
            for department_option in (department_options[1:]):
                print(department_option)
                self.select_content(_content=_department,
                                    _option=department_option)
                class_options = self.get_listOptions(_content=_class)
                for class_option in (class_options):
                    print(class_option)
                    self.select_content(_content=_class, _option=class_option)
                    self.crawl(department_option, course_option, class_option)
                print('----------------------------')

    def crawl(self, _department, _course, _class):
        if not os.path.exists("data"):
            os.mkdir("data")

        if not os.path.exists(f"data/{_department}"):
            os.mkdir(f"data/{_department}")

        if not os.path.exists(f"data/{_department}/{_course}"):
            os.mkdir((f"data/{_department}/{_course}"))

        data_column = [["STT", "Mã sinh viên", "Họ lót", "Tên", "Ngày sinh",
                        "Xem điểm", "Lịch học", "Thông tin", "Lịch thi", "Học phí"]]
        link_column = [["Xem điểm", "Lịch học",
                        "Thông tin", "Lịch thi", "Học phí"]]

        data, link = [], []
        try:
            table_id = self.driver.find_element(
                By.ID, 'ContentPlaceHolder1_ctl00_ctl00_ctl00_grvListStudent')
            rows = table_id.find_elements(By.TAG_NAME, 'tr')
            for row in rows[1:]:
                cols = row.find_elements(By.TAG_NAME, "td")
                links = row.find_elements(By.TAG_NAME, "a")
                data.append([col.text for col in cols])
                link.append([link.get_attribute("href") for link in links])

            data_df = pd.DataFrame(data=data, columns=data_column)
            link_df = pd.DataFrame(data=link, columns=link_column)

            data_df = data_df[["STT", "Mã sinh viên",
                               "Họ lót", "Tên", "Ngày sinh"]]

            df = pd.concat([data_df, link_df], axis=1)
            df.to_csv(f"data/{_department}/{_course}/{_class}.csv")
        except:
            return


page = BasePage()
page.login('minhlt_TCHC', 'minhlt_TCHC')
options = page.get_listOptions('GraduateLevel')
page.select_content('GraduateLevel', options[1])
page.get_studentData()

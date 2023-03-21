from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import pandas as pd

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://online.hcmue.edu.vn/")

login = driver.find_element(By.ID, 'lbtDangnhap')
login.click()

staff = driver.find_element(By.ID, 'ContentPlaceHolder1_ctl00_ctl00_rbtnStaff')
staff.click()

input_user = driver.find_element(
    By.ID, 'ContentPlaceHolder1_ctl00_ctl00_txtUserName')
input_password = driver.find_element(
    By.ID, 'ContentPlaceHolder1_ctl00_ctl00_txtPassword')

input_user.send_keys('minhlt_TCHC')
input_password.send_keys('minhlt_TCHC')

driver.find_element(By.ID, 'ContentPlaceHolder1_ctl00_ctl00_btLogin').click()

select = Select(driver.find_element(
    By.ID, 'ContentPlaceHolder1_ctl00_ctl00_ctl00_ddlGraduateLevel'))
select.select_by_visible_text('Đại học')

select_class = Select(driver.find_element(
    By.ID, 'ContentPlaceHolder1_ctl00_ctl00_ctl00_ddlClass'))
select_class.select_by_visible_text('Công nghệ thông tin A')

table_id = driver.find_element(
    By.ID, 'ContentPlaceHolder1_ctl00_ctl00_ctl00_grvListStudent')

rows = table_id.find_elements(By.TAG_NAME, 'tr')
data = []
link = []
column = [["STT", "Mã sinh viên", "Họ lót", "Tên", "Ngày sinh",
           "Xem điểm", "Lịch học", "Thông tin", "Lịch thi", "Học phí"]]
for row in rows[1:]:
    cols = row.find_elements(By.TAG_NAME, "td")
    data.append([col.text for col in cols])
    links = row.find_elements(By.TAG_NAME, "a")
    link.append([link.get_attribute("href") for link in links])

link_col = [["Xem điểm", "Lịch học", "Thông tin", "Lịch thi", "Học phí"]]

df = pd.DataFrame(data=data, columns=column)
df2 = df[["STT", "Mã sinh viên", "Họ lót", "Tên", "Ngày sinh"]]
df_link = pd.DataFrame(data=link, columns=link_col)

dt = pd.concat([df2, df_link], axis=1)
dt.to_csv("/home/ken/Work/ue-dashboard/data_2.csv", index=False)

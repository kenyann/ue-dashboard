import Class
from Class import BasePage, MarkPage
from Class import getUrlFromCSV
import glob
import multiprocessing
from multiprocessing import Pool, Process


def job(list_stu, list_url):
    page = MarkPage()
    page.login('minhlt_TCHC', 'minhlt_TCHC')
    for stu, url in zip(list_stu, list_url):
        page.crawlMarks(url, stu)


if __name__ == '__main__':

    data_path = glob.glob('data/info/*/*/*.csv')
    student_list, url_list = [], []
    for file in data_path[:10]:
        stu, url = getUrlFromCSV(file)
        student_list.append(stu)
        url_list.append(url)

    process_1 = Process(target=job, args=(
        student_list[0][:3], url_list[0][:3]))
    process_2 = Process(target=job, args=(
        student_list[0][3:5], url_list[0][3:5]))

    process_1.start()
    process_2.start()

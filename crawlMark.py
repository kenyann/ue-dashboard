import Class
from Class import BasePage, MarkPage
from Class import getUrlFromCSV
import glob
import multiprocessing
from multiprocessing import Pool, Process
from tqdm import tqdm


def job(url, stu):
    page = MarkPage(headless=True)
    page.login('minhlt_TCHC', 'minhlt_TCHC')
    page.crawlMarks(url, stu)
    print(f'Done {stu}')
    page.close()


if __name__ == '__main__':

    data_path = glob.glob('data/info/*/*/*.csv')
    student_list, url_list = [], []
    for file in data_path:
        stu, url = getUrlFromCSV(file)
        student_list.extend(stu)
        url_list.extend(url)

    pool = Pool(processes=4)
    results = pool.starmap(job, zip(url_list, student_list), chunksize=4)

# page = MarkPage()
# page.login('minhlt_TCHC', 'minhlt_TCHC')
# page.close()

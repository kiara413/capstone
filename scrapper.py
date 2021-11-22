import requests
from bs4 import BeautifulSoup

def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "tplPagination"}).find_all("a")
    last_page = pages[-2].string
    return int(last_page)  #10

def extract_job(html):
    title = html.find("div", {"class": "post-list-info"}).find("a")["title"]
    company = html.find("div", {"class": "post-list-corp"}).find("a")["title"]
    location = html.find("div", { "class": "post-list-info"}).find("span", {
    "class": "long"}).string
    job_val = html["data-gno"]
    return {
    'title': title,
    'company': company,
    'location': location,
    'link': f"https://www.jobkorea.co.kr/Recruit/GI_Read/{job_val}"}

def extract_jobs(last_page, url):
    jobs = []
    for page in range(1, last_page + 1):
        print(f"Scrapping JK: Page: {page}")
        result = requests.get(f"{url}&Page_No={page}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find("div", { "class": "lists" }).find_all("li", {"class":"list-post"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
            # print(job)
    return jobs


def get_jobs(word):
    url = f"https://www.jobkorea.co.kr/Search/?stext={word}"
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page, url)
    return jobs

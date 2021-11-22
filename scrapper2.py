import requests
from bs4 import BeautifulSoup

def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class": "pagination"})
    links = pagination.find_all('a')
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))
    last_page = pages[-1]
    return int(last_page)

def extract_job(html):
    title = html.find("div", {"class": "area_job"}).find('a')["title"]
    company = html.find("div", {"class": "area_corp"}).find('a')["title"]
    location = html.find("div", {"class": "job_condition"}).find("span").text
    job_val = html["value"]
    return {
    'title':title,
    'company':company,
    'location': location,
    'link': f"https://www.saramin.co.kr/zf_user/jobs/relay/view?rec_idx={job_val} "}

def extract_jobs(last_page, url):
    jobs = []
    for page in range(1, last_page + 1):
        print(f"Scrapping Saramin: Page: {page}")
        result = requests.get(f"{url}&recruitPage={page}") 
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "item_recruit"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs2(word):
    url = f"https://www.saramin.co.kr/zf_user/search/recruit?searchword={word}&recruitPageCount=50"
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page, url)
    return jobs
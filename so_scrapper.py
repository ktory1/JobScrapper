import requests
from bs4 import BeautifulSoup

def get_last_page(url):
  result = requests.get(url)
  soup = BeautifulSoup(result.text, "html.parser")
  if soup.find("div", {"class":"s-pagination"}):
    pages = soup.find("div", {"class":"s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
  else:
    last_page = 1
  return int(last_page)

def extract_jobs(last_page, url):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping SO page {page}")
    result = requests.get(f"{url}&pg={page+1}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div",{"class":"-job"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs

def extract_job(html):
  title = html.find("h2").find("a")["title"]
  company, location = html.find("h3").find_all("span", recursive=False)
  if location is not None:
    location = location.get_text(strip = True)
  company = company.get_text(strip=True)
  job_id = html['data-jobid']
  return {
    'title': title,
    'company': company,
    'location':location,
    'apply_link': f"https://stackoverflow.com/jobs/{job_id}"
  }

def get_jobs(word):
  url = f"https://stackoverflow.com/jobs?q={word}&l=Canada&d=20&u=Km"
  last_page = get_last_page(url)
  jobs = extract_jobs(last_page, url)
  return jobs
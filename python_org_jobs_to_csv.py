import requests
from bs4 import BeautifulSoup
import pandas as pd

# Target URL
url = "https://www.python.org/jobs/"

# Add headers to look like a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# Fetch the webpage
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Find the list of job postings
job_list = soup.find("ol", class_="list-recent-jobs")
jobs = []

for job_item in job_list.find_all("li"):
    title_tag = job_item.find("h2", class_="listing-company")
    location_tag = job_item.find("span", class_="listing-location")
    date_tag = job_item.find("time")
    link_tag = job_item.find("a")

    title = title_tag.text.strip() if title_tag else ""
    location = location_tag.text.strip() if location_tag else ""
    publish_date = date_tag.text.strip() if date_tag else ""
    detail_link = "https://www.python.org" + link_tag['href'] if link_tag else ""

    jobs.append({
        "Title": title,
        "Location": location,
        "Publish Date": publish_date,
        "Detail Link": detail_link
    })

# Save to CSV
df = pd.DataFrame(jobs)
df.to_csv("python_org_jobs.csv", index=False)
print("Jobs saved successfully to python_org_jobs.csv")

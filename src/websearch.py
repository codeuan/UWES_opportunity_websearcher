import requests
from bs4 import BeautifulSoup

response = requests.get(
    "https://yubhub.co/jobs/search/",
    params={"q": "electronics", "sort": "newest"},
    timeout=15,
) #look for latest electronics jobs.
response.raise_for_status() #check for errors.
soup = BeautifulSoup(response.content, "html.parser") #convert raw HTML data into a tree for parsing.

for row in soup.select("li.job-row"): #for each job listing.
    link = row.select_one('a.font-display[href*="/job/"]') #address of job details page.
    if link is None:
        continue

    date = row.select_one("span.font-mono.whitespace-nowrap")
    print(
        date.get_text(strip=True) if date else "",
        link.get_text(" ", strip=True), #.get() reads an HTML attribute.
        row.get("data-company", ""),
        row.get("data-location", ""),
        link["href"],
        sep=" | ",
    )

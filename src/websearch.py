import requests
from bs4 import BeautifulSoup
from webhook import sendToChannel
import json
from pathlib import Path

POSTED_JOBS = Path(__file__).with_name("posted_jobs.json")

def websearch(search_params, heading):
    response = requests.get(
        "https://yubhub.co/jobs/search/",
        params={**search_params, "sort": "newest"},
        timeout=15,
    ) #look for latest electronics jobs.
    response.raise_for_status() #check for errors.
    soup = BeautifulSoup(response.content, "html.parser") #convert raw HTML data into a tree for parsing.
    
    posted_urls = (
        set(json.loads(POSTED_JOBS.read_text(encoding="utf-8")))
        if POSTED_JOBS.exists()
        else set()
    )
    seen_urls = posted_urls.copy()
    
    
    jobs = []
    for row in soup.select("li.job-row"): #for each job listing.
        link = row.select_one('a.font-display[href*="/job/"]') #address of job details page.
        if link is None:
            continue

        logo = row.select_one("img[src]")
        date = row.select_one("span.font-mono.whitespace-nowrap")

        embed = {
            "title": link.get_text(" ", strip=True),
            "url": link["href"],
            "description": (
                f"**{row.get('data-company', '')}**\n" #** is bold Discord markdown.
                f"{row.get('data-location', '')}"
            ),
        }

        if logo:
            embed["thumbnail"] = {"url": logo["src"]} #add company logo.

        if date:
            embed["fields"] = [
                {"name": "Posted", "value": date.get_text(strip=True)}
            ]
        url = embed["url"]
        if url in seen_urls:
            continue

        seen_urls.add(url)
        jobs.append(embed)

    if not jobs:
        sendToChannel([], heading)
        return

    for start in range(0, len(jobs), 10): #send in batches of 10.
        batch = jobs[start:start + 10]
        batch_heading = heading if start == 0 else None
        sendToChannel(jobs[start:start + 10], batch_heading)
        posted_urls.update(job["url"] for job in batch)
        POSTED_JOBS.write_text(
            json.dumps(sorted(posted_urls), indent=2),
            encoding="utf-8",
        ) #update posted_jobs.
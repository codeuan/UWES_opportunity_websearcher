#Entry point of program.
from websearch import websearch

if __name__ == "__main__":
    websearch({"q": "industrial placement"}, "New Industrial Placements")
    websearch(
        {"q": "internship", "category": "engineering"},
        "New Engineering Internships",
    )
    websearch({"q": "work experience"}, "New Work Experience Opportunities")
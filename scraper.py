import csv
import requests

APP_ID = "d065aea6"
APP_KEY = "1ea74a67372c9b4c5875ca11c36509f7"
BASE_URL = "https://api.adzuna.com/v1/api/jobs/gb/search/1"

def search_jobs(keyword, location=""):
    response = requests.get(
        BASE_URL,
        params={
            "app_id": APP_ID,
            "app_key": APP_KEY,
            "what": keyword,
            "where": location,
            "results_per_page": 10
        }
    )

    data = response.json()
    jobs = data.get("results", [])

    if not jobs:
        print("No jobs found.")
        return

    print(f"\nFound {data['count']} jobs for '{keyword}'\n")

    for job in jobs:
        print("---")
        print("Title:    ", job["title"])
        print("Company:  ", job["company"]["display_name"])
        print("Location: ", job["location"]["display_name"])
        print("Salary:   ", f"£{job.get('salary_min', 'N/A')} - £{job.get('salary_max', 'N/A')}")
        print("URL:      ", job["redirect_url"])

    filename = f"{keyword.replace(' ', '_')}_jobs.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Company", "Location", "Salary Min", "Salary Max", "URL"])
        for job in jobs:
            writer.writerow([
                job["title"],
                job["company"]["display_name"],
                job["location"]["display_name"],
                job.get("salary_min", "N/A"),
                job.get("salary_max", "N/A"),
                job["redirect_url"]
            ])

    print(f"\nResults saved to {filename}")

keyword = input("Enter job title: ")
location = input("Enter location (or press Enter to skip): ")
search_jobs(keyword, location)
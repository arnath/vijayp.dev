import json
import os
import requests
from typing import Any

next_csrf_token: str | None = None


def get_apple_jobs(locations_file_path: str | None = None):
    if not locations_file_path:
        locations_file_path = (
            "src/lib/better-apple-job-search/locations-2024-09-01.json"
        )

    with open(locations_file_path, "r") as file:
        locations = json.loads(file.read())

    parsed_jobs: dict[str, Any] = {}
    for index, location in enumerate(locations):
        print(f"Handling location {index + 1}: {location}")
        jobs = get_for_location(location)
        for job in jobs:
            parsed_jobs[job["id"]] = {
                "id": job["id"],
                "link": f"https://jobs.apple.com/en-us/details/{job['positionId']}",
                "postDate": job.get("postDateInGMT"),
                "title": job["postingTitle"],
                "summary": job["jobSummary"],
                "teamName": job.get("team", {})["teamName"],
                "remoteOK": bool(job.get("homeOffice", "False")),
                "location": location["displayName"],
            }

    with open(
        os.path.join("src/lib/better-apple-job-search", "jobs.json"), "w"
    ) as output_file:
        output_file.write(json.dumps(list(parsed_jobs.values())))


def get_for_location(location: Any) -> list[Any]:
    global next_csrf_token

    jobs = []
    expected_job_count = 1
    request = {
        "query": "",
        "locale": "en-us",
        "filters": {"postingpostLocation": [location["id"]]},
        "page": 1,
    }
    while True:
        response = requests.post(
            "https://jobs.apple.com/api/role/search",
            json=request,
        )

        try:
            response_json = response.json()
        except:
            print(f"request failed, response content: {response.text}")
            response_json = {}

        original_job_count = len(jobs)
        jobs.extend(response_json.get("searchResults", []))
        total_records = response_json.get("totalRecords")
        if total_records:
            expected_job_count = int(total_records)

        if len(jobs) == original_job_count or len(jobs) == expected_job_count:
            break

        request["page"] += 1

    return jobs


if __name__ == "__main__":
    get_apple_jobs()

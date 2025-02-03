from datetime import datetime, timezone
import json
import os
import requests
from typing import Any

OUTPUT_DIRECTORY = "src/lib/better-apple-job-search"


def get_apple_jobs(locations_file_path: str | None = None):
    # I made a few smaller location files for testing but this is the default.
    if not locations_file_path:
        locations_file_path = (
            "src/lib/better-apple-job-search/locations-2024-09-01.json"
        )

    with open(locations_file_path, "r") as file:
        locations = json.loads(file.read())

    # Handle each location one at a time.
    parsed_jobs: dict[str, Any] = {}
    for index, location in enumerate(locations):
        jobs = get_for_location(location)
        original_length = len(parsed_jobs)
        for job in jobs:
            if job["id"] not in parsed_jobs:
                parsed_jobs[job["id"]] = {
                    "link": f"https://jobs.apple.com/en-us/details/{job['positionId']}",
                    **job,
                }

        # We do this because jobs are sometimes listed twice across two locations. We have more
        # specific locations first so they won't be overwritten in the dictionary.
        print(
            f"Handled location {index + 1} {location['displayName']}, added {len(parsed_jobs) - original_length} jobs"
        )

    # Write the jobs as JSON.
    with open(os.path.join(OUTPUT_DIRECTORY, "jobs.json"), "w") as jobs_json:
        jobs_json.write(json.dumps(list(parsed_jobs.values())))

    # Write the date that the jobs were last updated.
    with open(
        os.path.join(OUTPUT_DIRECTORY, "update_timestamp.txt"), "w"
    ) as update_timestamp:
        update_timestamp.write(datetime.now(timezone.utc).strftime("%Y-%m-%d"))


def get_for_location(location: Any) -> list[Any]:
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

        # The response sometimes includes a "totalRecords" value. If this is present, we use
        # it to get the expected number of jobs.
        original_job_count = len(jobs)
        jobs.extend(response_json.get("searchResults", []))
        total_records = response_json.get("totalRecords")
        if total_records:
            expected_job_count = int(total_records)

        # Stop asking for new pages if we either hit the expected count or didn't find any new
        # jobs.
        if len(jobs) == original_job_count or len(jobs) == expected_job_count:
            break

        # Ask for the next page.
        request["page"] += 1

    return jobs


if __name__ == "__main__":
    get_apple_jobs()

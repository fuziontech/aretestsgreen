import os

import requests
from dotenv import load_dotenv

load_dotenv()


def get_latest_commit_status(username, token, owner, repo_name):
    url = f"https://api.github.com/repos/{owner}/{repo_name}/commits"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"token {token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return

    commits = response.json()
    latest_commit_sha = commits[0]["sha"]

    url = f"https://api.github.com/repos/{owner}/{repo_name}/commits/{latest_commit_sha}/check-runs"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return

    check_runs = response.json()["check_runs"]

    all_passed = True
    for check_run in check_runs:
        if check_run["conclusion"] != "success":
            all_passed = False
            print(f"Test '{check_run['name']}' failed.")
            break

    if all_passed:
        print("All tests are passing.")
    else:
        print("Some tests are failing.")

if __name__ == "__main__":
    your_username = os.getenv('GITHUB_USERNAME')
    your_token = os.getenv('GITHUB_TOKEN')
    owner = os.getenv('GITHUB_OWNER')
    repo_name = os.getenv('GITHUB_REPO')
    get_latest_commit_status(your_username, your_token, owner, repo_name)
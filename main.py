"""
Communicate with CD Runner

- ask for app-deploy
- poll for job-status until it is:
  - "success" (exit code 0)
  - "error" (exit code 1)
- abort if it takes longer than timeout (exit code 2)
"""

import argparse
import os
import requests
import signal
import sys
import time

CD_URLS = {
    "test": "https://enac-test-cd-runner.epfl.ch",
    "prod": "https://enac-prod-cd-runner.epfl.ch",
}
DEPLOYMENT_SECRET = os.environ.get("ENAC_IT4R_CD_deployment_secret")

# Read arguments
parser = argparse.ArgumentParser(prog="main", description="CD app-deploy client")
parser.add_argument(
    "--env", type=str, help="environment", required=True, choices=["test", "prod"]
)
parser.add_argument("--deployment-id", type=str, help="deployment id", required=True)
parser.add_argument(
    "--interval", type=int, help="polling interval in seconds", default=5
)
parser.add_argument(
    "--timeout", type=int, help="timeout before giving up in seconds", default=240
)
args = parser.parse_args()

ROOT_URL = CD_URLS[args.env]


# Manage timeout
def process_took_too_long(signum, frame):
    print(
        f"!! Timeout Error: Process took longer than {args.timeout} seconds, exiting."
    )
    sys.exit(2)


signal.signal(signal.SIGALRM, process_took_too_long)
signal.alarm(args.timeout)


def talk_to_cd(action, json):
    r = requests.post(
        f"{ROOT_URL}/{action}/",
        json=json,
    )
    if r.status_code != 200:
        print(f"! Error: failed to ask for {action}: {r.status_code=} {r.text=}")
        sys.exit(1)
    return r.json()


class Output:
    def __init__(self):
        self.output_already_printed = ""

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def print(self, output):
        new_output = output[len(self.output_already_printed) :]
        print(new_output, end="")
        self.output_already_printed = output


# Start the story
print(f"-> Asking for app-deploy of {args.deployment_id} on {ROOT_URL}!")
response = talk_to_cd(
    action="app-deploy",
    json={"deployment_id": args.deployment_id, "deployment_secret": DEPLOYMENT_SECRET},
)
if response["status"] == "error":
    print(f"! Error: App deploy failed! {response['error']}")
    sys.exit(1)
job_id = response["job_id"]

with Output() as output:
    while True:
        response = talk_to_cd(
            action="job-status",
            json={
                "deployment_id": args.deployment_id,
                "deployment_secret": DEPLOYMENT_SECRET,
                "job_id": job_id,
            },
        )
        output.print(response["output"])
        if response["status"] == "error":
            print("! Error: App deploy failed!")
            sys.exit(1)
        if response["status"] == "success":
            print("-> App deploy finished successfully!")
            break
        time.sleep(args.interval)

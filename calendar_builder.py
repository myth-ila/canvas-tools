# Canvas Calendar Builder - Creates calendar events and assignments on Canvas LMS from a CSV file
# Author: Mithila Hegde
# Version: 1.0
# Date: July 2025

import pandas as pd
import requests
import os
from datetime import datetime

# ---- CONFIGURE YOUR API ACCESS TOKEN ----
# See README file for instructions on how to generate your ACCESS TOKEN on Canvas

# Option 1: Store your token in a file called "canvas_token.txt" in the same folder
#            (just paste the token as the only line in the file)
# Option 2: Paste your token directly below where indicated

TOKEN_FILE = "canvas_token.txt"
ACCESS_TOKEN = ""  # Leave this blank, it is only initialising the variable

# Checks for Option 1: Read from file
if os.path.exists(TOKEN_FILE):
    with open(TOKEN_FILE, "r") as f:
        ACCESS_TOKEN = f.read().strip()
    print(f"Token loaded from {TOKEN_FILE}")

# Checks for Option 2: If no file found, use the token pasted below
if not ACCESS_TOKEN:
    ACCESS_TOKEN = ""  # <-- PASTE YOUR TOKEN HERE, BETWEEN THE QUOTES

# Check that a token was provided through either option
if not ACCESS_TOKEN:
    print(" No API token found!")
    print("   Option 1: Create a file called 'canvas_token.txt' with your token in it.")
    print("   Option 2: Paste your token into the ACCESS_TOKEN variable in the script.")
    print("   See README for instructions on how to generate it and set up here.")
    exit()

# ---- CANVAS SETTINGS ----
# Update these to match your institution and course
BASE_URL = "https://your-institution.instructure.com"  # e.g., https://canvas.university.edu
COURSE_ID = 0  # Find this in your Canvas course URL: /courses/XXXXXX

# ---- CALENDAR EVENT SETTINGS ----
TIMEZONE = "America/New_York"            # Timezone for event times (IANA format)
LOCATION_NAME = "Zoom"                   # Default location name for calendar events
ZOOM_LINK = ""                           # Your Zoom/meeting link (leave blank if not needed)

# ---- FILE PATH ----
CSV_PATH = "canvas_events.csv"  # Path to your CSV file; see README for required columns

# ---------------------------------------------------------------------------
# ---- YOU DO NOT NEED TO SET UP ANYTHING IN THE CODE FROM THIS POINT ON ----
# ---------------------------------------------------------------------------

# ---- HEADERS ----
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

# ---- FUNCTIONS ----

def iso_datetime(date_str, time_str):
    """Convert a date string and time string to ISO 8601 format.

    Args:
        date_str: Date in YYYY-MM-DD format (e.g., "2025-09-01")
        time_str: Time in HH:MM format (e.g., "09:45")
    """
    dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    return dt.isoformat()


def create_assignment(title, start_time, end_time):
    """Create a graded assignment on Canvas."""
    assignment_data = {
        "assignment": {
            "name": title,
            "description": f"{title} assignment",
            "due_at": end_time,
            "lock_at": end_time,
            "unlock_at": start_time,
            "published": True
        }
    }
    response = requests.post(
        f"{BASE_URL}/api/v1/courses/{COURSE_ID}/assignments",
        headers=HEADERS,
        json=assignment_data
    )
    return response


def create_calendar_event(title, start_time, end_time):
    """Create a calendar event on Canvas."""
    description = f"Class on Zoom: {ZOOM_LINK}" if ZOOM_LINK else title
    event_data = {
        "calendar_event": {
            "context_code": f"course_{COURSE_ID}",
            "title": title,
            "description": description,
            "location_name": LOCATION_NAME,
            "start_at": start_time,
            "end_at": end_time,
            "time_zone": TIMEZONE
        }
    }
    response = requests.post(
        f"{BASE_URL}/api/v1/calendar_events",
        headers=HEADERS,
        json=event_data
    )
    return response


def process_events(df):
    """Loop through the CSV rows and create each event or assignment on Canvas."""
    created = 0
    failed = 0

    for _, row in df.iterrows():
        title = str(row["title"])
        event_type = str(row["type"]).strip().lower()
        start_time = iso_datetime(row["date"], str(row["start_time"]).strip())
        end_time = iso_datetime(row["date"], str(row["end_time"]).strip())

        if event_type == "assignment":
            response = create_assignment(title, start_time, end_time)
        else:
            response = create_calendar_event(title, start_time, end_time)

        if response.status_code in [200, 201]:
            print(f"Created: {title}")
            created += 1
        else:
            print(f"Failed: {title} - {response.status_code}")
            print(f"{response.text}")
            failed += 1

    return created, failed


# ---- CALL FUNCTIONS ----
if __name__ == "__main__":
    print(f"Reading events from {CSV_PATH}...")
    df = pd.read_csv(CSV_PATH)
    print(f"   Found {len(df)} events\n")

    created, failed = process_events(df)

    print(f"\n Done! {created} events created, {failed} failed.")
    print(f"View your course at: {BASE_URL}/courses/{COURSE_ID}")
# Canvas Quiz Builder - Creates quizzes on Canvas LMS from an Excel spreadsheet
# Author: Mithila Hegde
# Version: 1.0
# Date: July 2025

import pandas as pd
import requests
import os

# ---- CONFIGURE YOUR API ACCESS TOKEN ----
#See Readme file for instructions on how to generate your ACCESS TOKEN on Canvas
# Option 1: Store your token in a file called "canvas_token.txt" in the same folder
#            (just paste the token as the only line in the file)
# Option 2: Paste your token directly below where indicated 

TOKEN_FILE = "canvas_token.txt"
ACCESS_TOKEN = "" #Leave this blank, it is only initialising the variable

# Try Option 1: Read from file
if os.path.exists(TOKEN_FILE):
    with open(TOKEN_FILE, "r") as f:
        ACCESS_TOKEN = f.read().strip()
    print(f"Token loaded from {TOKEN_FILE}")

# Option 2: If no file found, use the token pasted below
if not ACCESS_TOKEN:
    ACCESS_TOKEN = ""  # <-- PASTE YOUR TAKEN HERE, BETWEEN THE QUOTES

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

# ---- QUIZ SETTINGS ----
QUIZ_TITLE = "My Quiz"
QUIZ_DESCRIPTION = "Quiz created via Canvas API."
QUIZ_TYPE = "assignment"            # "assignment" (graded) or "practice_quiz" or "survey"
TIME_LIMIT = 30                     # Minutes (set to None for no limit)
SHUFFLE_ANSWERS = True              # Set to False if you don't want options to be shuffled 
HIDE_RESULTS = "always"             # "always", "until_after_last_attempt", or None
ALLOWED_ATTEMPTS = 1                # -1 for unlimited attempts
DUE_DATE = "2025-07-08T23:59:00Z"  # ISO 8601 format in UTC
PUBLISHED = False                   # Set to True to publish immediately; if you set to False you can verify if it has set up correctly on Canvas and then publish it

# ---- FILE PATH ----
EXCEL_PATH = "quiz_questions.xlsx"  # Path to your Excel file; see README for required columns

# ---------------------------------------------------------------------------
# ---- YOU DO NOT NEED TO SET UP ANYTHING IN THE CODE THIS POINT ONWARDS ----
# ---------------------------------------------------------------------------


# ---- HEADERS ----
HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

# ---- FUNCTIONS ----

def create_quiz():
    """Create an empty new quiz on Canvas and return its ID."""
    quiz_payload = {
        "quiz": {
            "title": QUIZ_TITLE,
            "description": QUIZ_DESCRIPTION,
            "quiz_type": QUIZ_TYPE,
            "published": PUBLISHED,
            "due_at": DUE_DATE,
            "time_limit": TIME_LIMIT,
            "shuffle_answers": SHUFFLE_ANSWERS,
            "hide_results": HIDE_RESULTS,
            "allowed_attempts": ALLOWED_ATTEMPTS
        }
    }

    response = requests.post(
        f"{BASE_URL}/api/v1/courses/{COURSE_ID}/quizzes",
        headers=HEADERS,
        json=quiz_payload
    )

    if response.status_code not in [200, 201]:
        print(" Failed to create quiz")
        print(response.text)
        exit()

    quiz_id = response.json()["id"]
    print(f" Quiz created with ID {quiz_id}")
    return quiz_id


def add_questions(quiz_id, df):
    """Add all questions from the DataFrame to the quiz."""
    for i, row in df.iterrows():                                                #Sets up question level properties in a format the API can understand
        question_data = {
            "question": {
                "question_name": str(row["question_name"]),
                "question_text": str(row["question_text"]),
                "question_type": row["question_type"],
                "points_possible": float(row["points_possible"]),
                "answers": []
            }
        }

        # Loop over answer columns (supports up to 15 answers)
        for j in range(1, 16):                                                 #Sets up each answer option along with it's corresponding weight. This is done for each question
            answer_col = f"answer_{j}"
            weight_col = f"weight_{j}"
            if pd.notna(row.get(answer_col)) and pd.notna(row.get(weight_col)):
                question_data["question"]["answers"].append({
                    "text": str(row[answer_col]),
                    "weight": float(row[weight_col])
                })

        response = requests.post(
            f"{BASE_URL}/api/v1/courses/{COURSE_ID}/quizzes/{quiz_id}/questions", #Gives the information set up above to the API endpoint relevant to adding questions to a quiz
            headers=HEADERS,
            json=question_data
        )

        if response.status_code in [200, 201]:                                  
            print(f"   Added question: {row['question_name']}")
        else:
            print(f"   Failed to add question: {row['question_name']}")
            print(f"     {response.text}")

# ---- CALL FUNCTIONS ----
if __name__ == "__main__":
    print(f"📖 Reading questions from {EXCEL_PATH}...")
    df = pd.read_excel(EXCEL_PATH)
    print(f"   Found {len(df)} questions\n")                                   

    quiz_id = create_quiz()
    add_questions(quiz_id, df)

    print(f"\n Done! {len(df)} questions added to quiz {quiz_id}")
    print(f"   View it at: {BASE_URL}/courses/{COURSE_ID}/quizzes/{quiz_id}")
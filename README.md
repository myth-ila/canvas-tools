# Canvas Tools

A collection of Python tools for automating tasks on 
[Canvas LMS](https://www.instructure.com/canvas) using its REST API.

> **Status:** This repository currently contains the Quiz Builder tool. 
> More Canvas automation tools will be added over time.

## Tools

### 1. Quiz Builder (`quiz_builder.py`)

Creates a quiz on Canvas from an Excel spreadsheet. Define your questions, 
answer choices, and correct answers in Excel, and the script uploads 
everything to Canvas automatically.

## Motivation

Setting up a multiple-choice quiz on Canvas is surprisingly tedious. Each 
question requires multiple clicks — you have to type the question, add each 
answer option one by one, mark the correct answer, set the point value, and 
repeat for every single question. For a 40-question quiz, this becomes a 
time-consuming and error-prone process.

This tool simplifies it: you set up your questions in an Excel spreadsheet 
(one row per question, columns for answers and correct/incorrect weights), 
run the script, and the quiz appears on Canvas, fully configured.

The code and API setup is a **one-time effort**. Once configured, creating 
future quizzes only requires preparing a new Excel file and running the 
script again.

## Getting Started

### Prerequisites

- Python 3.7+
- A Canvas LMS account with API access
- A Canvas API token

### Installation

Install the required Python libraries:

```bash
pip install pandas requests openpyxl
```

### Getting Your Canvas API Token
1. Log in to Canvas
1. Go to Account → Settings
1. Scroll to Approved Integrations
1. Click + New Access Token
1. Give it a name (e.g., "Quiz Builder") and click Generate Token
1. Copy the token — you won't be able to see it again

### Setting Your Token
**Option 1 (Recommended): Token file**

Create a file called `canvas_token.txt` in the same folder as the script. 
Paste your token as the only line in the file. The script will read it 
automatically.

> This file is listed in `.gitignore` so it will never be uploaded to GitHub.

**Option 2: Paste directly in the script**

Open `quiz_builder.py` and replace `PASTE_YOUR_TOKEN_HERE` with your token:

```python
ACCESS_TOKEN = "your_actual_token_here"
```
> ***If you use this option, be careful never to share the script with anyone with your token in it.***

## Quiz Builder Usage

### 1. Prepare Your Excel File

Create an Excel file (.xlsx) with the following columns:

| Column | Description | Example |
|---|---|---|
| `question_name` | Short label for the question | `Q1` |
| `question_text` | The full question text | `What is the marketing mix?` |
| `question_type` | Canvas question type | `multiple_choice_question` |
| `points_possible` | Point value | `2` |
| `answer_1` | First answer choice | `Product, Price, Place, Promotion` |
| `weight_1` | Weight (100 = correct, 0 = incorrect) | `100` |
| `answer_2` | Second answer choice | `People, Process, Plan, Profit` |
| `weight_2` | Weight | `0` |
|... | Up to `answer_15` / `weight_15` |... |

Supported question types:

- `multiple_choice_question`
- `true_false_question`
- `short_answer_question`
- `essay_question`

### 2. Configure the Script

Open `quiz_builder.py` and update the Canvas settings here:

```python
BASE_URL = "https://your-institution.instructure.com"
COURSE_ID = 1234567  # From your Canvas course URL
```

Update the quiz settings as needed:

```python
QUIZ_TITLE = "Midterm Exam"
TIME_LIMIT = 60
ALLOWED_ATTEMPTS = 1
DUE_DATE = "2025-12-15T23:59:00Z"
```
(Comments in the code explain the options for each variable; for further reference take a look at Canvas API documentation linked below)

### 3. Run the Script

```bash
python quiz_builder.py
```

## Example Output

```
 Reading questions from quiz_questions.xlsx...
   Found 40 questions

 Quiz created with ID 7654321
   Added question: Q1
   Added question: Q2...
   Added question: Q40

 Done! 40 questions added to quiz 7654321
   View it at: https://your-institution.instructure.com/courses/1234567/quizzes/7654321
```

### 4. Use the time and mental effort you saved elsewhere! (Maybe research?)

## Canvas API Documentation

This tool uses the Canvas LMS REST API. For further reference on quiz 
settings, question types, and other API capabilities:

- [Canvas REST API — Quizzes](https://canvas.instructure.com/doc/api/quizzes.html) — Creating and managing quizzes
- [Canvas REST API — Quiz Questions](https://canvas.instructure.com/doc/api/quiz_questions.html) — Adding and editing quiz questions
- [Canvas API — Getting Started](https://canvas.instructure.com/doc/api/) — Overview and authentication guide

> **Note:** Canvas is transitioning its API documentation to the 
> [Instructure Developer Documentation Portal](https://developerdocs.instructure.com/services/canvas). 
> The older URLs above will redirect after July 1, 2026.
> If this code doesn't work due to changes in the API please reach out to me at mithila(at)business.unc.edu and I will try to help.

## Development Process
These tools were developed for author's use while teaching at UNC Kenan-Flagler Business School.

## License
MIT License — feel free to use, modify, and distribute.


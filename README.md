# MAFA Chemistry Attendance Analytics

A Streamlit dashboard that parses an institution/student text dataset into a pandas DataFrame and presents attendance-oriented summary metrics and Plotly visualizations.

## Features
- Converts institution headings and hyphen-prefixed student entries into structured records.
- Calculates total student records and distinct institutions.
- Summarizes institution-level counts.
- Displays interactive visualizations.

## Stack
Python, Streamlit, pandas, Plotly.

## Setup
```bash
git clone https://github.com/nyohleonard-nlktech/mafa-chemistry-attendance.git
cd mafa-chemistry-attendance
python -m venv .venv
```

Activate:
```bash
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install and run:
```bash
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit (normally http://localhost:8501).

## Data format
The current parser treats non-bulleted lines as institution names and hyphen-prefixed lines as student names. Preserve this format when replacing the source data, or update load_and_normalize_data() and add tests.

## Structure
```text
app.py
requirements.txt
README.md
```

Attendance data can identify learners. Use only authorized data and anonymize records in public demos. No license file is present; all rights reserved unless an explicit license is added.

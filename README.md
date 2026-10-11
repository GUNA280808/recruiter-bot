# Build-a-Recruiter-Bot

A Python backend API that ranks candidates against job openings using skill overlap, experience, availability, and culture-keyword matching. It returns ranked results with component scores and explanations.

## Technology Stack

- Python 3.11
- FastAPI
- Uvicorn
- SQLite
- Built-in Python `sqlite3`
- Pytest-style test functions using Python assertions

## Features

- Stores candidates, jobs, candidate skills, and job-required skills in SQLite.
- Calculates a weighted match score for every candidate–job pair.
- Returns matched and missing skills.
- Provides explanations for each match.
- Ranks candidates for a job and jobs for a candidate.
- Handles invalid IDs with HTTP 404 responses.
- Uses parameterized SQL queries and foreign-key constraints.
- Includes tests for scoring, ranking, and edge cases.

## Matching Algorithm

The total score is calculated using these weights:

- Skills: 50%
- Experience: 25%
- Availability: 15%
- Culture keywords: 10%

### Skill score

The score is the percentage of required skills possessed by the candidate. Matching is case-insensitive.

### Experience score

- If the minimum experience is zero, the score is 100.
- If the candidate has less experience than required, the score is `70 × candidate experience / minimum experience`.
- If the candidate meets the minimum, the score starts at 70 and increases by 5 for each additional year, capped at 100.

### Availability score

- Immediate: 100
- 2 weeks: 70
- Not looking: 0

### Culture score

The score is the percentage of job culture keywords matched by the candidate's listed traits.

The component scores are combined using the weights above. Candidates are ranked by total score, followed by skill score, availability score, and ID to provide deterministic tie-breaking.

The minimum experience requirement affects the score rather than automatically excluding a candidate. This allows the API to surface potentially suitable candidates while clearly indicating experience gaps.

## Project Structure

```text
build-a-recruiter-bot/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── matching.py
│   └── main.py
├── scripts/
│   └── seed_data.py
├── tests/
│   └── test_matching.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

Python 3.11 is recommended.

Create and activate a virtual environment on Windows:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Load the sample dataset:

```powershell
python -m scripts.seed_data
```

Run the API:

```powershell
python -m uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` to explore and execute the endpoints interactively.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Check the API welcome response |
| GET | `/health` | Check API health |
| GET | `/jobs/{job_id}/matches` | Rank candidates for a job |
| GET | `/candidates/{candidate_id}/matches` | Rank jobs for a candidate |

Example requests:

```text
GET /jobs/1/matches
GET /candidates/1/matches
```

Invalid job or candidate IDs return HTTP 404.

## Run Tests

```powershell
python -m tests.test_matching
```

The test suite covers skill overlap, experience scoring, availability, culture matching, ranked results, invalid IDs, edge cases, deterministic ranking, and match explanations.

## Design Decisions and Trade-offs

- SQLite keeps setup simple and requires no separate database server.
- Built-in `sqlite3` and handwritten parameterized SQL keep database interactions explicit and avoid an ORM.
- Separate scoring functions make the matching logic easier to test and maintain.
- Weighted scoring makes the ranking understandable, but the weights are initial design choices and should be calibrated against recruiter feedback and real hiring outcomes.
- Culture keywords are a simple proxy, not an objective measure of personality or job performance.
- The results support recruiter decision-making; they should not be treated as an automatic hiring decision.

## Limitations

- Skill and culture matching use exact normalized keyword matches rather than semantic similarity.
- Availability categories are predefined.
- Scores depend on the quality and completeness of the supplied data.
- The sample dataset is illustrative and does not establish real-world hiring accuracy.

## Future Improvements

- Add API integration tests.
- Add pagination and filtering for larger datasets.
- Calibrate weights using validated hiring outcomes.
- Add structured request/response schemas.
- Add authentication and access controls before production deployment.


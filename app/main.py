
from fastapi import FastAPI, HTTPException

from app.database import create_tables
from app.matching import get_job_matches, get_candidate_matches


app = FastAPI(
    title="Build-a-Recruiter-Bot",
    description="A backend API for matching candidates with jobs.",
    version="1.0.0",
)


@app.on_event("startup")
def initialize_database():
    """Ensure database tables exist when the application starts."""
    create_tables()


@app.get("/")
def home():
    return {
        "message": "Build-a-Recruiter-Bot API is running!",
        "status": "success",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/jobs/{job_id}/matches")
def matches_for_job(job_id: int):
    """Return candidates ranked for a particular job."""
    result = get_job_matches(job_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"Job with ID {job_id} not found",
        )

    return result


@app.get("/candidates/{candidate_id}/matches")
def matches_for_candidate(candidate_id: int):
    """Return jobs ranked for a particular candidate."""
    result = get_candidate_matches(candidate_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"Candidate with ID {candidate_id} not found",
        )

    return result

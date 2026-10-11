
from app.database import get_connection


WEIGHTS = {
    "skills": 0.50,
    "experience": 0.25,
    "availability": 0.15,
    "culture": 0.10,
}


AVAILABILITY_SCORES = {
    "immediate": 100,
    "2 weeks": 70,
    "not looking": 0,
}


def normalize(value):
    """Normalize text for consistent, case-insensitive comparisons."""
    return value.strip().casefold()


def parse_keywords(value):
    """Convert comma-separated text into normalized keywords."""
    if not value:
        return set()

    return {
        normalize(item)
        for item in value.split(",")
        if item.strip()
    }


def calculate_skill_score(candidate_skills, required_skills):
    """Return skill score, matched skills, and missing skills."""
    candidate_skills = {
        normalize(skill) for skill in candidate_skills
    }
    required_skills = {
        normalize(skill) for skill in required_skills
    }

    if not required_skills:
        return 100.0, [], []

    matched = sorted(candidate_skills & required_skills)
    missing = sorted(required_skills - candidate_skills)

    score = len(matched) / len(required_skills) * 100

    return score, matched, missing


def calculate_experience_score(experience, minimum):
    """Score experience without allowing unlimited bonus points."""
    if minimum <= 0:
        return 100.0

    if experience < minimum:
        # Below-minimum experience earns a proportional score,
        # reaching 70 when the minimum is met.
        return 70.0 * experience / minimum

    # Meeting the minimum earns 70; extra experience adds
    # five points per year, capped at 100.
    return min(100.0, 70.0 + 5.0 * (experience - minimum))


def calculate_availability_score(availability):
    """Return the availability score for the supplied category."""
    return AVAILABILITY_SCORES.get(
        normalize(availability), 0
    )


def calculate_culture_score(traits, culture_keywords):
    """Compare explicitly listed traits with job culture keywords."""
    candidate_traits = parse_keywords(traits)
    job_keywords = parse_keywords(culture_keywords)

    if not job_keywords:
        return 100.0, [], []

    matched = sorted(candidate_traits & job_keywords)
    missing = sorted(job_keywords - candidate_traits)

    score = len(matched) / len(job_keywords) * 100

    return score, matched, missing


def calculate_total_score(
    skill_score,
    experience_score,
    availability_score,
    culture_score,
):
    """Combine the component scores using the defined weights."""
    return (
        skill_score * WEIGHTS["skills"]
        + experience_score * WEIGHTS["experience"]
        + availability_score * WEIGHTS["availability"]
        + culture_score * WEIGHTS["culture"]
    )


def get_candidate_skills(connection, candidate_id):
    rows = connection.execute(
        """
        SELECT skill
        FROM candidate_skills
        WHERE candidate_id = ?
        ORDER BY skill
        """,
        (candidate_id,),
    ).fetchall()

    return [row["skill"] for row in rows]


def get_job_skills(connection, job_id):
    rows = connection.execute(
        """
        SELECT skill
        FROM job_required_skills
        WHERE job_id = ?
        ORDER BY skill
        """,
        (job_id,),
    ).fetchall()

    return [row["skill"] for row in rows]


def score_candidate_for_job(connection, candidate, job):
    """Calculate a candidate's suitability for one job."""
    candidate_skills = get_candidate_skills(
        connection, candidate["id"]
    )
    required_skills = get_job_skills(
        connection, job["id"]
    )

    skill_score, matched_skills, missing_skills = (
        calculate_skill_score(candidate_skills, required_skills)
    )

    experience_score = calculate_experience_score(
        candidate["experience"],
        job["min_experience"],
    )

    availability_score = calculate_availability_score(
        candidate["availability"]
    )

    culture_score, matched_traits, missing_traits = (
        calculate_culture_score(
            candidate["traits"],
            job["culture_keywords"],
        )
    )

    total_score = calculate_total_score(
        skill_score,
        experience_score,
        availability_score,
        culture_score,
    )

    reasons = []

    if matched_skills:
        reasons.append(
            "Matches required skills: "
            + ", ".join(matched_skills)
        )

    if missing_skills:
        reasons.append(
            "Missing required skills: "
            + ", ".join(missing_skills)
        )

    if candidate["experience"] >= job["min_experience"]:
        reasons.append(
            "Meets the minimum experience requirement"
        )
    else:
        reasons.append(
            f"Below the minimum experience requirement "
            f"({candidate['experience']} years; "
            f"{job['min_experience']} required)"
        )

    if normalize(candidate["availability"]) == "not looking":
        reasons.append("Candidate is currently not looking")
    elif normalize(candidate["availability"]) == "immediate":
        reasons.append("Candidate is available immediately")
    else:
        reasons.append(
            f"Availability: {candidate['availability']}"
        )

    if matched_traits:
        reasons.append(
            "Matching culture keywords: "
            + ", ".join(matched_traits)
        )

    return {
        "candidate_id": candidate["id"],
        "candidate_name": candidate["name"],
        "job_id": job["id"],
        "job_title": job["title"],
        "score": round(total_score, 2),
        "component_scores": {
            "skills": round(skill_score, 2),
            "experience": round(experience_score, 2),
            "availability": round(availability_score, 2),
            "culture": round(culture_score, 2),
        },
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "matched_culture_keywords": matched_traits,
        "missing_culture_keywords": missing_traits,
        "reason": "; ".join(reasons),
    }


def get_job_matches(job_id):
    """Rank candidates for a particular job."""
    with get_connection() as connection:
        job = connection.execute(
            "SELECT * FROM jobs WHERE id = ?",
            (job_id,),
        ).fetchone()

        if job is None:
            return None

        candidates = connection.execute(
            "SELECT * FROM candidates ORDER BY id"
        ).fetchall()

        matches = [
            score_candidate_for_job(connection, candidate, job)
            for candidate in candidates
        ]

        matches.sort(
            key=lambda match: (
                -match["score"],
                -match["component_scores"]["skills"],
                -match["component_scores"]["availability"],
                match["candidate_id"],
            )
        )

        return {
            "job_id": job["id"],
            "job_title": job["title"],
            "matches": matches,
        }


def get_candidate_matches(candidate_id):
    """Rank jobs for a particular candidate."""
    with get_connection() as connection:
        candidate = connection.execute(
            "SELECT * FROM candidates WHERE id = ?",
            (candidate_id,),
        ).fetchone()

        if candidate is None:
            return None

        jobs = connection.execute(
            "SELECT * FROM jobs ORDER BY id"
        ).fetchall()

        matches = [
            score_candidate_for_job(connection, candidate, job)
            for job in jobs
        ]

        matches.sort(
            key=lambda match: (
                -match["score"],
                -match["component_scores"]["skills"],
                -match["component_scores"]["availability"],
                match["job_id"],
            )
        )

        return {
            "candidate_id": candidate["id"],
            "candidate_name": candidate["name"],
            "matches": [
                {
                    "job_id": match["job_id"],
                    "job_title": match["job_title"],
                    "score": match["score"],
                    "component_scores": match["component_scores"],
                    "matched_skills": match["matched_skills"],
                    "missing_skills": match["missing_skills"],
                    "reason": match["reason"],
                }
                for match in matches
            ],
        }

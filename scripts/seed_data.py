
from app.database import get_connection, create_tables


CANDIDATES = [
    {
        "name": "Sherlock H.",
        "skills": ["deduction", "pattern-recognition", "forensics"],
        "experience": 8,
        "availability": "Immediate",
        "traits": "analytical, blunt",
        "quirk": (
            "Solves problems by eliminating the impossible; "
            "occasionally insufferable in standups."
        ),
    },
    {
        "name": "Hermione G.",
        "skills": ["research", "time-management", "public-speaking"],
        "experience": 4,
        "availability": "2 weeks",
        "traits": "detail-oriented, overachiever",
        "quirk": (
            "Reads the entire documentation before writing "
            "a single line of code."
        ),
    },
    {
        "name": "Tony S.",
        "skills": ["systems-design", "rapid-prototyping", "leadership"],
        "experience": 12,
        "availability": "Not looking",
        "traits": "confident, innovative",
        "quirk": "Ships an MVP overnight, refuses to write tests.",
    },
    {
        "name": "Leslie K.",
        "skills": [
            "project-management",
            "stakeholder-management",
            "public-speaking",
        ],
        "experience": 6,
        "availability": "Immediate",
        "traits": "tenacious, organized",
        "quirk": "Has a binder for everything, including the binder.",
    },
    {
        "name": "Ron S.",
        "skills": ["woodworking", "minimalism", "negotiation"],
        "experience": 15,
        "availability": "Not looking",
        "traits": "stubborn, principled",
        "quirk": "Refuses to use more than one monitor.",
    },
    {
        "name": "Rick S.",
        "skills": ["systems-design", "rapid-prototyping", "chemistry"],
        "experience": 20,
        "availability": "Immediate",
        "traits": "genius, reckless",
        "quirk": "Solution works, mechanism deeply concerning.",
    },
    {
        "name": "Elle W.",
        "skills": ["persuasion", "research", "public-speaking"],
        "experience": 3,
        "availability": "Immediate",
        "traits": "optimistic, sharp",
        "quirk": "Underestimated in every standup, correct in every retro.",
    },
    {
        "name": "MacGyver",
        "skills": [
            "rapid-prototyping",
            "resourcefulness",
            "chemistry",
            "systems-design",
        ],
        "experience": 10,
        "availability": "2 weeks",
        "traits": "calm, improviser",
        "quirk": "Fixes production outages with duct tape and a paperclip metaphor.",
    },
    {
        "name": "Sheldon C.",
        "skills": [
            "theoretical-analysis",
            "pattern-recognition",
            "research",
        ],
        "experience": 9,
        "availability": "Immediate",
        "traits": "rigid, brilliant",
        "quirk": "Correct 95% of the time. Insufferable 100% of the time.",
    },
    {
        "name": "Katniss E.",
        "skills": ["precision", "strategy", "crisis-management"],
        "experience": 5,
        "availability": "Immediate",
        "traits": "resilient, decisive",
        "quirk": "Excellent under pressure, terrible with public speaking.",
    },
    {
        "name": "Michael S.",
        "skills": ["sales", "public-speaking", "team-building"],
        "experience": 11,
        "availability": "Not looking",
        "traits": "enthusiastic, chaotic",
        "quirk": "World's best boss, according to a mug he bought himself.",
    },
    {
        "name": "Olivia P.",
        "skills": [
            "crisis-management",
            "negotiation",
            "strategy",
            "leadership",
        ],
        "experience": 13,
        "availability": "2 weeks",
        "traits": "decisive, intense",
        "quirk": "Handles it. Whatever it is.",
    },
    {
        "name": "Ted L.",
        "skills": [
            "team-building",
            "optimism",
            "mentorship",
            "public-speaking",
        ],
        "experience": 7,
        "availability": "Immediate",
        "traits": "empathetic, persistent",
        "quirk": "Turns every technical setback into a folksy metaphor.",
    },
    {
        "name": "Miranda P.",
        "skills": [
            "leadership",
            "negotiation",
            "stakeholder-management",
            "precision",
        ],
        "experience": 18,
        "availability": "Not looking",
        "traits": "demanding, decisive",
        "quirk": "Reviews every PR personally. Says nothing. Everyone panics.",
    },
    {
        "name": "Dwight S.",
        "skills": ["sales", "negotiation", "security", "loyalty"],
        "experience": 9,
        "availability": "Immediate",
        "traits": "intense, loyal",
        "quirk": "Assistant to the regional backend engineer.",
    },
]


JOBS = [
    {
        "title": "Backend Detective",
        "required_skills": [
            "deduction",
            "pattern-recognition",
            "forensics",
        ],
        "min_experience": 3,
        "culture_keywords": "analytical, autonomous",
        "tagline": "We have a bug. We have no leads. We have you.",
    },
    {
        "title": "Rapid Prototyping Engineer",
        "required_skills": ["rapid-prototyping", "systems-design"],
        "min_experience": 2,
        "culture_keywords": "innovative, fast-paced",
        "tagline": "Ship first, document never (kidding — please document).",
    },
    {
        "title": "Developer Relations Lead",
        "required_skills": ["public-speaking", "research"],
        "min_experience": 2,
        "culture_keywords": "energetic, curious",
        "tagline": "Explain complex things to confused humans, cheerfully.",
    },
    {
        "title": "Engineering Manager, Chaos Team",
        "required_skills": [
            "team-building",
            "stakeholder-management",
            "leadership",
        ],
        "min_experience": 5,
        "culture_keywords": "empathetic, organized",
        "tagline": "Herd cats. The cats are senior engineers.",
    },
    {
        "title": "Incident Commander",
        "required_skills": [
            "crisis-management",
            "strategy",
            "negotiation",
        ],
        "min_experience": 4,
        "culture_keywords": "decisive, calm-under-pressure",
        "tagline": "3am page. You're the one who picks up.",
    },
    {
        "title": "Sales Engineer",
        "required_skills": ["sales", "public-speaking", "negotiation"],
        "min_experience": 3,
        "culture_keywords": "enthusiastic, persistent",
        "tagline": "Sell the vision, then go build it.",
    },
]


def seed_database():
    create_tables()
    connection = get_connection()

    try:
        with connection:
            # Reset only the four assignment tables.
            connection.execute("DELETE FROM candidate_skills")
            connection.execute("DELETE FROM job_required_skills")
            connection.execute("DELETE FROM candidates")
            connection.execute("DELETE FROM jobs")

            for candidate_id, candidate in enumerate(CANDIDATES, start=1):
                connection.execute(
                    """
                    INSERT INTO candidates
                    (id, name, experience, availability, traits, quirk)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        candidate_id,
                        candidate["name"],
                        candidate["experience"],
                        candidate["availability"],
                        candidate["traits"],
                        candidate["quirk"],
                    ),
                )

                connection.executemany(
                    """
                    INSERT INTO candidate_skills (candidate_id, skill)
                    VALUES (?, ?)
                    """,
                    [
                        (candidate_id, skill)
                        for skill in candidate["skills"]
                    ],
                )

            for job_id, job in enumerate(JOBS, start=1):
                connection.execute(
                    """
                    INSERT INTO jobs
                    (id, title, min_experience, culture_keywords, tagline)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        job_id,
                        job["title"],
                        job["min_experience"],
                        job["culture_keywords"],
                        job["tagline"],
                    ),
                )

                connection.executemany(
                    """
                    INSERT INTO job_required_skills (job_id, skill)
                    VALUES (?, ?)
                    """,
                    [
                        (job_id, skill)
                        for skill in job["required_skills"]
                    ],
                )

        print("Seed data loaded successfully!")

        with connection:
            candidate_count = connection.execute(
                "SELECT COUNT(*) FROM candidates"
            ).fetchone()[0]

            job_count = connection.execute(
                "SELECT COUNT(*) FROM jobs"
            ).fetchone()[0]

            candidate_skill_count = connection.execute(
                "SELECT COUNT(*) FROM candidate_skills"
            ).fetchone()[0]

            job_skill_count = connection.execute(
                "SELECT COUNT(*) FROM job_required_skills"
            ).fetchone()[0]

            print(f"Candidates: {candidate_count}")
            print(f"Jobs: {job_count}")
            print(f"Candidate skill records: {candidate_skill_count}")
            print(f"Job required-skill records: {job_skill_count}")

            print("\nJobs stored:")
            rows = connection.execute(
                "SELECT id, title FROM jobs ORDER BY id"
            ).fetchall()

            for row in rows:
                print(f"{row['id']}. {row['title']}")

            assert candidate_count == 15, "Candidate count mismatch"
            assert job_count == 6, "Job count mismatch"

    finally:
        connection.close()


if __name__ == "__main__":
    seed_database()

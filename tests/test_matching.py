
from app.matching import (
    calculate_skill_score,
    calculate_experience_score,
    calculate_availability_score,
    calculate_culture_score,
    get_job_matches,
    get_candidate_matches,
)


# 1. Test skill overlap and missing skills
def test_skill_score():
    score, matched, missing = calculate_skill_score(
        ["python", "sql"],
        ["python", "sql", "fastapi"],
    )

    assert round(score, 2) == 66.67
    assert matched == ["python", "sql"]
    assert missing == ["fastapi"]


# 2. Test experience scoring rules
def test_experience_score():
    assert round(calculate_experience_score(2, 3), 2) == 46.67
    assert calculate_experience_score(3, 3) == 70
    assert calculate_experience_score(20, 3) == 100


# 3. Test availability categories
def test_availability_score():
    assert calculate_availability_score("Immediate") == 100
    assert calculate_availability_score("2 weeks") == 70
    assert calculate_availability_score("Not looking") == 0


# 4. Test culture keyword matching
def test_culture_score():
    score, matched, missing = calculate_culture_score(
        "analytical, blunt",
        "analytical, autonomous",
    )

    assert score == 50
    assert matched == ["analytical"]
    assert missing == ["autonomous"]


# 5. Test candidates ranked for a job
def test_job_matches():
    result = get_job_matches(1)

    assert result is not None
    assert result["job_title"] == "Backend Detective"
    assert len(result["matches"]) == 15

    sherlock = next(
        match for match in result["matches"]
        if match["candidate_name"] == "Sherlock H."
    )

    assert sherlock["matched_skills"] == [
        "deduction",
        "forensics",
        "pattern-recognition",
    ]

    scores = [match["score"] for match in result["matches"]]
    assert scores == sorted(scores, reverse=True)


# 6. Test jobs ranked for a candidate
def test_candidate_matches():
    result = get_candidate_matches(1)

    assert result is not None
    assert result["candidate_name"] == "Sherlock H."
    assert len(result["matches"]) == 6

    scores = [match["score"] for match in result["matches"]]
    assert scores == sorted(scores, reverse=True)


# 7. Test nonexistent candidate and job IDs
def test_invalid_ids():
    assert get_job_matches(9999) is None
    assert get_candidate_matches(9999) is None


# 8. Edge case: no skill overlap
def test_no_skill_overlap():
    score, matched, missing = calculate_skill_score(
        ["woodworking", "negotiation"],
        ["deduction", "forensics"],
    )

    assert score == 0
    assert matched == []
    assert missing == ["deduction", "forensics"]


# 9. Edge case: job has no required skills
def test_empty_required_skills():
    score, matched, missing = calculate_skill_score(
        ["python"],
        [],
    )

    # Current design: no required skills means no skill mismatch.
    assert score == 100
    assert matched == []
    assert missing == []


# 10. Edge case: experience score stays within 0–100
def test_experience_score_is_bounded():
    for experience in [0, 1, 3, 10, 50]:
        score = calculate_experience_score(experience, 3)
        assert 0 <= score <= 100


# 11. Edge case: repeated requests return the same ranking
def test_ranking_is_deterministic():
    first_result = get_job_matches(1)
    second_result = get_job_matches(1)

    assert first_result is not None
    assert second_result is not None

    first_ranking = [
        (match["candidate_id"], match["score"])
        for match in first_result["matches"]
    ]

    second_ranking = [
        (match["candidate_id"], match["score"])
        for match in second_result["matches"]
    ]

    assert first_ranking == second_ranking


# 12. Edge case: every match has a valid score and explanation
def test_match_explanations_exist():
    result = get_job_matches(1)

    assert result is not None

    for match in result["matches"]:
        assert isinstance(match["reason"], str)
        assert match["reason"].strip() != ""
        assert 0 <= match["score"] <= 100

        assert set(match["component_scores"]) == {
            "skills",
            "experience",
            "availability",
            "culture",
        }


if __name__ == "__main__":
    tests = [
        test_skill_score,
        test_experience_score,
        test_availability_score,
        test_culture_score,
        test_job_matches,
        test_candidate_matches,
        test_invalid_ids,
        test_no_skill_overlap,
        test_empty_required_skills,
        test_experience_score_is_bounded,
        test_ranking_is_deterministic,
        test_match_explanations_exist,
    ]

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print(f"\nAll {len(tests)} matching tests passed!")

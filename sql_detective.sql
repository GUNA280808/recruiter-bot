
-- Q1: List all currently open job postings with their recruiter names
SELECT
    jp.id AS job_id,
    jp.title AS job_title,
    r.name AS recruiter_name
FROM job_postings AS jp
JOIN recruiters AS r
    ON jp.recruiter_id = r.id
WHERE jp.status = 'open'
ORDER BY jp.id;



-- Q2: Count distinct applicants who reached the Final stage for each job
SELECT
    jp.id AS job_id,
    jp.title AS job_title,
    COUNT(DISTINCT i.applicant_id) AS final_stage_applicants
FROM job_postings AS jp
LEFT JOIN interviews AS i
    ON jp.id = i.job_posting_id
    AND i.stage = 'Final'
GROUP BY jp.id, jp.title
ORDER BY jp.id;



-- Q3: Find applicants associated with more than one job
SELECT
    a.id AS applicant_id,
    a.full_name,
    COUNT(DISTINCT i.job_posting_id) AS jobs_applied
FROM applicants AS a
JOIN interviews AS i
    ON a.id = i.applicant_id
GROUP BY a.id, a.full_name
HAVING COUNT(DISTINCT i.job_posting_id) > 1
ORDER BY a.id;



-- Q4: Calculate each recruiter's Final-stage conversion rate
SELECT
    r.id AS recruiter_id,
    r.name AS recruiter_name,
    COUNT(DISTINCT i.applicant_id) AS total_applicants,
    COUNT(DISTINCT CASE
        WHEN i.stage = 'Final' THEN i.applicant_id
    END) AS final_stage_applicants,
    ROUND(
        100.0 * COUNT(DISTINCT CASE
            WHEN i.stage = 'Final' THEN i.applicant_id
        END)
        / NULLIF(COUNT(DISTINCT i.applicant_id), 0),
        2
    ) AS final_conversion_rate
FROM recruiters AS r
LEFT JOIN job_postings AS jp
    ON r.id = jp.recruiter_id
LEFT JOIN interviews AS i
    ON jp.id = i.job_posting_id
GROUP BY r.id, r.name
ORDER BY final_conversion_rate DESC, r.id;



-- Q5: Bonus - Find the most successful recruiter per department
WITH recruiter_stats AS (
    SELECT
        jp.department,
        r.id AS recruiter_id,
        r.name AS recruiter_name,
        COUNT(DISTINCT i.applicant_id) AS total_applicants,
        COUNT(DISTINCT CASE
            WHEN i.stage = 'Final' THEN i.applicant_id
        END) AS final_stage_applicants,
        ROUND(
            100.0 * COUNT(DISTINCT CASE
                WHEN i.stage = 'Final' THEN i.applicant_id
            END)
            / NULLIF(COUNT(DISTINCT i.applicant_id), 0),
            2
        ) AS final_conversion_rate
    FROM recruiters AS r
    JOIN job_postings AS jp
        ON r.id = jp.recruiter_id
    LEFT JOIN interviews AS i
        ON jp.id = i.job_posting_id
    GROUP BY jp.department, r.id, r.name
),
ranked_recruiters AS (
    SELECT
        *,
        RANK() OVER (
            PARTITION BY department
            ORDER BY final_conversion_rate DESC
        ) AS recruiter_rank
    FROM recruiter_stats
)
SELECT
    department,
    recruiter_id,
    recruiter_name,
    total_applicants,
    final_stage_applicants,
    final_conversion_rate
FROM ranked_recruiters
WHERE recruiter_rank = 1
ORDER BY department;

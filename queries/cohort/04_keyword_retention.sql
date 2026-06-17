WITH keyword_cohorts AS (
    SELECT DISTINCT
        keyword,
        toMonday(toStartOfWeek(toDate(event_date))) AS cohort_week
    FROM marketing.ads_data
),
weekly_keyword_activity AS (
    SELECT DISTINCT
        keyword,
        toMonday(toStartOfWeek(toDate(event_date))) AS activity_week
    FROM marketing.ads_data
)
SELECT
    kc.cohort_week,
    kc.keyword,
    count(DISTINCT wka.keyword) AS active_weeks
FROM keyword_cohorts AS kc
LEFT JOIN weekly_keyword_activity AS wka
    ON kc.keyword = wka.keyword
    AND wka.activity_week >= kc.cohort_week
GROUP BY kc.cohort_week, kc.keyword
ORDER BY kc.cohort_week, active_weeks DESC
LIMIT 50
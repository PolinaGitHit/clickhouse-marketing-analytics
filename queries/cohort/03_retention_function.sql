WITH cohorts AS (
    SELECT DISTINCT
        campaign_id,
        campaign_name,
        toMonday(toStartOfWeek(toDate(event_date))) AS cohort_week
    FROM marketing.ads_data
),
weekly_activity AS (
    SELECT DISTINCT
        campaign_id,
        toMonday(toStartOfWeek(toDate(event_date))) AS activity_week
    FROM marketing.ads_data
)
SELECT
    c.cohort_week,
    count(DISTINCT c.campaign_id) AS cohort_size,
    count(DISTINCT wa.campaign_id) AS active_campaigns,
    round(count(DISTINCT wa.campaign_id) / count(DISTINCT c.campaign_id) * 100, 2) AS retention_pct
FROM cohorts AS c
LEFT JOIN weekly_activity AS wa
    ON c.campaign_id = wa.campaign_id
    AND wa.activity_week >= c.cohort_week
GROUP BY c.cohort_week
ORDER BY c.cohort_week
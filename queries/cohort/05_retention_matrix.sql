WITH cohorts AS (
    SELECT DISTINCT
        campaign_id,
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
    dateDiff('week', c.cohort_week, wa.activity_week) AS week_num,
    count(DISTINCT wa.campaign_id) AS active_campaigns
FROM cohorts AS c
LEFT JOIN weekly_activity AS wa
    ON c.campaign_id = wa.campaign_id
    AND wa.activity_week >= c.cohort_week
GROUP BY c.cohort_week, week_num
ORDER BY c.cohort_week, week_num
SELECT
    cohort_week,
    count(DISTINCT campaign_id) AS active_campaigns
FROM marketing.ads_cohorts
GROUP BY cohort_week
ORDER BY cohort_week
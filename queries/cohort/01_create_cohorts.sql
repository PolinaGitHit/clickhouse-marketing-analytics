INSERT INTO marketing.ads_cohorts
SELECT DISTINCT
    campaign_id,
    campaign_name,
    toMonday(toStartOfWeek(event_date)) AS cohort_week
FROM marketing.ads_data
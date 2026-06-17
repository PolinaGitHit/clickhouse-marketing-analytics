SELECT
    toStartOfMonth(event_date) AS month,
    campaign_name,
    round(avg(ctr), 2) AS avg_ctr,
    sum(clicks) AS total_clicks,
    sum(impressions) AS total_impressions,
    sum(cost) AS total_cost,
    sum(conversions) AS total_conversions
FROM marketing.ads_data
GROUP BY month, campaign_name
ORDER BY month, avg_ctr DESC
SELECT
    campaign_name,
    round(avg(ctr), 2) AS avg_ctr,
    sum(clicks) AS total_clicks,
    sum(impressions) AS total_impressions
FROM marketing.ads_data
GROUP BY campaign_name
ORDER BY avg_ctr DESC
SELECT
    campaign_name,
    round(avg(ctr), 2) AS avg_ctr,
    round(avg(cpa), 2) AS avg_cpa,
    sum(cost) AS total_cost,
    sum(clicks) AS total_clicks,
    sum(impressions) AS total_impressions,
    sum(conversions) AS total_conversions
FROM marketing.ads_data
GROUP BY campaign_name
ORDER BY total_cost DESC
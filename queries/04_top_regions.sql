SELECT
    region,
    sum(cost) AS total_cost,
    sum(clicks) AS total_clicks,
    sum(impressions) AS total_impressions,
    sum(conversions) AS total_conversions,
    round(avg(ctr), 2) AS avg_ctr
FROM marketing.ads_data
GROUP BY region
ORDER BY total_cost DESC
LIMIT 10
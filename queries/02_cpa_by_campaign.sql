SELECT
    campaign_name,
    round(avg(cpa), 2) AS avg_cpa,
    sum(cost) AS total_cost,
    sum(conversions) AS total_conversions
FROM marketing.ads_data
GROUP BY campaign_name
ORDER BY avg_cpa DESC
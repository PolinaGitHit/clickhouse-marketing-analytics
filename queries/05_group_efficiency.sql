SELECT
    campaign_name,
    group_name,
    sum(cost) AS total_cost,
    sum(clicks) AS total_clicks,
    sum(conversions) AS total_conversions,
    round(avg(cr), 2) AS avg_cr,
    round(avg(ctr), 2) AS avg_ctr,
    round(avg(cpa), 2) AS avg_cpa
FROM marketing.ads_data
GROUP BY campaign_name, group_name
ORDER BY total_cost DESC
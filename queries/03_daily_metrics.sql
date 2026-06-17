SELECT
    event_date,
    sum(cost) AS total_cost,
    sum(clicks) AS total_clicks,
    sum(impressions) AS total_impressions,
    sum(conversions) AS total_conversions,
    round(avg(ctr), 2) AS avg_ctr,
    round(avg(cpa), 2) AS avg_cpa
FROM marketing.ads_data
GROUP BY event_date
ORDER BY event_date
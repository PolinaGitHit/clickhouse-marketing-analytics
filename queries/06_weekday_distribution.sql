SELECT
    toDayOfWeek(event_date) AS dow,
    campaign_name,
    sum(clicks) AS total_clicks,
    sum(impressions) AS total_impressions,
    round(avg(ctr), 2) AS avg_ctr
FROM marketing.ads_data
GROUP BY dow, campaign_name
ORDER BY campaign_name, dow
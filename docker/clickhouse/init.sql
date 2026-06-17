CREATE DATABASE IF NOT EXISTS marketing;

CREATE TABLE IF NOT EXISTS marketing.ads_data (
    event_date Date,
    campaign_id UInt64,
    campaign_name String,
    group_name String,
    group_id UInt64,
    ad_id UInt64,
    region String,
    region_code UInt32,
    keyword String,
    cost Float64,
    impressions UInt64,
    clicks UInt64,
    conversions UInt64,
    cr Float64,
    cpa Float64,
    ctr Float64
) ENGINE = MergeTree()
ORDER BY (event_date, campaign_name);

CREATE TABLE IF NOT EXISTS marketing.ads_cohorts (
    campaign_id UInt64,
    campaign_name String,
    cohort_week Date
) ENGINE = MergeTree()
ORDER BY (cohort_week, campaign_id);
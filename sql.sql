-- check data quality 
SELECT
    COUNT(*) AS total_records,
    COUNT(*) FILTER (
        WHERE report_date IS NULL
    ) AS missing_dates,
    COUNT(*) FILTER (
        WHERE entity_id IS NULL
    ) AS missing_entity_ids,
    COUNT(*) FILTER (
        WHERE hqla_gbp_m IS NULL
    ) AS missing_hqla,
    COUNT(*) FILTER (
        WHERE net_cash_outflows_30d_gbp_m IS NULL
    ) AS missing_outflows,
    COUNT(*) FILTER (
        WHERE net_cash_outflows_30d_gbp_m < 0
    ) AS negative_outflows
FROM public.balance_sheet;

-- calculation of liquidity coverage proxy
SELECT
    report_date,
    entity_id,
    entity_name,
    hqla_gbp_m,
    net_cash_outflows_30d_gbp_m,
    ROUND(
        (hqla_gbp_m / NULLIF(
            net_cash_outflows_30d_gbp_m, 0
        )) * 100,
        2
    ) AS calculated_lcr_proxy_pct
FROM public.balance_sheet
ORDER BY report_date, entity_id;

-- identifying records that need attention
SELECT
    report_date,
    entity_id,
    entity_name,
    ROUND(
        (hqla_gbp_m / NULLIF(
            net_cash_outflows_30d_gbp_m, 0
        )) * 100,
        2
    ) AS lcr_proxy_pct,
    CASE
        WHEN hqla_gbp_m IS NULL
          OR net_cash_outflows_30d_gbp_m IS NULL
          OR net_cash_outflows_30d_gbp_m <= 0
            THEN 'DATA REVIEW REQUIRED'
        WHEN hqla_gbp_m / net_cash_outflows_30d_gbp_m < 1
            THEN 'HIGH RISK'
        WHEN hqla_gbp_m / net_cash_outflows_30d_gbp_m < 1.2
            THEN 'WARNING'
        ELSE 'NORMAL'
    END AS risk_status
FROM public.balance_sheet
ORDER BY report_date DESC, lcr_proxy_pct ASC NULLS FIRST;


-- finding latest risk status for each entity
WITH latest_records AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY entity_id
            ORDER BY report_date DESC
        ) AS rn
    FROM public.balance_sheet
)
SELECT
    report_date,
    entity_id,
    entity_name,
    hqla_gbp_m,
    net_cash_outflows_30d_gbp_m,
    ROUND(
        (hqla_gbp_m / NULLIF(
            net_cash_outflows_30d_gbp_m, 0
        )) * 100,
        2
    ) AS lcr_proxy_pct
FROM latest_records
WHERE rn = 1
ORDER BY lcr_proxy_pct ASC NULLS FIRST;

-- Calculation of monthly liquidity trends

SELECT
    DATE_TRUNC('month', report_date)::DATE AS month,
    ROUND(AVG(
        hqla_gbp_m / NULLIF(
            net_cash_outflows_30d_gbp_m, 0
        ) * 100
    ), 2) AS avg_lcr_proxy_pct,
    COUNT(*) AS records_analyzed,
    COUNT(*) FILTER (
        WHERE hqla_gbp_m IS NULL
           OR net_cash_outflows_30d_gbp_m IS NULL
           OR net_cash_outflows_30d_gbp_m <= 0
    ) AS records_needing_review
FROM public.balance_sheet
GROUP BY DATE_TRUNC('month', report_date)
ORDER BY month;

-- Detecting deteriorating liquidity

WITH liquidity_trend AS (
    SELECT
        report_date,
        entity_id,
        entity_name,
        hqla_gbp_m / NULLIF(
            net_cash_outflows_30d_gbp_m, 0
        ) * 100 AS lcr_proxy_pct,
        LAG(
            hqla_gbp_m / NULLIF(
                net_cash_outflows_30d_gbp_m, 0
            ) * 100
        ) OVER (
            PARTITION BY entity_id
            ORDER BY report_date
        ) AS previous_lcr_proxy_pct
    FROM public.balance_sheet
)
SELECT
    report_date,
    entity_id,
    entity_name,
    ROUND(lcr_proxy_pct, 2) AS current_lcr_proxy_pct,
    ROUND(previous_lcr_proxy_pct, 2) AS previous_lcr_proxy_pct,
    ROUND(
        lcr_proxy_pct - previous_lcr_proxy_pct, 2
    ) AS change_percentage_points,
    CASE
        WHEN lcr_proxy_pct IS NULL
          OR previous_lcr_proxy_pct IS NULL
            THEN 'INSUFFICIENT DATA'
        WHEN lcr_proxy_pct < 100
            THEN 'HIGH RISK'
        WHEN lcr_proxy_pct < previous_lcr_proxy_pct
            THEN 'LIQUIDITY DECLINING'
        ELSE 'STABLE OR IMPROVING'
    END AS early_warning_status
FROM liquidity_trend
ORDER BY report_date DESC, change_percentage_points ASC NULLS FIRST;



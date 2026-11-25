-- Purpose: Compare each entity's valid proxy with its previous available observation.
-- Change is measured in percentage points; observations may not be exactly one month apart.
WITH metrics AS (
    SELECT
        report_date,
        entity_id,
        entity_name,
        CASE
            WHEN hqla_gbp_m IS NULL
              OR hqla_gbp_m < 0
              OR net_cash_outflows_30d_gbp_m IS NULL
              OR net_cash_outflows_30d_gbp_m <= 0
                THEN NULL
            ELSE hqla_gbp_m / net_cash_outflows_30d_gbp_m * 100
        END AS lcr_proxy_pct
    FROM public.balance_sheet
),
liquidity_trend AS (
    SELECT
        *,
        LAG(lcr_proxy_pct) OVER (
            PARTITION BY entity_id ORDER BY report_date
        ) AS previous_lcr_proxy_pct
    FROM metrics
)
SELECT
    report_date,
    entity_id,
    entity_name,
    ROUND(lcr_proxy_pct, 2) AS current_lcr_proxy_pct,
    ROUND(previous_lcr_proxy_pct, 2) AS previous_lcr_proxy_pct,
    ROUND(lcr_proxy_pct - previous_lcr_proxy_pct, 2) AS change_percentage_points,
    CASE
        WHEN lcr_proxy_pct IS NULL OR previous_lcr_proxy_pct IS NULL
            THEN 'INSUFFICIENT DATA'
        WHEN lcr_proxy_pct < 100 THEN 'HIGH RISK'
        WHEN lcr_proxy_pct < previous_lcr_proxy_pct THEN 'LIQUIDITY DECLINING'
        ELSE 'STABLE OR IMPROVING'
    END AS early_warning_status
FROM liquidity_trend
ORDER BY report_date DESC, change_percentage_points ASC NULLS FIRST;

-- Purpose: Compare each entity's proxy with its previous available observation.
-- Change is in percentage points. LAG rows may not be exactly one month apart.
WITH liquidity_trend AS (
    SELECT
        report_date, entity_id, entity_name,
        hqla_gbp_m / NULLIF(net_cash_outflows_30d_gbp_m, 0) * 100
            AS lcr_proxy_pct,
        LAG(hqla_gbp_m / NULLIF(net_cash_outflows_30d_gbp_m, 0) * 100)
            OVER (PARTITION BY entity_id ORDER BY report_date)
            AS previous_lcr_proxy_pct
    FROM public.balance_sheet
)
SELECT
    report_date, entity_id, entity_name,
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

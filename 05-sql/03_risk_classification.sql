-- Purpose: Assign illustrative risk categories.
-- Thresholds are project assumptions, not JPMorgan/internal bank limits.
WITH metrics AS (
    SELECT
        report_date,
        entity_id,
        entity_name,
        hqla_gbp_m,
        net_cash_outflows_30d_gbp_m,
        CASE
            WHEN hqla_gbp_m IS NULL
              OR hqla_gbp_m < 0
              OR net_cash_outflows_30d_gbp_m IS NULL
              OR net_cash_outflows_30d_gbp_m <= 0
                THEN NULL
            ELSE (hqla_gbp_m / net_cash_outflows_30d_gbp_m) * 100
        END AS lcr_proxy_pct
    FROM public.balance_sheet
)
SELECT
    report_date,
    entity_id,
    entity_name,
    ROUND(lcr_proxy_pct, 2) AS lcr_proxy_pct,
    CASE
        WHEN lcr_proxy_pct IS NULL THEN 'DATA REVIEW REQUIRED'
        WHEN lcr_proxy_pct < 100 THEN 'HIGH RISK'
        WHEN lcr_proxy_pct < 120 THEN 'WARNING'
        ELSE 'NORMAL'
    END AS risk_status
FROM metrics
ORDER BY report_date DESC, lcr_proxy_pct ASC NULLS FIRST;

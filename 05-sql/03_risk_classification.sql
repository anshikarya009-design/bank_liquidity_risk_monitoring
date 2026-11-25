-- Purpose: Assign illustrative risk categories.
-- Thresholds are project assumptions, not JPMorgan/internal bank limits.
SELECT
    report_date, entity_id, entity_name,
    ROUND((hqla_gbp_m / NULLIF(net_cash_outflows_30d_gbp_m, 0)) * 100, 2)
        AS lcr_proxy_pct,
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

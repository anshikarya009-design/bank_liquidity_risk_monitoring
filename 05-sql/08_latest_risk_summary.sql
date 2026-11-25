-- Purpose: Latest observation per entity with illustrative risk classification.
WITH latest_records AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY entity_id ORDER BY report_date DESC
           ) AS rn
    FROM public.balance_sheet
),
latest_metrics AS (
    SELECT
        report_date, entity_id, entity_name,
        hqla_gbp_m, net_cash_outflows_30d_gbp_m,
        hqla_gbp_m / NULLIF(net_cash_outflows_30d_gbp_m, 0) * 100
            AS lcr_proxy_pct
    FROM latest_records
    WHERE rn = 1
)
SELECT
    report_date, entity_id, entity_name,
    ROUND(lcr_proxy_pct, 2) AS lcr_proxy_pct,
    CASE
        WHEN hqla_gbp_m IS NULL
          OR net_cash_outflows_30d_gbp_m IS NULL
          OR net_cash_outflows_30d_gbp_m <= 0
            THEN 'DATA REVIEW REQUIRED'
        WHEN lcr_proxy_pct < 100 THEN 'HIGH RISK'
        WHEN lcr_proxy_pct < 120 THEN 'WARNING'
        ELSE 'NORMAL'
    END AS risk_status
FROM latest_metrics
ORDER BY lcr_proxy_pct ASC NULLS FIRST;

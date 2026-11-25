-- Purpose: Return the latest observation for each entity.
WITH latest_records AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY entity_id ORDER BY report_date DESC
           ) AS rn
    FROM public.balance_sheet
)
SELECT
    report_date, entity_id, entity_name,
    hqla_gbp_m, net_cash_outflows_30d_gbp_m,
    ROUND((hqla_gbp_m / NULLIF(net_cash_outflows_30d_gbp_m, 0)) * 100, 2)
        AS lcr_proxy_pct
FROM latest_records
WHERE rn = 1
ORDER BY lcr_proxy_pct ASC NULLS FIRST;

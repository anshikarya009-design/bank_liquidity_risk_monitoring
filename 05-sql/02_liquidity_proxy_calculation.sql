-- Purpose: Calculate a simplified liquidity coverage proxy.
-- This is not an official regulatory LCR calculation.
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
        ELSE ROUND((hqla_gbp_m / net_cash_outflows_30d_gbp_m) * 100, 2)
    END AS calculated_lcr_proxy_pct
FROM public.balance_sheet
ORDER BY report_date, entity_id;

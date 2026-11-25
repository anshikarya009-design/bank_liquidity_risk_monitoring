-- Purpose: Summarize valid liquidity proxies and review counts by month.
WITH metrics AS (
    SELECT
        DATE_TRUNC('month', report_date)::DATE AS month,
        CASE
            WHEN hqla_gbp_m IS NULL
              OR hqla_gbp_m < 0
              OR net_cash_outflows_30d_gbp_m IS NULL
              OR net_cash_outflows_30d_gbp_m <= 0
                THEN NULL
            ELSE hqla_gbp_m / net_cash_outflows_30d_gbp_m * 100
        END AS lcr_proxy_pct
    FROM public.balance_sheet
)
SELECT
    month,
    ROUND(AVG(lcr_proxy_pct), 2) AS avg_lcr_proxy_pct,
    COUNT(*) AS records_analyzed,
    COUNT(*) FILTER (WHERE lcr_proxy_pct IS NULL) AS records_needing_review
FROM metrics
GROUP BY month
ORDER BY month;

-- Purpose: Summarize liquidity proxy and data-review counts by month.
SELECT
    DATE_TRUNC('month', report_date)::DATE AS month,
    ROUND(AVG(hqla_gbp_m / NULLIF(net_cash_outflows_30d_gbp_m, 0) * 100), 2)
        AS avg_lcr_proxy_pct,
    COUNT(*) AS records_analyzed,
    COUNT(*) FILTER (
        WHERE hqla_gbp_m IS NULL
           OR net_cash_outflows_30d_gbp_m IS NULL
           OR net_cash_outflows_30d_gbp_m <= 0
    ) AS records_needing_review
FROM public.balance_sheet
GROUP BY DATE_TRUNC('month', report_date)
ORDER BY month;

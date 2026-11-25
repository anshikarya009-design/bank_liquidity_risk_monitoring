-- Purpose: Check completeness and basic validity. Read-only.
SELECT
    COUNT(*) AS total_records,
    COUNT(*) FILTER (WHERE report_date IS NULL) AS missing_dates,
    COUNT(*) FILTER (WHERE entity_id IS NULL) AS missing_entity_ids,
    COUNT(*) FILTER (WHERE hqla_gbp_m IS NULL) AS missing_hqla,
    COUNT(*) FILTER (WHERE net_cash_outflows_30d_gbp_m IS NULL) AS missing_outflows,
    COUNT(*) FILTER (WHERE net_cash_outflows_30d_gbp_m < 0) AS negative_outflows
FROM public.balance_sheet;

-- Optional: inspect records needing review.
SELECT *
FROM public.balance_sheet
WHERE report_date IS NULL
   OR entity_id IS NULL
   OR hqla_gbp_m IS NULL
   OR net_cash_outflows_30d_gbp_m IS NULL
   OR net_cash_outflows_30d_gbp_m < 0
ORDER BY report_date NULLS FIRST, entity_id;

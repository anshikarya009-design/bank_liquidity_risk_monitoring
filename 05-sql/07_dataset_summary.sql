-- Purpose: Summarize reporting coverage and distinct entities.
SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT entity_id) AS distinct_entities,
    MIN(report_date) AS first_report_date,
    MAX(report_date) AS latest_report_date,
    COUNT(DISTINCT DATE_TRUNC('month', report_date)) AS reporting_months
FROM public.balance_sheet;

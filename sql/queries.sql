-- Top 5 funds by AUM
SELECT * FROM fact_aum
ORDER BY aum DESC
LIMIT 5;

-- Average NAV by month
SELECT strftime('%Y-%m', date),
AVG(nav)
FROM fact_nav
GROUP BY 1;

-- SIP YoY Growth
SELECT year,
SUM(amount)
FROM fact_transactions
WHERE transaction_type='SIP'
GROUP BY year;

-- Transactions by state
SELECT state,
COUNT(*)
FROM fact_transactions
GROUP BY state;

-- Expense ratio below 1%
SELECT *
FROM fact_performance
WHERE expense_ratio < 1;

-- Top performing funds
SELECT *
FROM fact_performance
ORDER BY return_5y DESC
LIMIT 10;

-- Highest NAV schemes
SELECT *
FROM fact_nav
ORDER BY nav DESC
LIMIT 10;

-- Fund count by category
SELECT category,
COUNT(*)
FROM dim_fund
GROUP BY category;

-- Total inflows by category
SELECT category,
SUM(amount)
FROM fact_transactions
GROUP BY category;

-- Monthly transaction volume
SELECT strftime('%Y-%m', date),
COUNT(*)
FROM fact_transactions
GROUP BY 1;

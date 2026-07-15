SELECT COUNT(*)
FROM companies;


SELECT id,
       COUNT(*) AS years
FROM profitandloss
GROUP BY id
ORDER BY years DESC;


SELECT id,
       AVG(roe_percentage) AS avg_roe
FROM companies
GROUP BY id
ORDER BY avg_roe DESC;


SELECT id,
       MAX(close_price) AS highest_price
FROM stock_prices
GROUP BY id
ORDER BY highest_price DESC
LIMIT 10;


SELECT id,
       COUNT(*)
FROM balancesheet
GROUP BY id;


SELECT id,
       SUM(net_profit)
FROM profitandloss
GROUP BY id;


SELECT *
FROM analysis
LIMIT 10;


SELECT *
FROM financial_ratios
ORDER BY year DESC
LIMIT 20;


SELECT id,
       COUNT(*)
FROM documents
GROUP BY id
ORDER BY COUNT(*) DESC;


PRAGMA foreign_key_check;
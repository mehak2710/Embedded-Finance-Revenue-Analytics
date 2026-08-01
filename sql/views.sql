/* Executive KPI view*/

CREATE VIEW funnel_summary AS

SELECT

stage,

COUNT(DISTINCT customer_id)
AS users


FROM funnel_events


GROUP BY stage;

SELECT * FROM funnel_summary;

/* Revenue prformance dashboard view */

CREATE VIEW revenue_dashboard AS

SELECT

COUNT(transaction_id) AS total_transactions,

COUNT(DISTINCT customer_id) AS total_customers,

ROUND(SUM(revenue),2) AS total_revenue,

ROUND(
AVG(amount),
2
) AS avg_transaction_value


FROM transactions

WHERE status='Success';

SELECT * 
FROM revenue_dashboard;

/* Product performance dashboard */

CREATE VIEW product_performance AS


SELECT

p.product_name,

p.category,


COUNT(t.transaction_id)
AS transactions,


COUNT(DISTINCT t.customer_id)
AS customers,


ROUND(SUM(t.revenue),2)
AS revenue,


ROUND(

SUM(t.revenue)
/
COUNT(DISTINCT t.customer_id),

2

)

AS revenue_per_customer


FROM transactions t


JOIN products p

ON t.product_id=p.product_id


WHERE t.status='Success'


GROUP BY

p.product_name,

p.category;

SELECT*FROM product_performance;

/* Partner analytics dashboard */

CREATE VIEW partner_performance AS


SELECT


p.partner_name,


p.industry,


COUNT(DISTINCT t.customer_id)
AS customers,


COUNT(t.transaction_id)
AS transactions,


ROUND(SUM(t.revenue),2)
AS revenue,


ROUND(

AVG(
CASE
WHEN t.is_repeat='Yes'
THEN 1
ELSE 0
END
)*100,

2

)

AS repeat_rate



FROM transactions t


JOIN partners p

ON t.partner_id=p.partner_id


WHERE t.status='Success'


GROUP BY

p.partner_name,

p.industry;

SELECT*FROM partner_performance;

/*customer value dashboard */

CREATE VIEW customer_value AS


SELECT


customer_id,


COUNT(transaction_id)
AS transactions,


COUNT(DISTINCT product_id)
AS products_used,


ROUND(SUM(revenue),2)
AS lifetime_value,


MAX(transaction_date)
AS last_transaction



FROM transactions


WHERE status='Success'


GROUP BY customer_id;

SELECT*FROM customer_value;

/* Funnel analytics dashboard */

CREATE VIEW funnel_dashboard AS


SELECT


stage,


COUNT(DISTINCT customer_id)
AS users



FROM funnel_events


GROUP BY stage;

SELECT*FROM funnel_dashboard;

/* Executive KPI view */

CREATE VIEW executive_kpi AS


SELECT


COUNT(DISTINCT customer_id)
AS customers,


COUNT(transaction_id)
AS transactions,


ROUND(SUM(revenue),2)
AS revenue,


ROUND(

SUM(revenue)

/

COUNT(DISTINCT customer_id),

2

)

AS average_cltv



FROM transactions


WHERE status='Success';

SELECT*FROM executive_kpi;


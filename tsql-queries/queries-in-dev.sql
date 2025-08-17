
-------------------------------------------------------------------
-- query Last Day FundValue Data
WITH CTE_LastDay
AS 
(
    SELECT MAX(Dt) as MAXDT FROM FundValue
)
SELECT * FROM CTE_LastDay
INNER JOIN FundValue as fv
ON fv.Dt = CTE_LastDay.MAXDT
--------------
-- Equivalant:
--------------
SELECT * FROM FundValue WHERE Dt = (SELECT MAX(Dt) FROM FundValue);
-------------------------------------------------------------------


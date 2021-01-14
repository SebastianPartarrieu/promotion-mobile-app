-- SQL queries to be fed to anosdb
-- Use the :param syntax for portability and readability.

-- name: now
SELECT CURRENT_TIMESTAMP;

--name: get_promotion_all
SELECT DISTINCT p.pid, p.pdescription, c.cnom, p.tdebut 
FROM Promotion AS p
JOIN Commerce AS c USING (cid)
ORDER BY p.tdebut DESC;

--name: get_promotion_agg_all
SELECT DISTINCT p.pid, p.pdescription, c.cnom, p.tdebut
FROM Promotion AS p
JOIN Commerce AS c USING (cid)
JOIN Agglomeration AS a USING (aid)
WHERE a.anom = :agg
ORDER BY p.tdebut DESC;

--name: get_promotion_agg_nb
SELECT DISTINCT p.pid, p.pdescription, c.cnom, p.tdebut
FROM Promotion AS p
JOIN Commerce AS c USING (cid)
JOIN Agglomeration AS a USING (aid)
WHERE a.anom = :agg 
ORDER BY p.tdebut DESC
LIMIT :nb;

--name: get_promotion_nb_all
SELECT DISTINCT p.pid, p.pdescription, c.cnom, p.tdebut
FROM Promotion AS p
JOIN Commerce AS c USING (cid)
ORDER BY p.tdebut DESC
LIMIT :nb;



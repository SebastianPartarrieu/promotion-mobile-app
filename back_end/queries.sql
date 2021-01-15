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

--name: get_commerce
SELECT DISTINCT c.cnom, c.cpresentation, a.anom, c.code_postal, c.rue_and_num
FROM Commerce AS c
JOIN CommerceCategorie AS cc USING (cid)
JOIN Categorie AS ca USING (catid)
JOIN Agglomeration AS a USING (aid)
WHERE a.anom LIKE :agg AND ca.catnom LIKE :cat
ORDER BY 1;

--name: get_client_info
SELECT clnom, clpnom, clemail, aid
FROM Client 
WHERE clid = :clid;

--name: post_client_info!
INSERT INTO Client(clnom, clpnom, clemail, aid) VALUES (:clnom, :clpnom, :clemail, :aid);
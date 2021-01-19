-- SQL queries to be fed to anosdb
-- Use the :param syntax for portability and readability.

-- name: now
SELECT CURRENT_TIMESTAMP;

--name: get_promotion
SELECT DISTINCT p.pdescription, c.cnom, p.tdebut
FROM Promotion AS p
JOIN Commerce AS c USING (cid)
JOIN Agglomeration AS a USING (aid)
JOIN CommerceCategorie AS cc USING (cid)
JOIN Categorie AS ca USING (catid)
WHERE a.anom LIKE :agg AND ca.catnom LIKE :cat
ORDER BY p.tdebut DESC
LIMIT :nb;

--name: get_promotion_info
SELECT p.pdescription, c.cnom, p.tdebut, p.tfin
FROM Promotion AS p
JOIN Commerce AS c USING (cid)
WHERE p.pid = :pid;

--name: get_commerce
SELECT c.cnom, c.cpresentation, a.anom, c.code_postal, c.rue_and_num
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

--name: fetch_login_client
SELECT clid, clemail, clmdp FROM Client
WHERE clemail = :clemail;

--name: post_client_info!
INSERT INTO Client(clnom, clpnom, clemail, aid, clmdp) VALUES (:clnom, :clpnom, :clemail, :aid, :clmdp);

--name: patch_client_nom!
UPDATE Client SET clnom = :clnom WHERE clid = :clid;

--name: patch_client_pnom!
UPDATE Client SET clpnom = :clpnom WHERE clid = :clid;

--name: patch_client_clemail!
UPDATE Client SET clemail = :clemail WHERE clid = :clid;

--name: patch_client_aid!
UPDATE Client SET aid = :aid WHERE clid = :clid;

--name: get_commerce_info
SELECT cnom, cpresentation, cemail, url_ext, code_postal, rue_and_num, aid, catnom
FROM Commerce 
join CommerceCategorie using (cid)
join Categorie using (catid)
WHERE cid = :cid;

--name: patch_commerce_cpresentation!
UPDATE Commerce SET cpresentation = :cpresentation WHERE cid = :cid;

--name: patch_commerce_nom!
UPDATE Commerce SET cnom = :cnom WHERE cid = :cid;

--name: patch_commerce_cemail!
UPDATE Commerce SET cemail = :cemail WHERE cid = :cid;

--name: patch_commerce_url_ext!
UPDATE Commerce SET url_ext = :url_ext WHERE cid = :cid;

--name: patch_commerce_code_postal!
UPDATE Commerce SET code_postal = :code_postal WHERE cid = :cid;

--name: patch_commerce_rue_and_num!
UPDATE Commerce SET rue_and_num = :rue_and_num WHERE cid = :cid;

--name: patch_commerce_aid!
UPDATE Commerce SET aid = :aid WHERE cid = :cid;

--name: patch_commerce_catnom!
UPDATE CommerceCategorie SET catnom = :catnom WHERE cid = :cid;

--name: post_commerce_info
INSERT INTO Commerce (cnom, cpresentation, code_postal, rue_and_num, aid, cmdp, cemail, url_ext) 
VALUES (:cnom, :cpresentation, :code_postal, :rue_and_num, :aid, :cmdp, :cemail, :url_ext) returning cid;

--name: post_commerce_categorie!
INSERT INTO CommerceCategorie (cid, catid) values (:cid, (select catid from Categorie where catnom=:catnom));

--name: delete_commerce_categorie!
DELETE from CommerceCategorie where cid=1;

-- SQL queries to be fed to anosdb
-- Use the :param syntax for portability and readability.

-- name: now
SELECT CURRENT_TIMESTAMP;

--name: get_promotion
SELECT DISTINCT p.pid, p.pdescription, c.cnom, p.tdebut
FROM Promotion AS p
JOIN Commerce AS c USING (cid)
JOIN Agglomeration AS a USING (aid)
JOIN CommerceCategorie AS cc USING (cid)
JOIN Categorie AS ca USING (catid)
WHERE a.anom LIKE :agg AND ca.catnom LIKE :cat
ORDER BY p.tdebut DESC
LIMIT :nb;

--name: get_promotion_info
SELECT c.cid, p.pdescription, c.cnom, p.tdebut, p.tfin
FROM Promotion AS p
JOIN Commerce AS c USING (cid)
WHERE p.pid = :pid;

--name: get_commerce
SELECT DISTINCT c.cid, c.cnom, c.cpresentation, a.anom, c.code_postal, c.rue_and_num, c.latitude, c.longitude
FROM Commerce AS c
JOIN CommerceCategorie AS cc USING (cid)
JOIN Categorie AS ca USING (catid)
JOIN Agglomeration AS a USING (aid)
WHERE a.anom LIKE :agg AND ca.catnom LIKE :cat AND c.cnom LIKE '%%' || :search || '%%' 
ORDER BY 1;

--name: get_client_info
SELECT clnom, clpnom, clemail, aid
FROM Client 
WHERE clid = :clid;

--name: delete_client_info!
DELETE FROM Client WHERE clid = :clid;

--name: invalidate_client_account!
UPDATE Client SET active = False WHERE clid = :clid;

--name: check_client_active
SELECT active FROM Client WHERE clid = :clid; 

--name: fetch_login_client
SELECT clid, clemail, clmdp FROM Client
WHERE clemail = :clemail;

--name: post_client_info
INSERT INTO Client(clnom, clpnom, clemail, aid, clmdp) VALUES (:clnom, :clpnom, :clemail, :aid, :clmdp) RETURNING clid;

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

--name: fetch_code_postal_from_cid
SELECT code_postal FROM Commerce WHERE cid = :cid;

--name: fetch_rue_and_num_from_cid
SELECT rue_and_num FROM Commerce WHERE cid = :cid;

--name: fetch_aid_from_commerce
SELECT aid FROM Commerce WHERE cid = :cid;

--name: check_commerce_active
SELECT active FROM Commerce WHERE cid = :cid;

--name: delete_commerce_info!
DELETE FROM Commerce WHERE cid = :cid;

--name: invalidate_commerce_account!
UPDATE Commerce SET active = False WHERE cid = :cid;

--name: post_promotion
INSERT INTO Promotion(cid, pdescription, tdebut, tfin) VALUES (:cid, :pdescription, :tdebut, :tfin) RETURNING pid;

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

--name: patch_commerce_lat_long!
UPDATE Commerce SET latitude = :latitude, longitude = :longitude WHERE cid = :cid;


--name: patch_promotion_pdescription!
UPDATE Promotion SET pdescription = :pdescription WHERE pid = :pid;

--name: patch_promotion_tdebut!
UPDATE Promotion SET tdebut = :tdebut WHERE pid = :pid;

--name: patch_promotion_tfin!
UPDATE Promotion SET tfin = :tfin WHERE pid = :pid;


--name: post_commerce_info
INSERT INTO Commerce (cnom, cpresentation, code_postal, rue_and_num, aid, cmdp, cemail, url_ext, latitude, longitude) 
VALUES (:cnom, :cpresentation, :code_postal, :rue_and_num, :aid, :cmdp, :cemail, :url_ext, :latitude, :longitude) RETURNING cid;

--name: post_commerce_categorie!
INSERT INTO CommerceCategorie (cid, catid) values (:cid, (select catid from Categorie where catnom=:catnom));

--name: delete_commerce_categorie!
DELETE from CommerceCategorie where cid=:cid;

--name: fetch_login_commerce
SELECT cid, cemail,cmdp FROM Commerce 
Where cemail=:cemail;

--name: post_promotion_image
INSERT INTO ImagePromotion (imgname, ranks, verified, pid) VALUES (:imgname, :ranks, FALSE, :pid) returning imid;

--name: get_promotion_image
SELECT 'promotionImage/' || imgname, ranks,imid FROM ImagePromotion where pid=:pid and verified=FALSE ORDER BY ranks asc; 

--name: delete_promotion_image
DELETE from ImagePromotion where pid=:pid  and imid=:imid returning imgname;

--name: delete_promotion_images
DELETE from ImagePromotion where pid=:pid  returning imgname;

--name: change_promotion_filename_image!
UPDATE ImagePromotion SET ranks=:ranks WHERE imid=:imid and pid=:pid;


--name: verify_image!
UPDATE ImagePromotion SET verified=TRUE where imgname=:imgname;

--name: fetch_promotion_of_commerce
SELECT DISTINCT p.pdescription, c.cnom, p.tdebut
FROM Promotion AS p
JOIN Commerce AS c USING (cid)
WHERE c.cid = :cid
ORDER BY p.tdebut DESC;

--name: post_commerce_image
INSERT INTO ImageCommerce (imgname, ranks, cid, verified) VALUES (:imgname, :ranks, :cid, FALSE) returning imid;


--name: delete_commmerce_images
DELETE from ImageCommerce where cid=:cid  returning imgname;

--name: get_commerce_image
SELECT 'commerceImage/' || imgname, ranks, imid FROM ImageCommerce where cid=:cid and verified=FALSE ORDER BY ranks asc; 

--name: delete_commerce_image
DELETE from ImageCommerce where cid=:cid  and imid=:imid returning imgname;

--name: change_commerce_filename_image!
UPDATE ImageCommerce SET ranks=:ranks WHERE imid=:imid and cid=:cid;

--name: get_rank_last_image_promotion
Select ranks from ImagePromotion Where pid=:pid order by ranks desc limit 1;

--name: get_rank_last_image_commerce
Select ranks + 1 from ImageCommerce Where cid=:cid order by ranks desc limit 1;

--name: fetch_cid_of_pid
SELECT DISTINCT cid FROM Commerce AS c
JOIN Promotion AS p USING (cid)
WHERE p.pid = :pid;

--name: fetch_agglo_from_aid
SELECT anom FROM Agglomeration WHERE aid = :aid;

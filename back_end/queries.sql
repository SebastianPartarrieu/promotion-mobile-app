-- SQL queries to be fed to anosdb
-- Use the :param syntax for portability and readability.

-- name: now
SELECT CURRENT_TIMESTAMP;

--name: get_store_all
SELECT key, val FROM Store ORDER BY 1;

--name: post_store!
INSERT INTO Store VALUES (:mykey, :myval);

--name: delete_store!
DELETE FROM Store;

--name: get_store_filter
SELECT key, val FROM Store
WHERE key LIKE :myfilter;

--name: delete_store_filter!
DELETE FROM Store 
WHERE key LIKE :myfilter;

--name: get_store_key
SELECT val FROM Store WHERE key = :mykey;

--name: patch_value_with_key!
UPDATE Store SET val = :myval WHERE key = :mykey;

--name: delete_store_key!
DELETE FROM Store 
WHERE key = :mykey;
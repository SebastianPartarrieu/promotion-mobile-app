-- create application tables
CREATE TABLE Agglomeration(aid SERIAL PRIMARY KEY,
                           anom TEXT UNIQUE NOT NULL);

CREATE TABLE Categorie(catid SERIAL PRIMARY KEY,
                       catnom TEXT UNIQUE NOT NULL);


CREATE TABLE Client(clid SERIAL PRIMARY KEY,
                    clnom VARCHAR(32) NOT NULL,
                    clpnom VARCHAR(32) NOT NULL,
                    clemail VARCHAR(50) UNIQUE NOT NULL,
                    clmdp VARCHAR(100) NOT NULL,
                    aid INTEGER REFERENCES Agglomeration,
                    UNIQUE(clemail, clmdp));
 
CREATE TABLE Commerce(cid SERIAL PRIMARY KEY,
                      cnom VARCHAR(32) NOT NULL,
                      cpresentation VARCHAR(400) NOT NULL,
                      cemail VARCHAR(100) UNIQUE NOT NULL,
                      url_ext VARCHAR(150),
                      code_postal INTEGER NOT NULL,
                      rue_and_num VARCHAR(100) NOT NULL,
                      aid INTEGER NOT NULL REFERENCES Agglomeration,
                      cmdp VARCHAR(100) NOT NULL,
                      UNIQUE(cnom, cpresentation, code_postal, rue_and_num),
                      UNIQUE(cemail, cmdp));
                      -- imid INTEGER NOT NULL REFERENCES Image,  
                      -- clocation GEOGRAPHY UNIQUE NOT NULL,
                      --UNIQUE (cnom, mdp));

CREATE TABLE CommerceCategorie(cid INTEGER NOT NULL REFERENCES Commerce,
                               catid INTEGER NOT NULL REFERENCES Categorie,
                               UNIQUE(cid, catid));

CREATE TABLE Promotion(pid SERIAL PRIMARY KEY,
                       cid INTEGER NOT NULL REFERENCES Commerce,
                       pdescription VARCHAR(400) NOT NULL,
                       tdebut DATE,
                       tfin DATE);

CREATE TABLE ClientCategorie(clid INTEGER NOT NULL REFERENCES Client,
                             catid INTEGER NOT NULL REFERENCES Categorie,
                             UNIQUE(clid, catid));

CREATE TABLE ClientFavCommerce(clid INTEGER NOT NULL REFERENCES Client,
                               cid INTEGER NOT NULL REFERENCES Commerce,
                               UNIQUE(clid, cid));

CREATE TABLE Admins(adminid SERIAL PRIMARY KEY, 
                    adminemail VARCHAR(150) UNIQUE NOT NULL,
                    adminmdp VARCHAR(100) NOT NULL);

CREATE TABLE ImagePromotion(imid SERIAL PRIMARY KEY,  imgname TEXT UNIQUE NOT NULL,
 ranks INTEGER NOT NULL, verified Boolean NOT NULL, pid INTEGER NOT NULL REFERENCES Promotion);

CREATE TABLE ImageCommerce(imid SERIAL PRIMARY KEY,  imgname TEXT UNIQUE NOT NULL,
 ranks INTEGER NOT NULL, verified Boolean NOT NULL, cid INTEGER NOT NULL REFERENCES Commerce);
 
--CREATE TABLE CarteFidelite(carteid SERIAL PRIMARY KEY,
--                           clid INTEGER NOT NULL REFERENCES Client,
--                           QRCode UNIQUE BYTEARRAY);

--CREATE TABLE CommerceScanCarte(cscancarteid SERIAL PRIMARY KEY,
--                               cid INTEGER NOT NULL REFERENCES Commerce,
--                               carteid INTEGER NOT NULL REFERENCES CarteFidelite,
--                               Point INTEGER NOT NULL,
--                               PointExpiration DATE,
--                               UNIQUE (cid, carteid));
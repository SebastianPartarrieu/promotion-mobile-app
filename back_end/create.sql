-- create application tables
CREATE TABLE Agglomeration(aid SERIAL PRIMARY KEY,
                           anom TEXT UNIQUE NOT NULL);

CREATE TABLE Categorie(catid SERIAL PRIMARY KEY,
                       catnom TEXT UNIQUE NOT NULL);

CREATE TABLE Client(clid SERIAL PRIMARY KEY,
                    clnom TEXT NOT NULL,
                    clpnom TEXT NOT NULL,
                    clemail TEXT UNIQUE NOT NULL,
                    aid INTEGER NOT NULL REFERENCES Agglomeration);

--CREATE TABLE Image(imid SERIAL PRIMARY KEY,  need to revisit  image database
--                 im ByteARRAY);      

CREATE TABLE Commerce(cid SERIAL PRIMARY KEY,
                      cnom TEXT NOT NULL,
                      cpresentation TEXT NOT NULL,
                      url_ext TEXT,
                      -- clocation GEOGRAPHY UNIQUE NOT NULL,
                      -- imid INTEGER NOT NULL REFERENCES Image,  
                      -- mdp TEXT NOT NULL,
                      code_postal INTEGER NOT NULL,
                      rue_num TEXT NOT NULL,
                      aid INTEGER NOT NULL REFERENCES Agglomeration,
                      UNIQUE (cnom, mdp));

CREATE TABLE CommerceCategorie(cid INTEGER NOT NULL REFERENCES Commerce,
                               catid INTEGER NOT NULL REFERENCES Categorie,
                               UNIQUE(cid, catid));

CREATE TABLE Promotion(pid SERIAL PRIMARY KEY,
                       cid INTEGER NOT NULL REFERENCES Commerce,
                       -- imid INTEGER NOT NULL REFERENCES Image,
                       pdescription TEXT NOT NULL,
                       tdebut TIMESTAMP,
                       tfin TIMESTAMP);

CREATE TABLE ClientCategorie(clid INTEGER NOT NULL REFERENCES Client,
                             catid INTEGER NOT NULL REFERENCES Categorie,
                             UNIQUE(clid, catid));

CREATE TABLE ClientFavCommerce(clid INTEGER NOT NULL REFERENCES Client,
                               cid INTEGER NOT NULL REFERENCES Commerce,
                               UNIQUE(clid, cid));

--CREATE TABLE CarteFidelite(carteid SERIAL PRIMARY KEY,
--                           clid INTEGER NOT NULL REFERENCES Client,
--                           QRCode UNIQUE BYTEARRAY);

--CREATE TABLE CommerceScanCarte(cscancarteid SERIAL PRIMARY KEY,
--                               cid INTEGER NOT NULL REFERENCES Commerce,
--                               carteid INTEGER NOT NULL REFERENCES CarteFidelite,
--                               Point INTEGER NOT NULL,
--                               PointExpiration DATE,
--                               UNIQUE (cid, carteid));
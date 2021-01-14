-- create application tables
CREATE TABLE Agglomeration(aid SERIAL PRIMARY KEY,
                           anom TEXT UNIQUE NOT NULL);

CREATE TABLE Categorie(catid SERIAL PRIMARY KEY,
                       catnom TEXT UNIQUE NOT NULL);

-- no authentification yet for clients
CREATE TABLE Client(clid SERIAL PRIMARY KEY,
                    clnom VARCHAR(32) NOT NULL,
                    clpnom VARCHAR(32) NOT NULL,
                    clemail VARCHAR(50) UNIQUE NOT NULL,
                    aid INTEGER NOT NULL REFERENCES Agglomeration);

--CREATE TABLE Image(imid SERIAL PRIMARY KEY,  need to revisit  image database
--                 im ByteARRAY);      

-- no authentification yet for commerce either 
CREATE TABLE Commerce(cid SERIAL PRIMARY KEY,
                      cnom VARCHAR(32) NOT NULL,
                      cpresentation VARCHAR(400) NOT NULL,
                      url_ext VARCHAR(150),
                      code_postal INTEGER NOT NULL,
                      rue_and_num TEXT NOT NULL,
                      aid INTEGER NOT NULL REFERENCES Agglomeration,
                      UNIQUE(cnom, cpresentation, code_postal, rue_and_num));
                      -- clocation GEOGRAPHY UNIQUE NOT NULL,
                      -- imid INTEGER NOT NULL REFERENCES Image,  
                      -- mdp TEXT NOT NULL,
                      --UNIQUE (cnom, mdp));

CREATE TABLE CommerceCategorie(cid INTEGER NOT NULL REFERENCES Commerce,
                               catid INTEGER NOT NULL REFERENCES Categorie,
                               UNIQUE(cid, catid));

CREATE TABLE Promotion(pid SERIAL PRIMARY KEY,
                       cid INTEGER NOT NULL REFERENCES Commerce,
                       -- imid INTEGER NOT NULL REFERENCES Image,
                       pdescription VARCHAR(400) NOT NULL,
                       tdebut DATE,
                       tfin DATE);

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
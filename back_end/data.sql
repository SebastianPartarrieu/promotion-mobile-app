-- initial data for testing purposes

-- initial agglomeration
INSERT INTO Agglomeration(anom) VALUES ('Paris'), ('Caen'), ('Nice');

-- initial categories
INSERT INTO Categorie(catnom) VALUES ('Restaurant'), ('Textile'), ('Librairie'), ('Coiffeur'), ('Hotel'), ('Magasin');

-- fictional clients and stores
INSERT INTO Client(clnom, clpnom, clemail, aid, clmdp) VALUES
('Stonebraker', 'Michael', 'mstonebraker@turing.org', 1, 'password'), 
('Codd', 'Edgar', 'ecodd@turing.org', 1, 'password'),
('Gray', 'James', 'jgray@turing.org', 2, 'Password'), 
('GenericName', 'Calvin', 'calvin.hobbes@me.com', 3, 'PaSSword');

INSERT INTO Commerce(cnom, cpresentation, code_postal, rue_and_num, aid, cmdp, cemail, latitude, longitude) VALUES
('Mines de Paris','L ecole nationale supérieure des mines de Paris',75272, '60 Boulevard Saint-Michel',1,'password5','matmaz@mines-paristech.fr',48.845770758284054,2.338596411379499),
('La maison des Mines', 'La Maison des Mines et des Ponts',75005,'270 rue saint jacques',1,'password4','matmaz4@mines-paristech.fr',48.841924881665165, 2.3411000804314797),
('Panda Wok','Envie d’un repas agréable asiatique ?',75015,'208 rue saint jacques',1,'password3','matmaz3@mines-paristech.fr',48.84554822428966,2.34254952705813),
('La Muraille du Phénix','Un bon choix de mets raffinés',75030,'179 rue saint jacques',1,'password2','matmaz2@mines-paristech.fr',48.84561630864182, 2.34271995589359),
('Mcdonalds','haîne emblématique de restauration rapide',75405,'65 Boulevard Saint-Michel',1,'password1','matmaz1@mines-paristech.fr',48.8471983255236, 2.341062113564534);


-- linking stores with their categories
INSERT INTO CommerceCategorie(cid, catid) VALUES (1, 1), (2, 1), (3, 2), (4, 3),(5, 3);

-- one or two promotions
INSERT INTO Promotion(cid, pdescription, tdebut, tfin) VALUES (1, 'La Marguerite a 7€!!!', '2021-01-14'::DATE, NULL),
(1, 'La Napolitaine a 8€', '2021-01-15', '2021-01-15'),
(3, 'Tous les livres à moins de 10€', '2021-01-15', NULL),
(2, 'Formule étudiante à 6 euros 50', '2021-01-15', '2021-01-15');

-- calvin loves food 
INSERT INTO ClientCategorie(clid, catid) VALUES (4, 1), (1, 3);

-- calvin loves mario's pizzas
INSERT INTO ClientFavCommerce(clid, cid) VALUES (4, 4), (2, 1), (3, 2); 

INSERT INTO Admins(adminemail, adminmdp) VALUES ('sebastian.partarrieu@mines-paristech.fr', 'amazingpassword');

INSERT INTO ImagePromotion (imid, imgname,ranks, verified, pid) VALUES (1, '1ad9b3c763dab473c47c85d65cc15fa2.jpg' , 1 ,FALSE, 1), (2, 'b891da14a418d6ed5e916e0276b7cfa4.jpg' , 1 ,FALSE, 2);
INSERT INTO ImageCommerce (imid, imgname,ranks, verified, cid) VALUES (1, 'a' , 1 ,FALSE, 1);


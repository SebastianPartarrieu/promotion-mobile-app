-- initial data for testing purposes

-- initial agglomeration
INSERT INTO Agglomeration(anom) VALUES ('Paris'), ('Caen'), ('Nice');

-- initial categories
INSERT INTO Categorie(catnom) VALUES ('Restaurant'), ('Textile'), ('Librairie'), ('Coiffeur'), ('Hotel'), ('Magasin'), ('Boulangerie');

-- fictional clients and stores
INSERT INTO Client(clnom, clpnom, clemail, aid, clmdp) VALUES
('Stonebraker', 'Michael', 'mstonebraker@turing.org', 1, 'password'), 
('Codd', 'Edgar', 'ecodd@turing.org', 1, 'password'),
('Gray', 'James', 'jgray@turing.org', 2, 'Password'), 
('GenericName', 'Calvin', 'calvin.hobbes@me.com', 3, 'PaSSword');

INSERT INTO Commerce(cnom, cpresentation, code_postal, rue_and_num, aid, cmdp, cemail, latitude, longitude, url_ext) VALUES
('Mines de Paris','L ecole nationale supérieure des mines de Paris',75272, '60 Boulevard Saint-Michel',1,'password5','matmaz@mines-paristech.fr',48.845770758284054,2.338596411379499, 'https://www.minesparis.psl.eu/'),
('La maison des Mines', 'La Maison des Mines et des Ponts',75005,'270 rue saint jacques',1,'password4','matmaz4@mines-paristech.fr',48.841924881665165, 2.3411000804314797, 'http://www.maisondesmines.com/'),
('Panda Wok','Envie d’un repas agréable asiatique ?',75015,'208 rue saint jacques',1,'password3','matmaz3@mines-paristech.fr',48.84554822428966,2.34254952705813, 'https://panda-wok-75005.eatbu.com/?lang=fr'),
('La Muraille du Phénix','Un bon choix de mets raffinés',75030,'179 rue saint jacques',1,'password2','matmaz2@mines-paristech.fr',48.84561630864182, 2.34271995589359, ''),
('Mcdonalds','haîne emblématique de restauration rapide',75405,'65 Boulevard Saint-Michel',1,'password1','matmaz1@mines-paristech.fr',48.8471983255236, 2.341062113564534, 'https://www.restaurants.mcdonalds.fr/mcdonalds-luxembourg-pantheon'),
('Le Christine','Cuisine française modernisé entre la bistronomie et la gastronomie',75006,'1 rue Christine',1 , 'password', 'contact@restaurantlechristine.com', 48.854312, 2.340345, 'https://www.restaurantlechristine.com/'),
('Le Vin Qui Danse', 'Cuisine Française Moderne et Brunch le Dimanche', 75013, '69 rue broca', 1, 'password', 'gobelins@vqd.fr', 48.836928, 2.347006, 'https://vqd.fr/'),
('Café Le Petit Pont','Pizzas, Tapas, Fondue, Cocktail', 75005, '1 rue du Petit Pont', 1, 'password', 'annelise@cafelepetitpont.com', 48.852668, 2.346724, 'https://www.lafourchette.com/restaurant/le-petit-pont-r3459'),
('Atelier Ramey', 'Cuisine française' ,75018, '23 rue Ramey', 1, 'password', 'latelier.ramey@gmail.com' , 48.888327, 2.346721, 'http://www.atelier-ramey.com/'),
('Le Petit Pontoise', 'Cuisine française traditionnelle. Produits de qualité de nos belles régions  en France. Cuisine Maison par des Maîtres restaurateurs', 75005, '9 rue de pontoise' ,1, 'password','contact@lepetitpontoise.fr', 48.849903, 2.352112, 'http://www.lepetitpontoise.fr/'),
('L Ami Pierre','Bistrot, bar à vin.',75011, '5 rue de la Main d Or', 1, 'password', 'robingreiner93@gmail.com', 48.851543, 2.378266, 'https://www.lamipierre.fr/'),
('Les Fous de l Île', 'Cuisine française bistronomique',75004, '33 rue des Deux Ponts' ,1,'password','contact@lesfousdelile.com',48.852207,2.356763, 'https://www.lesfousdelile.com/'),
('Le Mesturet', 'Cuisine traditionnelle française',75002,'77 rue de Richelieu',1, 'password','contact@lemesturet.com',48.869,2.338492, 'https://www.lemesturet.com/'),
('Les Vignes du Liban','Plus ancien restraurant libanais de paris',75015,'291 rue de Vaugirard',1,'password','lesvignesduliban@me.com',48.839274,2.300757, 'https://www.lesvignesduliban.fr/'),
('La Rotonde des Lin','Cuisine traditionnelle, grande variété de pizzas, couscous reconnus, dessert maison.',75014,'7 place du 25 août',1,'password','Larotondedeslin@gmail.com', 48.822233,2.325784, ''),
('Le Colvert Bistrot','Cuisine française bistronomique',75006,'54 rue Saint-André des Arts',1,'password','contact@lecolvertbistrot.com', 48.8535,2.340117, 'https://lecolvertbistrot.com/'),
('Pleine Terre', 'Cuisine française parfumée d agrumes et d épices par le chef Jimmy Desrivières',75016,'15 rue de Bassano',1,'password','contact@restaurant-pleineterre.com',48.869007,2.297196, 'https://www.restaurant-pleineterre.com/'),
('Restaurant Menelik','Spécialités éthiopiennes, saveurs d Ethiopie',75017,'4 rue Sauffroy',1,'password','menelik@wanadoo.fr', 48.890705,2.320475, 'https://www.menelikrestaurant.com');

-- linking stores with their categories
INSERT INTO CommerceCategorie(cid, catid) VALUES (1, 1), (2, 1), (3, 2), (4, 3),(5, 3),
(6, 1),
(7, 1),
(8, 1),
(9, 1),
(10, 1),
(11, 1),
(12, 1),
(13, 1),
(14, 1),
(15, 1),
(16, 1),
(17, 1);

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


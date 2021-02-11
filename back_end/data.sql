-- initial data for testing purposes

-- initial agglomeration
INSERT INTO Agglomeration(anom) VALUES ('Paris'), ('Caen'), ('Nice');

-- initial categories
INSERT INTO Categorie(catnom) VALUES ('Restaurant'), ('Textile'), ('Coiffeur'), ('Epicerie'), ('Boulangerie'), ('Autre'), ('Jeux');

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
('Mcdonalds','chaîne emblématique de restauration rapide',75005,'65 Boulevard Saint-Michel',1,'password1','matmaz1@mines-paristech.fr',48.8471983255236, 2.341062113564534, 'https://www.restaurants.mcdonalds.fr/mcdonalds-luxembourg-pantheon'),
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
('Restaurant Menelik','Spécialités éthiopiennes, saveurs d Ethiopie',75017,'4 rue Sauffroy',1,'password','menelik@wanadoo.fr', 48.890705,2.320475, 'https://www.menelikrestaurant.com'),
('LUCO', 'Nous ne faisons que de la livraison à domicile, pas de magasin sur place.', 75018, '18 rue Lécuyer', 1, 'pwd', 'pauline.guillorel@leluco.fr', 48.8894055609, 2.34488391743, 'https://www.leluco.fr'),
('Henri Le Roux Saint-Dominique', 'Chocolat', 75007, '52 Rue Saint-Dominique', 1, 'pwd', 'mi@chocolat-leroux.fr', 48.8599709399, 2.30980941397, 'https://www.epicery.com/epiceries/henri-le-roux-st-dominique'),
('Mamy Thérèse la Madeleinerie', 'Première madeleinerie artisanale de Paris. Nous vous proposons différentes catégories de madeleines fraîches du jour fabriquées sur place.', 75004, '19 rue Saint-Antoine', 1, 'pwd', 'contact@mamytherese.com', 48.8534777331, 2.36607221211, 'http://www.mamytherese.com'),
('La Tropicale Glacier', 'Nous sommes artisan-glacier. Nous livrons paris intramuros, des pots familiaux de 500/250ml de glaces.', 75013, '180 bld Vincent Auriol', 1, 'pwd', 'latropicaleglacier@gmail.com', 48.8315478768, 2.35720780981, 'http://www.latropicaleglacier.com'),
('La Boutique MOSO', 'Boutique indépendante de cosmétiques et produits d hygiène naturels et bio. Livraison et click and collect à Paris.', 75014, '105 rue Raymond Losserand', 1, 'pwd', 'service-client@laboutiquemoso2.fr', 48.8330415488, 2.3165577449, 'https://www.laboutiquemoso.fr'),
('Stohrer', 'La plus ancienne pâtisserie de Paris', 75015, '95, rue Cambronne', 1, 'pwd', 'contact@stohrer.fr', 48.8421774708, 2.3031499315, 'http://www.stohrer.fr'),
('L éléphant rose', 'Marchand de jouets depuis 1932, L éléphant rose propose des jeux et jouets ludiques et de qualités pour petits et grands.', 75016, '96 avenue Mozart', 1, 'pwd', 'nathalie@elephantrose.fr', 48.8510297182, 2.26721705041, 'https://www.elephantrose.fr'),
('Café Lanni', 'Nous torréfions quotidiennement notre café et partageons aussi notre passion du thé.', 75010, '54 rue Faubourg Saint', 1, 'pwd', 'contact@thecoffeelovers.fr', 48.8722093749, 2.35413370311, 'https://thecoffeelovers.fr/'),
('Julhès Paris Saint Maur', 'Charcuterie', 75011, '31 Rue Saint-Maur', 1, 'pwd', 'julhescomptabilite@gmail.com', 48.8609075846, 2.38121168843, 'https://www.epicery.com/epiceries/julhes-maur'),
('L autre Boulange', 'Boulangerie - pâtisserie', 75011, '43 Rue de Montreuil', 1, 'pwd', 'denisdurand.lab@gmail.com', 48.8504995744, 2.38799771737, 'https://www.epicery.com/epiceries/l-autre-boulange'),
('Foucade Batignolles', 'Boulangerie - pâtisserie', 75017, '24 rue des Moines', 1, 'pwd', 'adm@foucadeparis.com,manonf@foucadeparis.com', 48.8885185147, 2.319198551, 'https://www.epicery.com/epiceries/foucade-batignolles'),
('BOULANGERIE PAUL', 'commander sur Just-Eat, Uber eats ou Deliveroo', 75008, '49 Av Franklin Roosevelt', 1, 'pwd', 'dgriguer@gmail.com', 48.8701297709, 2.30988538078, 'https://www.paul.fr'),
('Robin des Jeux', 'Nous sommes une boutique spécialisée en jeux de société pour toute la famille. Jeux de plateau, jeux de rôle, jeux de cartes, puzzles. Retrait en boutique 15 minutes après achat sur notre site.', 75011, '37 boulevard de Charonne', 1, 'pwd', 'contact@robindesjeux.com', 48.8516942131, 2.39782424864, 'https://www.robindesjeux.com'),
('HéDONIE', 'Un large choix de produits bio et artisanaux , arrivage quotidien de produits frais de qualité \nLivraison à domicile dans tout Paris et service de click & collect', 75006, '6 rue de Mézières', 1, 'pwd', 'hedonie@outlook.fr', 48.8503288233, 2.33147603688, 'http://www.hedonie.fr'),
('RUSIDDA', 'Epicerie fine sicilienne, Rusidda propose des produits de qualité importés directement de Sicile. Savourez nos pizzolis, lasagnes, plats della Nonna et paniers gourmands pour devenir un chef sicilien!', 75003, '1 rue Borda', 1, 'pwd', 'inforusiddaparis@gmail.com', 48.8660516815, 2.35747103524, 'https://www.rusidda.fr/'),
('À la Mère de Famille', 'Les plus anciennes chocolaterie de Paris', 75007, '35, rue Cler', 1, 'pwd', 'contact@lameredefamille.com', 48.8570994159, 2.30635319685, 'http://www.lameredefamille.com'),
('La Ruche qui dit Oui de l Age d or', 'La ruche qui dit oui, Produits locaux,  Majoritairement Bio, Manger Mieux, Manger Juste\nLégumes Bio, fruits BIO, laitages, viande, poisson, épicerie...', 75013, '26 rue du Docteur Magnan', 1, 'pwd', 'ruche.age.d.or13@gmail.com', 48.8264934528, 2.35994686204, 'https://laruchequiditoui.fr/fr/assemblies/6437'),
('DAMYEL', 'Chocolats et confiseries vegan fabriqués à Paris', 75016, '33 avenue Raymond Poincaré', 1, 'pwd', 'contact@damyel2.com', 48.865647099, 2.2861907938, 'http://www.damyel.com'),
('Natalys', 'Spécialiste depuis 1953 des produits de puériculture et des jouets pour bébé', 75016, '5 rue Guichard', 1, 'pwd', 'serviceclient@natalys.com', 48.85852788, 2.27691448664, 'http://www.natalys.com'),
('Biocoop le Retour à la Terre Les Champs', 'Alimentation bio, traiteur, fromagerie, boulangerie, viandes, fruits et légumes frais, espace beauté - santé, alimentation animale etc.', 75008, '89 rue la Boétie', 1, 'pwd', 'communication@leretouralaterre.fr', 48.8717101968, 2.30828920575, 'https://www.leretouralaterre.fr/'),
('Le Panier de Zoé', 'Vente de légumes, épicerie, crémerie et vin', 75009, '11 bis Rue Blanche', 1, 'pwd', 'olivier.krot@lepanierdezoe.com', 48.8784494779, 2.3316034469, 'https://www.lepanierdezoe.fr'),
('RESERVOIR Bi0', 'Boutique sans emballage bio , Alimentation bio est en vrac.', 75019, '109, rue de Belleville', 1, 'pwd', 'Les-silos@orange.fr', 48.8746988637, 2.38689113578, 'https://www.puyp.fr/reservoirbio'),
('CONFITURE PARISIENNE', 'Fabrication et vente de confitures gastronomiques sur place.', 75012, '17 avenue daumesnil', 1, 'pwd', 'bonjour@confiture-parisienne.com', 48.8484904397, 2.37326510745, 'https://www.confiture-parisienne.com'),
('DAMYEL', 'Chocolats et confiseries vegan fabriqués à Paris', 75017, '87 avenue de Wagram', 1, 'pwd', 'contact@damyel.com', 48.8808793585, 2.2999596314, 'http://www.damyel.com'),
('LE FURET TANRADE', 'Maître chocolatier et maître confiturier. \nTous nos produits sont faits maison.  Dégustez aussi nos pâtes à pizza, brisées, feuillettées, sablées de fabrication artisanale.', 75010, '23-25 RUE DE CHABROL', 1, 'pwd', 'alainlefurettanrade@yahoo.fr', 48.8766841121, 2.35396975924, 'https://chocolatiersonline.com/fr-fr/le-furet-tanrade'),
('Pierre Marcolini', 'Chocolatier engagé. Fèves torréfiées Maison et savoir-faire artisanal.', 75006, '89 rue de Seine', 1, 'pwd', 'commande@marcolini.com', 48.8523715876, 2.33712012476, 'http://www.marcolini.com'),
('Peas&Love', 'Nous livrons le mercredi après-midi et le samedi matin des paniers venus directement des producteurs d Île-de-France qui travaillent bien.', 75015, '51 quai de grenelle', 1, 'pwd', 'Info@peasandlove.com', 48.850799553, 2.28434282092, 'http://lemarche.peasandlove.com'),
('LE JARDIN E(S)T LA RECETTE', 'Alimentation - Beauté - Produits d entretien :\ndes paniers de produits préparés maison, avec des ingrédients du jardin\n\nNous proposons des produits préparés maison, avec des ingrédients du jardin.', 75019, '24 rue clavel', 1, 'pwd', 'benedicte@lejardinestlarecette.fr', 48.8761935409, 2.38369115468, 'http://www.lejardinestlarecette.fr'),
('Caviar de Neuvic', 'Caviar, Epicerie', 75006, '16 rue de l Odéon', 1, 'pwd', 'nathalie.colliette@caviardeneuvic.com', 48.8506575246, 2.33860001017, 'https://www.epicery.com/epiceries/caviar-de-neuvic'),
('Coursier', 'Nous travaillons avec les sociétés et les particuliers pour leurs livraisons : matériel informatique télétravail, avec les épiceries, les hôpitaux etc', 75008, '66 avenue des champs Élysées', 1, 'pwd', 'contacts@2htransports.com', 48.8708564224, 2.30536717562, 'https://coursier.xyz'),
('Causses', 'Alimentation générale de qualité', 75003, '222 rue Saint Martin', 1, 'pwd', 'Commande@causses.org', 48.8640189381, 2.35301306669, 'https://www.causses.org'),
('Le Zingam', 'Pour proposer une sélection diversifiée de fruits et légumes de saison, de charcuteries,\nde fromages, de vins et produits d’épicerie salée et sucrée, le Zingam a sillonné la campagne française!', 75011, '75 rue du chemin vert', 1, 'pwd', 'contact@lezingam.com', 48.8604976726, 2.37901148904, 'https://lezingam.com/'),
('Troll2jeux', 'des jeux pour toute la famille, pour les gamers, les novices, des jeux à deux, compétitifs ou coopératifs, des escape games : ce le monde du jeu a de mieux pour vous divertir ou vous faire réfléchir!', 75012, '15-17, place d Aligre', 1, 'pwd', 'troll2jeux@wanadoo.fr', 48.848650431, 2.37878983464, 'http://troll2jeux.com'),
('Substance Café', 'Nous proposons à la vente du café de spécialité torréfié sur place en grains et des accessoires pour faire du café (moulin, filtres, etc.)', 75002, '30 rue Dussoubs', 1, 'pwd', 'contact@substancecafe.com', 48.8662587148, 2.34917247376, 'https://www.substancecafe.com'),
('PIPELINE Store Bastille', 'La sélection de cigarettes électroniques et eliquides pour le débutant jusqu à l utilisateur avancé.', 75004, '43 bis boulevard Henri IV', 1, 'pwd', 'sav@fr-pipeline.com', 48.85274169, 2.36721256624, 'http://www.pipeline-store.fr'),
('I.B.U', 'Bar & Cave à Bières artisanales. \nNous proposons un service de Livraison dans Paris et de Click & Collect sur notre site internet', 75010, '20 cour des petites Ecuries', 1, 'pwd', 'bar@independentbrewsunited.fr', 48.8726136923, 2.35167424766, 'http://www.ibu.paris'),
('BACK IN BLACK', 'Torréfacteur depuis 2010 - Café en grains et café moulu fraîchement torréfié', 75011, '25 rue amelot', 1, 'pwd', 'coffee@kbcafeshop.com', 48.8562188725, 2.36902195643, 'https://kbcoffeeroasters.com/'),
('L ATELIER DU CHOCOLAT BASQUE', 'CHOCOLATIER : Livraison possible à partir de 50 € (règlements par chèques ou espèces)', 75015, '44 RUE DU COMMERCE', 1, 'pwd', 'rueducommerceparis@atelierduchocolat.com', 48.846720632, 2.29552186025, 'https://www.facebook.com/LAtelier-du-Chocolat-Paris-Commerce-106881157366641/'),
('Maison Balme', 'Charcuterie', 75006, '4-8 rue Lobineau', 1, 'pwd', 'paris@maisonbalme.com,k.ezcurra@balme.fr', 48.8517977263, 2.33617874988, 'https://www.epicery.com/epiceries/balme-saint-germain'),
('Rose et perle', 'Caviar', 75007, '27 Rue de Varenne', 1, 'pwd', 'jeanphilippe.chillet@yahoo.fr', 48.8539036955, 2.32398956076, 'https://www.epicery.com/epiceries/rose-et-perle'),
('Printemps du Goût', 'Chocolat', 75009, '115 Rue de Provence', 1, 'pwd', 'bdole@printemps.fr', 48.8741352566, 2.3279957859, 'https://www.epicery.com/epiceries/printemps-gout'),
('Cuistou', 'Brunch', 75011, '52 Rue Popincourt', 1, 'pwd', 'arthur.barbe@cuistou.fr', 48.8600555451, 2.37571739217, 'https://www.epicery.com/epiceries/cuistou'),
('Caviar Latian', 'Caviar', 75016, '36 Rue de l Annonciation', 1, 'pwd', 'contact@caviarlatian.fr', 48.857258097, 2.27846882812, 'https://www.epicery.com/epiceries/caviar-latian'),
('Compagnie Générale de la Biscuiterie', 'Chocolat', 75018, '1 Rue Constance', 1, 'pwd', 'alain.delarochere@gmail.com', 48.8852047764, 2.33367359492, 'https://www.epicery.com/epiceries/cie-generale-biscuiterie'),
('Ava and Mr joe', 'Jeux et jouets pour enfants de 0 à 12 ans.', 75011, '36 bis rue de montreuil', 1, 'pwd', 'Karine@ava-and-mr-joe.fr', 48.8503854906, 2.38670975724, 'https://www.ava-and-mr-joe.fr');

-- linking stores with their categories
INSERT INTO CommerceCategorie(cid, catid) VALUES (1, 6), (2, 6), (3, 1), (4, 1),(5, 1),
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
(17, 1),
(18, 1),
(19, 6),
(20, 5),
(21, 5),
(22, 4),
(23, 6),
(24, 5),
(25, 7),
(26, 4),
(27, 4),
(28, 5),
(29, 5),
(30, 5),
(31, 7),
(32, 6),
(33, 4),
(34, 5),
(35, 6),
(36, 4),
(37, 7),
(38, 6),
(39, 4),
(40, 6),
(41, 4),
(42, 4),
(43, 6),
(44, 6),
(45, 6),
(46, 6),
(47, 4),
(48, 6),
(49, 6),
(50, 6),
(51, 7),
(52, 6),
(53, 6),
(54, 6),
(55, 4),
(56, 4),
(57, 4),
(58, 4),
(59, 4),
(60, 4),
(61, 4),
(62, 5),
(63, 7);

-- one or two promotions
INSERT INTO Promotion(cid, pdescription, tdebut, tfin) VALUES (1, 'Un diplôme pas cher!', '2021-01-14'::DATE, NULL),
(2, 'Une chambre en plein Paris pour moins de 400€/mois', '2019-09-15', '2021-04-15'),
(3, 'Des wok de qualité avec formule étudiant à 9€', '2021-01-15', NULL),
(5, 'Des prix toujours imbattables', NULL, NULL),
(6, 'Plat du jour a 12€', NULL, NULL),
(4, 'La formule a 8€ passe a 6€ pour les trois prochaines semaines', '2021-02-10', '2021-02-25');

-- calvin loves food 
INSERT INTO ClientCategorie(clid, catid) VALUES (4, 1), (1, 3);

-- calvin loves mario's pizzas
INSERT INTO ClientFavCommerce(clid, cid) VALUES (4, 4), (2, 1), (3, 2); 

INSERT INTO Admins(adminemail, adminmdp) VALUES ('sebastian.partarrieu@mines-paristech.fr', 'amazingpassword');

INSERT INTO ImagePromotion ( imgname,ranks, verified, pid) VALUES
('mines_2.jpeg' , 1 ,FALSE, 1),
( 'meuh.jpeg' , 1 ,FALSE, 2),
('wok.jpeg', 1, FALSE, 3),
('mc_do_promo.jpeg', 1, FALSE, 4),
('gastronomie.jpeg', 1, FALSE, 5),
('nouille.jpeg', 1, FALSE, 6);

INSERT INTO ImageCommerce(imgname,ranks, verified, cid) VALUES
('mc_do.png' , 1 ,FALSE, 5),
('mc_do_2.jpeg', 2, FALSE, 5),
('mines_1.jpeg', 1, FALSE, 1),
('mines_2.jpeg', 2, FALSE, 1),
('maison_mines.jpeg', 1, FALSE, 2),
('muraille_phoenix.jpeg', 1, FALSE, 4),
('panda_wok.jpeg', 1, FALSE, 3);


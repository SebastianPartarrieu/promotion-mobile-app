# Promotion
Développement d'une application pour mettre en relation les petits commercants avec les consommateurs.

Depuis 20 ans, le monde du numérique a fait exploser la transition digitale des commerces, offrant de multiples solutions comme le ecommerce, le click&collect ou la livraison à domicile. Le parfait exemple est bien sur amazon. Bien que cette sur-digitalisation a créé des solutions bien plus confortables pour les consommateurs, elle a également mis dans l'ombre des acteurs plus locaux comme les commerces de proximité et a anéanti plus ou moins la notion de commerces de quartier. Monquartier a donc pour but de permettre à ces acteurs de redynamiser meur activité. Le but est donc de proposer une solution simple et globale aux commerces pour mettre en avant des pomotions pour certaines périodes ou un certain type de clients. Et de l'autre côté, cela permet aux clients de voir quels commerces se situent autour d'eux et quelles promotions leur sont accordées.

## Développement back-end
Le back-end est écrit en python avec l'aide du module Flask.
- app.py: gère l'ensemble des reqûete HTTP envoyé depuis le front-end vers le serveur. Il utilise pyjwt pour gérer les JSON Web Token (à la base de l'authentification et l'authorization de l'application). Utilisation de werkzeug pour hasher les mots de passe dans la base de données. Utilisation de Nominatim pour traduire une addresse en géolocalisation.
- queries.sql: Utilisation de anodb pour se connecter avec la bdd psql, les requêtes SQL sont donc implémenté dans un ce fichier queries.sql a part.
- data.sql: Données utilisées initialement, pour effectuer une démo. La plupart des commerces rentrés ont été récoltés à l'aide de 
https://data.iledefrance.fr/pages/home-covid/ qui met généreusement à disposition des données concernant les commerces. Un petit peu de refactoring a été effectué pour pouvoir mettre proprement ces données dans notre base.
- drop.sql: Permet de drop toutes les relations de la base. Utile en développement.
- truncate.sql: Nettoie les données à l'intérieur des tables sans pour autant supprimer les tables.
- app.conf: garde des variable d'intéret 
- makefile: automatiser un ensemble de choses utiles (run l'application, clean les données, stop ...) 'make run' 'make clean' 'make stop'

## Développement front-end
Développement en React.

## Utilisation de l'application
Images à inclure et petit tuto d'utilisation.



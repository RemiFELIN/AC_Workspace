# GUS : v1

![Exécution du programme](https://github.com/RemiFELIN/AC_Workspace/blob/main/agents/gus/img/gus_v1_output.png)

Cet agent a été réalisé dans le but de proposer à l'utilisateur la possibilité de réserver un vol de manière
interactive. Le processus suit le plan suivant :

![schema](https://github.com/RemiFELIN/AC_Workspace/blob/main/agents/gus/img/schema.png)

Je l'ai implémenté de sorte à ce que le dialogue soit fluide et claire, de plus les dernières fonctionnalités 
implémentées permettent à l'agent de pouvoir vérifier si l'utilisateur fait des erreurs :

- Si l'utilisateur soumet la même ville d'arrivée que celle de départ
- Si l'utilisateur ne soumet pas de date valide
- Si la date de départ est inférieure à celle d'aujourd'hui
- Si la date d'arrivée est inférieure à celle de la date de départ 
- ...

Un petit résumé de la conversation sera proposé à la fin du processus.

# GUS : v2

![Exécution du programme](https://github.com/RemiFELIN/AC_Workspace/blob/main/agents/gus/img/gus_v2_output.png)

Cette version a été implémenté de sorte à ce que celle-ci utilise le même système de "frame" abordé lors des séances
de cours. Je trouve cette solution plus élégante même si on aurait pu pousser les performances du programme un peu plus 
loin. Par exemple, utiliser NLTK ou SpaCy pour détecter les mots simplement et retirer le système des regex

Les regex sont assez performant si on respecte un format de message identique à celui présent sur l'exemple ci-dessus. 
Ils montrent évidemment leur limites dans des cas plus complexes.

Nous pouvons toutefois enchaîner les informations dans nos messages (comme sur l'exemple ci-dessus), celles-ci vont être 
récupéré et traité par le système.

Un petit résumé de la conversation sera proposé à la fin du processus.
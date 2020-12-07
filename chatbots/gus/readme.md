# GUS

![Exécution du programme](https://github.com/RemiFELIN/AC_Workspace/blob/main/chatbots/gus/img/gus_output.png)

Cet agent a été réalisé dans le but de proposer à l'utilisateur la possibilité de réserver un vol de manière
interactive. Le processus suit le plan suivant :

![schema](https://github.com/RemiFELIN/AC_Workspace/blob/main/chatbots/gus/img/schema.png)

Je l'ai implémenté de sorte à ce que le dialogue soit fluide et claire, de plus les dernières fonctionnalités 
implémentées permettent à l'agent de pouvoir vérifier si l'utilisateur fait des erreurs :

- Si l'utilisateur soumet la même ville d'arrivée que celle de départ
- Si l'utilisateur ne soumet pas de date valide
- Si la date de départ est inférieure à celle d'aujourd'hui
- Si la date d'arrivée est inférieure à celle de la date de départ 
- ...

Un petit résumé de la conversation sera proposé à la fin du processus.
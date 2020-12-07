# Agent reflexe basé sur des modèles et des buts

![Exécution du programme](https://github.com/RemiFELIN/AC_Workspace/blob/main/agents/agent_reflexe_modele_but/img/agent_reflexe_modele_but_output.png)

Le programme a été conçu pour être paramétrable à souhait :

- Vous pouvez choisir le nombre de salles à insérer dans l'environnement
- Vous pouvez choisir le nombre d'itérations (correspondant aux nombres d'actions de l'agent)

Ici, nous avons un but prédéfini qui est le suivant : "Si l'un de ces chemins est propre, alors l'agent a atteint son but"

Voici le schéma implémenté dans le programme :



En outre, l'agent va effectuer les actions selon le modèle précisé dans les diapo traitant de ce sujet. 
Les éléments suivants ont été ajouté pour rendre l'expérience plus agréable:

- Des retours sur chaques actions de l'agents avec sa position dans l'environnement
- Des retours sur la mémoire interne de l'agent avec des statistiques sur les actions de l'agent
- Des retours sur la 
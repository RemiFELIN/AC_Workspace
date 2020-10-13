import random
import string

### VARIABLES SIMULATIONS
NB_PIECES = 2
NB_ITERATIONS = 10

### VARIABLES STATIQUES
PIECE_SALE = 1
PIECE_PROPRE = 0

TOURNER_DROITE = "droite"
TOURNER_GAUCHE = "gauche"
ASPIRER_SALLE = "aspire"

### AGENT
position_agent = 0
perception = []

### ENVIRONNEMENT
salles = []
nom_salles = string.ascii_uppercase[:NB_PIECES]

# On génère l'environnement de manière aléatoire
for i in range(0, NB_PIECES):
    etat = random.randint(PIECE_PROPRE, PIECE_SALE)
    salle = nom_salles[i]
    salles.append([salle, etat])

# On défini de manière aléatoire la position_agent de l'agent
position_agent = int(random.uniform(0, NB_PIECES))


def agent_aspirateur_reflexe_modele(tab):
    if tab[1] == PIECE_SALE:
        return ASPIRER_SALLE
    else:
        if salles[tab[0]][0] == salles[0][0]:
            return TOURNER_DROITE
        else:
            return TOURNER_GAUCHE


def simulation():
    global position_agent
    # [emplacement, état]
    action = agent_aspirateur_reflexe_modele([position_agent, salles[position_agent][1]])
    # On applique les règles
    appliquer_regles(action)


def appliquer_regles(action):
    global position_agent
    if action == ASPIRER_SALLE:
        perception.append([nom_salles[position_agent], ASPIRER_SALLE])
        salles[position_agent][1] = PIECE_PROPRE
    elif action == TOURNER_GAUCHE:
        perception.append([nom_salles[position_agent], TOURNER_GAUCHE])
        position_agent -= 1
    elif action == TOURNER_DROITE:
        perception.append([nom_salles[position_agent], TOURNER_DROITE])
        position_agent += 1


def get_resume_agent(tab):
    i = 1
    print("----------------------")
    print("- MEMOIRE DE L'AGENT -")
    print("----------------------\n")
    print("Résumé:")
    for action in tab:
        if action[1] == "aspire":
            print("{}> J'ai {} dans la salle {}".format(i, action[1], action[0]))
            i += 1
        else:
            print("{}> Je suis dans la salle {} et je tourne à {}".format(i, action[0], action[1]))
            i += 1


# SIMULATION
i = 5
while i < NB_ITERATIONS:
    simulation()
    i += 1
# Pour afficher la mémoire de l'agent -> touche perso :)
get_resume_agent(perception)

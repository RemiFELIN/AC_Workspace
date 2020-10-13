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
RIEN_FAIRE = "rien"

### AGENT
position_agent = 0

### ENVIRONNEMENT
salles = []
str = string.ascii_uppercase[:NB_PIECES]
# On génère l'environnement de manière aléatoire
for i in range(0,NB_PIECES):
    etat = random.randint(PIECE_PROPRE, PIECE_SALE)
    salle = str[i]
    salles.append([salle, etat])
# TEST
print("[INIT] Gén. salles: ", salles)

# On défini de manière aléatoire la position_agent de l'agent
position_agent = int(random.uniform(0, NB_PIECES))

def agent_aspirateur_reflexe(tab):
    if tab[1] == PIECE_SALE:
        print("[pos:{}] > J'{}".format(tab[0], ASPIRER_SALLE))
        return ASPIRER_SALLE
    elif salles[tab[0]][0] == salles[0][0]:
        print("[pos:{}] > Je vais à {}".format(tab[0], TOURNER_DROITE))
        return TOURNER_DROITE
    else:
        print("[pos:{}] > Je vais à {}".format(tab[0], TOURNER_GAUCHE))
        return TOURNER_GAUCHE

def simulation():
    global position_agent
    # [emplacement, état]
    action = agent_aspirateur_reflexe([position_agent, salles[position_agent][1]])
    if action == ASPIRER_SALLE:
        salles[position_agent][1] = PIECE_PROPRE
    elif action == TOURNER_GAUCHE:
        position_agent -= 1
    elif action == TOURNER_DROITE:
        position_agent += 1

# SIMULATION
i = 5
while i < NB_ITERATIONS:
    simulation()
    i += 1
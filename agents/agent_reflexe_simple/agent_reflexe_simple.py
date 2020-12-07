import random
import string

# VARIABLES SIMULATIONS
NB_PIECES = 10
NB_ITERATIONS = 20

# VARIABLES STATIQUES
PIECE_SALE = 1
PIECE_PROPRE = 0
TOURNER_DROITE = "droite"
TOURNER_GAUCHE = "gauche"
ASPIRER_SALLE = "aspire"
RIEN_FAIRE = "rien"

# AGENT
position_agent = 0

# ENVIRONNEMENT
salles = []
nom_salles = string.ascii_uppercase[:NB_PIECES]
# On génère l'environnement de manière aléatoire
for i in range(0, NB_PIECES):
    etat = random.randint(PIECE_PROPRE, PIECE_SALE)
    salles.append([nom_salles[i], etat])

# On défini de manière aléatoire la position_agent de l'agent
position_agent = int(random.uniform(0, NB_PIECES))


def agent_aspirateur_reflexe(tab):
    # Retourne une action : aspirer ; tourner à gauche ou tourner à droite
    pos = nom_salles[tab[0]]
    if tab[1] == PIECE_SALE:
        print("[pos:{}] > J'{}".format(pos, ASPIRER_SALLE))
        return ASPIRER_SALLE
    elif tab[0] == 0:
        print("[pos:{}] > Je vais à {}".format(pos, TOURNER_DROITE))
        return TOURNER_DROITE
    elif tab[0] == NB_PIECES-1:
        print("[pos:{}] > Je vais à {}".format(pos, TOURNER_GAUCHE))
        return TOURNER_GAUCHE
    else:
        # Déplacement aléatoire
        if random.random() < 0.5:
            print("[pos:{}] > Je vais à {}".format(pos, TOURNER_GAUCHE))
            return TOURNER_GAUCHE
        else:
            print("[pos:{}] > Je vais à {}".format(pos, TOURNER_DROITE))
            return TOURNER_DROITE


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
print("\n[INIT] Gén. salles: ", salles, "\n")

print("Début de la simulation ...\n")
i = 0
while i < NB_ITERATIONS:
    simulation()
    i += 1
print("\nFin de la simulation !")

print("\n[END] Etats des salles: ", salles, "\n")

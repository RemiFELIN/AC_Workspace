import random
import string

# VARIABLES SIMULATIONS
NB_PIECES = 10
NB_ITERATIONS = 10

# STATIQUES
PIECE_SALE = 1
PIECE_PROPRE = 0

TOURNER_DROITE = "droite"
TOURNER_GAUCHE = "gauche"
ASPIRER_SALLE = "aspire"

# AGENT
position_agent = 0
perception = []

# ENVIRONNEMENT
salles = []
nom_salles = string.ascii_uppercase[:NB_PIECES]

# On génère l'environnement de manière aléatoire
for i in range(0, NB_PIECES):
    etat = random.randint(PIECE_PROPRE, PIECE_SALE)
    salles.append([nom_salles[i], etat])

# On défini de manière aléatoire la position_agent de l'agent
position_agent = int(random.uniform(0, NB_PIECES))


def agent_aspirateur_reflexe_modele(tab):
    pos = nom_salles[tab[0]]
    # Notre agent a maintenant conscience de ses actions, il sait s'il est dèjà allé dans une pièce donnée
    if nom_salles[tab[0]] in perception:
        # Nous sommes donc dans une salle déjà visité
        print("[pos:{}] > Je suis déjà allé dans cette salle !".format(pos))
        # Nous nous déplaçons donc de manière aléatoire avec les méthodes suivantes
    # Retourne une action : aspirer ; tourner à gauche ou tourner à droite
    if tab[1] == PIECE_SALE:
        print("[pos:{}] > J'{}".format(pos, ASPIRER_SALLE))
        return ASPIRER_SALLE
    elif tab[0] == 0:
        print("[pos:{}] > Je vais à {}".format(pos, TOURNER_DROITE))
        return TOURNER_DROITE
    elif tab[0] == NB_PIECES - 1:
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
    # Appel de la boucle principale et application des règles :
    global position_agent
    # [emplacement, état]
    action = agent_aspirateur_reflexe_modele([position_agent, salles[position_agent][1]])
    # On applique les règles
    appliquer_regles(action)


def appliquer_regles(action):
    global position_agent
    # Application des règles basiques
    # Nettoyer la pièce ; aller dans une autre pièce en tournant à droite ou à gauche
    if action == ASPIRER_SALLE:
        perception.append(nom_salles[position_agent])
        perception.append(ASPIRER_SALLE)
        salles[position_agent][1] = PIECE_PROPRE
    elif action == TOURNER_GAUCHE:
        perception.append(nom_salles[position_agent])
        perception.append(TOURNER_GAUCHE)
        position_agent -= 1
    elif action == TOURNER_DROITE:
        perception.append(nom_salles[position_agent])
        perception.append(TOURNER_DROITE)
        position_agent += 1


def get_resume_agent():
    nombre_piece_visite = len(list(set([x for x in perception if len(x) == 1])))
    print("\n----------------------")
    print("- MEMOIRE DE L'AGENT -")
    print("----------------------\n")
    print("Résumé:")
    print("> J'ai visité {} pièces".format(nombre_piece_visite))
    print("> J'ai aspiré {} fois".format(perception.count(ASPIRER_SALLE)))
    print("> J'ai tourné {} fois à gauche".format(perception.count(TOURNER_GAUCHE)))
    print("> J'ai tourné {} fois à droite".format(perception.count(TOURNER_DROITE)))


# SIMULATION
print("\n[INIT] Gén. salles: ", salles, "\n")

i = 1
print("Début de la simulation ...\n")
while i < NB_ITERATIONS:
    simulation()
    i += 1
print("\nFin de la simulation !")
# Pour afficher la mémoire de l'agent
get_resume_agent()

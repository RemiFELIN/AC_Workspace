import random
import string

# VARIABLES SIMULATIONS
NB_PIECES = 7
NB_ITERATIONS = 20

# VARIABLES STATIQUES
PIECE_SALE = 1
PIECE_PROPRE = 0
CHANGER_SALLE = "change de salle"
ASPIRER_SALLE = "aspire"

# AGENT
# La position de l'agent est fixée : il commence dans la salle A
position_agent = 0
perception = []
but_atteint = False

# ENVIRONNEMENT
salles = []
nom_salles = string.ascii_uppercase[:NB_PIECES]

# On génère l'environnement de manière aléatoire
for i in range(0, NB_PIECES):
    etat = random.randint(PIECE_PROPRE, PIECE_SALE)
    salles.append([nom_salles[i], etat])


def get_statut_salle(s):
    # On récupère l'état de la pièce au moment de
    # l'appel de la méthode
    return salles[nom_salles.index(s)][1]


def get_statut_chemin(chemin):
    # Chemin est un tableau de chemins possibles pour atteindre
    # la dernière salle, ainsi on retourne un tableau de l'état
    # du chemin
    statut = []
    for s in chemin:
        statut.append(get_statut_salle(s))
    return statut


def set_position_agent(pos):
    global position_agent
    # Mise à jour de la position de l'agent
    position_agent = pos


def verifier_but():
    global but_atteint
    # A -> B -> D -> F
    # A -> B -> C -> E -> G -> F
    # A -> C -> E -> G -> F
    # A -> C -> B -> D -> F
    # Si l'un de ces chemins est propre, alors l'agent a atteint son but
    if PIECE_SALE not in get_statut_chemin(["A", "B", "D", "F"]):
        but_atteint = True
    elif PIECE_SALE not in get_statut_chemin(["A", "C", "E", "G", "F"]):
        but_atteint = True


def changer_salle(pos):
    position = nom_salles[pos]
    nouvelle_position = 0
    salle_agent = nom_salles[pos]
    # Plusieurs chemins possibles pour aller à la salle F:
    # A -> B -> D -> F
    # A -> B -> C -> E -> G -> F
    # A -> C -> E -> G -> F
    # A -> C -> B -> D -> F
    # Son premier mouvement sera aléatoire : soit la salle B soit la salle C
    if salle_agent == "A":
        nouvelle_position = random.randint(1, 2)
        print("[pos:{}] > Je vais dans la salle {}".format(position, nom_salles[nouvelle_position]))
    # Par contre, si son parcours est déjà amorcé : on doit appliquer le circuit
    elif salle_agent == "B":
        # Ici, soit la salle C soit la salle D
        nouvelle_position = random.randint(2, 3)
        print("[pos:{}] > Je vais dans la salle {}".format(position, nom_salles[nouvelle_position]))
    elif salle_agent == "C":
        # Ici, soit la salle B soit la salle E
        nouvelle_position = random.choice([1, 4])
        print("[pos:{}] > Je vais dans la salle {}".format(position, nom_salles[nouvelle_position]))
    elif salle_agent == "D":
        # On arrive forcément au point d'arrivé
        nouvelle_position = 5
        print("[pos:{}] > Je vais dans la salle {} et je termine mon parcours".format(
            position, nom_salles[nouvelle_position])
        )
    elif salle_agent == "E":
        # On arrive forcément vers la salle G
        nouvelle_position = 6
        print("[pos:{}] > Je vais dans la salle {}".format(position, nom_salles[nouvelle_position]))
    elif salle_agent == "G":
        # On arrive forcément au point d'arrivé
        nouvelle_position = 5
        print("[pos:{}] > Je vais dans la salle {} et je termine mon parcours".format(
            position, nom_salles[nouvelle_position])
        )
    # On set la nouvelle position de l'agent
    set_position_agent(nouvelle_position)


def agent_aspirateur_reflexe_modele(tab):
    if tab[1] == PIECE_SALE:
        return ASPIRER_SALLE
    else:
        # On change de salle
        return CHANGER_SALLE


def simulation():
    global position_agent
    # [emplacement, état]
    action = agent_aspirateur_reflexe_modele([position_agent, salles[position_agent][1]])
    # On applique les règles
    appliquer_regles(action)
    # Si on arrive au point d'arrivé (salle F) alors on peut arreter la simulation
    if nom_salles[position_agent] == "F":
        # On la nettoie si on vient juste d'arriver
        appliquer_regles(ASPIRER_SALLE)
        # On vérifie si le but fixé a été atteint
        verifier_but()
        return False
    return True


def appliquer_regles(action):
    # Application des règles basiques
    global position_agent
    if action == ASPIRER_SALLE:
        perception.append(nom_salles[position_agent])
        perception.append(ASPIRER_SALLE)
        salles[position_agent][1] = PIECE_PROPRE
        print("[pos:{}] > J'{} la salle".format(nom_salles[position_agent], ASPIRER_SALLE))
    elif action == CHANGER_SALLE:
        # On change de salle
        perception.append(nom_salles[position_agent])
        perception.append(CHANGER_SALLE)
        changer_salle(position_agent)


def get_resume_agent():
    nombre_piece_visite = len(list(set([x for x in perception if len(x) == 1])))
    print("\n----------------------")
    print("- MEMOIRE DE L'AGENT -")
    print("----------------------\n")
    print("Résumé:")
    print("> J'ai aspiré {} pièces sur les {} pièces que j'ai visité".format(
        perception.count(ASPIRER_SALLE), nombre_piece_visite)
    )
    if but_atteint:
        print("> J'ai atteint mon but car au moins un des chemins est propre")
    else:
        print("> Je n'ai pas atteint mon but ...")


# SIMULATION
print("\n[INIT] Gén. salles: ", salles, "\n")

i = 1
print("Début de la simulation ...\n")
while i < NB_ITERATIONS:
    if simulation() is False:
        break
    i += 1
print("\nFin de la simulation !")
# Pour afficher la mémoire de l'agent -> touche personnelle
get_resume_agent()

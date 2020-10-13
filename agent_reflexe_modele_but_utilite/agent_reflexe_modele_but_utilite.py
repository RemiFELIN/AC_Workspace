import random
import string

### VARIABLES SIMULATIONS
NB_PIECES = 7
NB_ITERATIONS = 10

### VARIABLES STATIQUES
PIECE_SALE = 1
PIECE_PROPRE = 0
CHANGER_SALLE = "change de salle"
ASPIRER_SALLE = "aspire"

### AGENT
# La position de l'agent est fixée : il commence dans la salle A
position_agent = 0
perception = []
but_atteint = False

### ENVIRONNEMENT
salles = []
nom_salles = string.ascii_uppercase[:NB_PIECES]

# On génère l'environnement de manière aléatoire
for i in range(0, NB_PIECES):
    etat = random.randint(PIECE_PROPRE, PIECE_SALE)
    salle = nom_salles[i]
    salles.append([salle, etat])

count_piece_salle = 0
# On compte le nombre de pièces salles à l'origine
for salle, etat in salles:
    if etat == PIECE_SALE:
        count_piece_salle += 1


def get_statut_salle(salle):
    return salles[nom_salles.index(salle)][1]


def get_statut_chemin(chemin):
    # Chemin est un tableau de chemins possibles pour atteindre
    # la dernière salle, ainsi on retourne un tableau de l'état
    # du chemin
    statut = []
    for salle in chemin:
        statut.append(get_statut_salle(salle))
    return statut


def set_position_agent(pos):
    global position_agent
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
    elif PIECE_SALE not in get_statut_chemin(["A", "B", "C", "E", "G", "F"]):
        but_atteint = True
    elif PIECE_SALE not in get_statut_chemin(["A", "C", "E", "G", "F"]):
        but_atteint = True
    elif PIECE_SALE not in get_statut_chemin(["A", "C", "B", "D", "F"]):
        but_atteint = True


def va_vers_la_poussiere(a, b):
    if salles[a][1] == PIECE_SALE and salles[b][1] == PIECE_SALE:
        return random.choice([a, b])
    elif salles[a][1] == PIECE_SALE:
        return a
    elif salles[b][1] == PIECE_SALE:
        return b
    else:
        return random.choice([a, b])


def changer_salle(pos):
    nouvelle_position = 0
    salle_agent = nom_salles[pos]
    # Plusieurs chemins possibles pour aller à la salle F:
    # A -> B -> D -> F
    # A -> B -> C -> E -> G -> F
    # A -> C -> E -> G -> F
    # A -> C -> B -> D -> F
    # Son premier mouvement sera aléatoire : soit la salle B soit la salle C
    if salle_agent == "A":
        nouvelle_position = va_vers_la_poussiere(1, 2)
    # Par contre, si son parcours est déjà amorcé : on doit appliquer le circuit
    elif salle_agent == "B":
        # Ici, soit la salle C soit la salle D
        nouvelle_position = va_vers_la_poussiere(2, 3)
    elif salle_agent == "C":
        # Ici, soit la salle B soit la salle E
        nouvelle_position = va_vers_la_poussiere(1, 4)
    elif salle_agent == "D":
        # On arrive forcément au point d'arrivé
        nouvelle_position = 5
    elif salle_agent == "E":
        # On arrive forcément vers la salle G
        nouvelle_position = 6
    elif salle_agent == "G":
        # On arrive forcément au point d'arrivé
        nouvelle_position = 5
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
        if salles[position_agent][1] == PIECE_SALE:
            appliquer_regles(ASPIRER_SALLE)
        # On vérifie si le but fixé a été atteint
        verifier_but()
        return False
    return True


def appliquer_regles(action):
    global position_agent
    if action == ASPIRER_SALLE:
        perception.append([nom_salles[position_agent], ASPIRER_SALLE])
        salles[position_agent][1] = PIECE_PROPRE
    elif action == CHANGER_SALLE:
        # On change de salle
        changer_salle(position_agent)
        perception.append([nom_salles[position_agent], CHANGER_SALLE])


def get_indicateur_utilite():
    global count_piece_salle
    count = 0
    # On compte le nombre de salles que l'agent a lavé
    for pos, act in perception:
        if act == ASPIRER_SALLE:
            count += 1
    return [count, count_piece_salle]


def get_resume_agent(percep):
    i = 1
    print("--------")
    print("L'utilite ici va etre de nettoyer un maximum de pièces durant le parcours du circuit\n")
    print("----------------------")
    print("- MEMOIRE DE L'AGENT -")
    print("----------------------\n")
    print("Résumé:\n")
    for action in percep:
        if action[1] == "aspire":
            print("{}> J'ai {} dans la salle {}".format(i, action[1], action[0]))
            i += 1
        else:
            print("{}> J'ai {} ! je suis maintenant dans la salle {}".format(i, action[1], action[0]))
            i += 1
    print("----------------------\n")
    if but_atteint is True:
        print("\n> J'ai atteint mon but ! au moins un des chemins du circuit est propre")
    # Indicateur utilite
    indic = get_indicateur_utilite()
    percent = (indic[0]*100)/indic[1]
    print("\n> J'ai nettoyé {} pièce(s) parmis les {} pièces qui été sale à l'origine, soit {}%".format(indic[0], indic[1], percent))
    if percent == 100.0:
        print("> Parfait ! :D")
    elif percent >= 60.0:
        print("> C'est pas mal du tout :)")
    else:
        print("> Peut mieux faire ! :(")

# SIMULATION
i = 1
while i < NB_ITERATIONS:
    if simulation() is False:
        break
    i += 1
# Pour afficher la mémoire de l'agent -> touche perso :)
get_resume_agent(perception)
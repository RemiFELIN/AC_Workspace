import time
import random
import re
import datetime

user_template = "> "
bot_template = "[BOT] {}"

username = None

# Informations de l'agent
# Travel = ["ville de depart", "ville d'arrivee"]
voyage = [None] * 2
# Aller simple ou aller-retour
is_aller_simple = None
# Date de départ
date_depart = None
# Date d'arrivee
date_arrivee = None


def find_name(message):
    # à l'aide des regex, nous allons rechercher le nom de l'utilisateur
    # cela rend l'agent plus amical
    name = None
    name_keyboard = re.compile("name|call")
    capitalized_name = re.compile("[A-Z]{1}[a-z]*")
    if name_keyboard.search(message):
        name_word = capitalized_name.findall(message)
        if len(name_word) > 0:
            name = ' '.join(name_word)
    return name


def respond(message):
    global username
    name = find_name(message)
    if name is not None:
        username = name
        # Neutral response
        bot_talk("Hello, {} !".format(name))
        return


def send_message(message):
    respond(message)


def bot_talk(msg):
    time.sleep(0.5)
    print(bot_template.format(msg))
    time.sleep(0.25)


def build_reservation():
    # Voici la boucle principale de notre programme :
    # Il va nous permettre une interaction fluide avec l'agent pour réserver un vol
    # Les boucles traduisent le déroulement normal de la discussion : nous pouvons
    # interrompre le programme en tapant "exit"
    # Par défaut, le programme s'arrête quand nous avons fini le dialogue

    # Le plus de ce code : la vérification des réponses fournis par l'utilisateur

    global voyage, date_depart, date_arrivee, is_aller_simple
    # What city are you leaving from ?
    bot_talk("What city are you leaving from ?")
    msg = input(user_template)
    voyage[0] = msg
    # Where are you going ?
    bot_talk("Where are you going ?")
    i = False
    while i is False:
        msg = input(user_template)
        if msg != voyage[0]:
            voyage[1] = msg
            i = True
        else:
            bot_talk("It would be more profitable not to take tickets to stand still")
            bot_talk("Where are you going ?")
    # What date do you want to leave ?
    # Today or not ?
    bot_talk("Do you want to leave today ?")
    pattern = re.compile(r'[2-9][0-9][0-9][0-9]-[0-9][0-9]-[0-3][0-9]')
    t = False
    while t is False:
        msg = input(user_template)
        if "yes" in msg.lower():
            date_depart = str(datetime.date.today())
            t = True
        elif "no" in msg.lower():
            bot_talk("What date do you want to leave ? (YYYY-mm-dd)")
            k = False
            while k is False:
                msg = input(user_template)
                submission = pattern.findall(msg)
                if len(submission) != 0:
                    date_depart = submission[0]
                    if str(datetime.date.today()) > date_depart:
                        bot_talk("You can't leave from the past")
                        bot_talk("What date do you want to leave ? (YYYY-mm-dd)")
                    else:
                        k = True
                else:
                    bot_talk("Incorrect format ! try again...")
            t = True
        else:
            bot_talk("Please, respond at my request !")
    # Is it a one-way trip ?
    bot_talk("Is it a one-way trip ?")
    t = False
    while t is False:
        msg = input(user_template)
        if "yes" in msg.lower():
            is_aller_simple = True
            # If yes, do you want to go from <FROM> to <TO> on <DATE>?
            bot_talk("Do you want to go from {} to {} on {} ?".format(
                voyage[0],
                voyage[1],
                date_depart
            ))
            k = False
            while k is False:
                msg = input(user_template)
                if "yes" in msg.lower():
                    book_a_flight()
                    return True
                elif "no" in msg.lower():
                    cancel()
                    # Recursivity
                    build_reservation()
                else:
                    bot_talk("Please, respond at my request !")
            t = True
        elif "no" in msg.lower():
            is_aller_simple = False
            bot_talk("What date do you want to return ? (YYYY-mm-dd)")
            pattern = re.compile(r'[2-9][0-9][0-9][0-9]-[0-9][0-9]-[0-3][0-9]')
            k = False
            while k is False:
                msg = input(user_template)
                submission = pattern.findall(msg)
                if len(submission) != 0:
                    date_arrivee = submission[0]
                    if date_arrivee < date_depart:
                        bot_talk("Oops, do you want to arrive before you even leave ?")
                        bot_talk("What date do you want to return ? (YYYY-mm-dd)")
                    else:
                        # Do you want to go from <FROM> to <TO> on <DATE> returning on <RETURN>
                        bot_talk("Do you want to go from {} to {} on {} returning on {} ?".format(
                            voyage[0],
                            voyage[1],
                            date_depart,
                            date_arrivee
                        ))
                        l = False
                        while l is False:
                            msg = input(user_template)
                            if "yes" in msg.lower():
                                book_a_flight()
                                return True
                            elif "no" in msg.lower():
                                cancel()
                            else:
                                bot_talk("Please, respond at my request !")
                else:
                    bot_talk("Incorrect format ! try again...")
            t = True
        else:
            bot_talk("Please, respond at my request !")


def cancel():
    bot_talk("Okay, you are complex...")
    # Recursivity
    build_reservation()


def book_a_flight():
    bot_talk("Okay ! it's good")
    if is_aller_simple is True:
        bot_talk("I resume ... Your flight : {} -> {} for {}\nGood flight !".format(
            voyage[0],
            voyage[1],
            date_depart
        ))
    else:
        bot_talk("I will resume ...")
        bot_talk("Your flight : {} -> {} for {}".format(voyage[0], voyage[1], date_depart))
        bot_talk("You return at {} for {} !".format(voyage[0], date_arrivee))
        bot_talk("Good flight")


######################################################
# SIMULATION
######################################################
bot_talk("Please, give me your name to begin discuss")
while username is None:
    msg = input(user_template)
    respond(msg)
    if msg == "exit":
        bot_talk("Goodbye !")
        bool = True
    elif username is None:
        bot_talk("It's not correct, try with 'my name is [A-Z]*'")
t = False
while t is False:
    t = build_reservation()

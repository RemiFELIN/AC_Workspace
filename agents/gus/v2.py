import time
import random
import re
import datetime
import json
import calendar

user_template = "> "
bot_template = "[BOT] {}"

# FRAME
with open("data/frame.json") as json_file:
    frame = json.load(json_file)

# GUS
intro = "Hello, my name is Gus, I hope to be able to help you book the flight you want."
end = "I will resume, you leave at {} from {} on an {} plane to {}, " \
      "you return on {} at {}, is this correct? "


# you leave at [departure time] from [departure city] on an [airline] plane to [arrival city], you return on [arrival
# date] at [arrival time], is this correct?

# Evolution possible : récupérer le sens des mots avec Spacy ou nltk par exemple


def bot_talk(msg):
    time.sleep(0.5)
    print(bot_template.format(msg))
    time.sleep(0.25)


# récupérer les mots clés
def find_keywords(message):
    # à l'aide des regex, nous allons rechercher les mots clés (en majuscule)
    capitalized_word = re.compile("[A-Z][a-z]*")
    keywords = []
    words = capitalized_word.findall(message)
    if len(words) > 0 and "I" not in words:
        for word in words:
            keywords.append(word)
        return keywords
    return None


# récupérer la ville mentionnée dans le message
def find_city(msg):
    rgx_complex_city = re.compile(r"[A-Z][a-z]*\s[A-Z][a-z]*((\s)|)")
    # Exemple : San Diego
    rgx_city = re.compile(r"[A-Z][a-z]*")
    cities = []
    complex_city = rgx_complex_city.search(msg)
    if complex_city is not None:
        for element in complex_city.group().split(" "):
            if element in list(calendar.day_name):
                # Fix error
                basic_city = rgx_city.search(msg)
                if basic_city is not None:
                    return basic_city.group()
        return complex_city.group()
    else:
        basic_city = rgx_city.search(msg)
        if basic_city is not None:
            return basic_city.group()


# récupérer les heures mentionnées dans le message
def find_hour(msg):
    rgx = re.compile(r"[0-2][0-9]:[0-5][0-9]\s[ap]m")
    result = rgx.search(msg)
    if result is not None:
        return result.group()


# récupérer une date dans le message
def find_date(msg):
    date = re.compile(r"[A-Z][a-z]*\s[A-Z][a-z]*\s([0-9]|[0-2][0-9]|[3][0-1])(\s|$)")
    result = date.search(msg)
    if result is not None:
        return result.group()


# trouver la compagnie
def find_airline(msg):
    list_arlines = frame[4]["keywords"]
    for elem in list_arlines:
        if elem in msg:
            return elem


# On complète la mémoire de l'agent:
memoire = {
    "ORIGIN": None,
    "DEST": None,
    "DEP DATE": None,
    "DEP TIME": None,
    "ARR DATE": None,
    "ARR TIME": None,
    "AIRLINE": None
}


# Analyse du message par l'agent
def analyze(msg):
    # On cherche une ou deux villes éventuellement présentes dans le message
    city = find_city(msg)
    # On cherche une ou deux dates éventuellement présentes dans le message
    date = find_date(msg)
    # On cherche une ou deux heures éventuellement présentes dans le message
    hour = find_hour(msg)
    # On cherche une companie éventuellement présente dans le message
    airline = find_airline(msg)
    # Si on a des informations concernant city, dates et / ou hour, on met à jour la mémoire
    # Quelques règles :
    if date is not None and city in date:
        city = None
    if airline is not None and airline in city:
        city = None
    # print(city, "|", date, "|", hour, "|", airline)
    return city, date, hour, airline


def ask_question():
    for el in memoire:
        if memoire.get(el) is None:
            # On itére dans notre objet json
            for i in range(len(frame)):
                if frame[i]["slot"] == el:
                    bot_talk(random.choice(frame[i]["question"]))
                    return el, i


def is_finish():
    for el in memoire:
        if memoire.get(el) is None:
            return False
    return True


# SIMULATION
bot_talk(intro)
msg = ""
while True:
    # On peut enchainer les villes, date et heure tel que :
    # "i would like to go at San Diego for Wednesday May 28 at 23:45 pm"
    slot, index = ask_question()
    msg = input(user_template)
    tup = analyze(msg)
    tup = tuple(x for x in tup if x is not None)
    for elem in tup:
        memoire.update({str(frame[index]["slot"]): elem})
        index += 1
    # print(memoire)
    if is_finish():
        bot_talk(end.format(memoire.get("DEP TIME"), memoire.get("ORIGIN"), memoire.get("AIRLINE"),
                            memoire.get("DEST"), memoire.get("ARR DATE"), memoire.get("ARR TIME")))
        msg = input(user_template)
        if "yes" in msg:
            break

bot_talk("It was a pleasure, bye !")

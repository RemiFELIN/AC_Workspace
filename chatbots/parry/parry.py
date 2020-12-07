import time
import random
import re

# Ce bot est inspiré du chatbox "Eliza" développé un peu plus tôt
# Sont ajouté dans cette version une implémentation simple d'une personnalité à notre chatbo
# Les principaux concepts ont été implémenté ci-dessous

user_template = "> "
bot_template = "[BOT] {}"

username = "Rémi"
weather = ["cloudy", "rainy", "sunny", "windy", "gusty"]
perception = []
tolerance = 3
stop_discussion = False
talked = False

LVL_COLERE_PEUR, LVL_MEFIANCE, LVL_AMOUR = 0, 0, 0
MAX_PEUR_COLERE, MAX_MEFIANCE, MAX_AMOUR = 20, 15, 15

key_angry = ["bookmaker", "money", "bet", "angry", "fulconis"]
key_bully = ["bad", "hate", "low", "poor", "annoying", "kill"]
key_compliment = ["good", "well", "nice", "pretty"]
key_love = ["appareance", "family", "education"]
key_afraid = ["mafia", "gun", "vendetta", "kill"]

# Define a dictionary containing a list of responses for each message
responses = {
    "name": [
        "my name is Parry",
        "they call me Parry",
        "the name's Ry, Parry !"
    ],
    "weather": [
        "the weather is {}".format(random.choice(weather)),
        "it's {} today".format(random.choice(weather))
    ],
    "repeat": "You are so annoying to talk about {} everytime !"
}


def find_name(message):
    name = None
    name_keyboard = re.compile("name|call")
    capitalized_name = re.compile("[A-Z][a-z]*")
    if name_keyboard.search(message):
        name_word = capitalized_name.findall(message)
        if len(name_word) > 0:
            name = ' '.join(name_word)
    return name


def respond(message):
    time.sleep(1)
    # Nom
    name = find_name(message)
    if name is not None:
        return bot_talk("Hello, {0}!".format(name))
    elif "weather" in message:
        return bot_talk(random.choice(responses["weather"]))
    elif "name" in message and "?" in message:
        return bot_talk(random.choice(responses["name"]))
    elif "yes" == message.lower() or "no" == message.lower():
        return bot_talk("Why ?")
    else:
        output = replace_pronouns(message)
        if "hello" in output:
            return bot_talk(output)
        return bot_talk(output + "?")


# Define replace_pronouns()
def replace_pronouns(message):
    if 'I' in message:
        output = re.sub('I', 'You', message)
        if 'am' in message:
            return re.sub('am', 'are', output)
        else:
            return output
    message = message.lower()
    if 'me' in message:
        # Replace 'me' with 'you'
        return re.sub('me', 'you', message)
    if 'my' in message:
        # Replace 'my' with 'your'
        return re.sub('my', 'your', message)
    if 'your' in message:
        # Replace 'your' with 'my'
        return re.sub('your', 'my', message)
    if 'you' in message:
        # Replace 'you' with 'me'
        return re.sub('you', 'me', message)
    if 'am' in message:
        return re.sub('am', 'are', message)
    return message


def send_message(message):
    # print(user_template.format(message))
    update_perception(message)
    # Si on se répète sur des concepts
    if perception.count(tolerance) != 0:
        repeated_word = perception[perception.index(tolerance) - 1]
        bot_talk(responses["repeat"].format(repeated_word))
    # return false if discuss must be ended
    # print(user_template.format(message))
    update_states(message)
    respond(message)
    time.sleep(1)


def update_perception(message):
    capitalized_name = re.compile("[A-Z][A-Za-z]*")
    for concept in capitalized_name.findall(message):
        if concept in perception:
            perception.append(concept)
            perception.append(perception.count(concept))
        else:
            perception.append(concept)


def up_value(var, val):
    var += val
    return var


def update_states(message):
    message = message.lower()
    # Will respond at your message
    global LVL_MEFIANCE, LVL_COLERE_PEUR, LVL_AMOUR
    # He's afraid about mafia, angry about bookmaker, like horseraces
    strMsg = message.split()
    for str in strMsg:
        if str in key_angry:
            LVL_COLERE_PEUR = up_value(LVL_COLERE_PEUR, 5)
            rules_states()
            for s in strMsg:
                if s in key_bully:
                    LVL_COLERE_PEUR = up_value(LVL_COLERE_PEUR, 10)
                    rules_states()
                    bot_talk("What do you said ???")
            bot_talk("Don't talk about {}".format(str))
        elif str in key_afraid:
            LVL_MEFIANCE = up_value(LVL_MEFIANCE, 5)
            rules_states()
            for s in strMsg:
                if s in key_bully:
                    LVL_MEFIANCE = up_value(LVL_MEFIANCE, 10)
                    rules_states()
                    bot_talk("I didn't come here to suffer okay?")
            bot_talk("{} afraid me ...".format(str))
        elif str in key_bully:
            LVL_COLERE_PEUR = up_value(LVL_COLERE_PEUR, 5)
            rules_states()
            for s in strMsg:
                if s in key_love:
                    LVL_COLERE_PEUR = up_value(LVL_COLERE_PEUR, 10)
                    rules_states()
                    bot_talk("{} ???".format(str))
                elif s in key_angry:
                    bot_talk("Don't talk about this...")
            bot_talk("Calm down please ...")
        elif str in key_love:
            LVL_AMOUR = up_value(LVL_AMOUR, 5)
            rules_states()
            for s in strMsg:
                if s in key_compliment:
                    LVL_AMOUR = up_value(LVL_AMOUR, 10)
                    rules_states()
                    bot_talk("Wow you are too good !")
            bot_talk("C'est bieng !")


def log_states():
    print("\n>>> peur/méfiance: {} - mefiance: {} - amour: {}\n".format(LVL_COLERE_PEUR, LVL_MEFIANCE, LVL_AMOUR))


def rules_states():
    # return false if discuss must be ended
    global LVL_MEFIANCE, LVL_COLERE_PEUR, LVL_AMOUR, stop_discussion
    # Rules for max range of different mood
    if LVL_MEFIANCE >= MAX_MEFIANCE:
        LVL_MEFIANCE = MAX_MEFIANCE
        customize_responses()
        stop_discussion = True
    if LVL_COLERE_PEUR >= MAX_PEUR_COLERE:
        LVL_COLERE_PEUR = MAX_PEUR_COLERE
        customize_responses()
        stop_discussion = True
    if LVL_AMOUR >= MAX_AMOUR:
        LVL_AMOUR = MAX_AMOUR
        customize_responses()
        stop_discussion = True


def customize_responses():
    global username
    if username is None:
        username = "Anonymous user"
    # return a break (if false) or continue discuss (if true)
    if LVL_AMOUR == MAX_AMOUR:
        bot_talk("Wow... {}, would you being my friend ?".format(username))
        response = input(user_template)
        if response == "no":
            bot_talk(":(")
        elif response == "yes":
            bot_talk("Cool !")
        return True
    if LVL_MEFIANCE == MAX_MEFIANCE:
        bot_talk("You are too crazy {} ! bye !".format(username))
        return False
    if LVL_COLERE_PEUR == MAX_PEUR_COLERE:
        bot_talk("{} ... You are so annoying !".format(username))
        return False


def bot_talk(msg):
    global talked
    if not talked:
        print(bot_template.format(msg))
        talked = True


# SIMULATION
while stop_discussion is False:
    msg = input(user_template)
    if msg == "exit":
        bot_talk("Goodbye !")
        stop_discussion = True
    else:
        send_message(msg)
        talked = False

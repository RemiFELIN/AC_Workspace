import time
import random
import re

user_template = "[USER] "
bot_template = "[BOT] {}"

LVL_COLERE_PEUR = 0
LVL_MEFIANCE = 0
LVL_AMOUR = 0

MAX_PEUR_COLERE = 20
MAX_MEFIANCE = 15
MAX_AMOUR = 15

multi_responses = {
    "i like football": [
        "Me too !",
        "Ok, tell me more about "
    ],
    "Do you know Yan Fulconis ?": [
        "SoprYan !",
        "Yeah, Chiesa hates him a lot..."
    ],
    "If i talk about Jul, will you like it ?": [
        "x(..."
    ]
}

key_angry = ["bookmaker", "money", "bet", "angry", "fulconis"]
key_bully = ["bad", "low", "poor", "stfu", "kill"]
key_compliment = ["good", "well", "nice", "pretty"]
key_love = ["appareance", "family", "education"]
key_afraid = ["mafia", "gun", "vendetta", "kill"]

username = None


def find_name(message):
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
    time.sleep(1)
    name = find_name(message)
    if name is not None:
        username = name
        # Neutral response
        bot_talk("Hello, {} !".format(name))
        return
    for resp in multi_responses:
        response = resp.lower()
        if message.lower() == response:
            # With emotion
            bot_talk(random.choice(multi_responses[resp]))
            return
    else:
        bot_talk("I can hear you, you said " + message)
        return


def send_message(message):
    # return false if discuss must be ended
    # print(user_template.format(message))
    state_modify = update_states(message)
    if state_modify is False:
        respond(message)
    update = rules_states()
    if update is False:
        return False
    # To debug states
    # log_states()
    time.sleep(1)


def up_value(var, val):
    var += val
    return var


def update_states(message):
    message = message.lower()
    # Will respond at your message
    global LVL_MEFIANCE, LVL_COLERE_PEUR, LVL_AMOUR
    # He's afraid about mafia, angry about bookmaker, like horseraces
    strMsg = message.split()
    '''
    key_angry = ["bookmaker", "money", "bet"]
    key_bully = ["bad", "low", "poor", "stfu"]
    key_compliment = ["good", "well", "nice"]
    key_love = ["appareance", "family", "education"]
    key_afraid = ["mafia", "gun", "vendetta", "kill"]
    '''
    for str in strMsg:
        if str in key_angry:
            LVL_COLERE_PEUR = up_value(LVL_COLERE_PEUR, 1)
            for s in strMsg:
                if s in key_bully:
                    LVL_COLERE_PEUR = up_value(LVL_COLERE_PEUR, 5)
                    bot_talk("What do you said ???")
                    return True
            bot_talk("Don't talk about {}".format(str))
            return True
        elif str in key_afraid:
            LVL_MEFIANCE = up_value(LVL_MEFIANCE, 1)
            for s in strMsg:
                if s in key_bully:
                    LVL_MEFIANCE = up_value(LVL_MEFIANCE, 5)
                    bot_talk("I'm not here to suffer OKAY !?")
                    return True
            bot_talk("{} afraid me ...".format(str))
            return True
        elif str in key_bully:
            LVL_COLERE_PEUR = up_value(LVL_COLERE_PEUR, 1)
            for s in strMsg:
                if s in key_love:
                    LVL_COLERE_PEUR = up_value(LVL_COLERE_PEUR, 5)
                    bot_talk("{} ???".format(str))
                    return True
                elif s in key_angry:
                    bot_talk("Don't talk about this...")
                    return True
            bot_talk("bruuh calm down ...")
            return True
        elif str in key_love:
            LVL_AMOUR = up_value(LVL_AMOUR, 1)
            for s in strMsg:
                if s in key_compliment:
                    LVL_AMOUR = up_value(LVL_AMOUR, 3)
                    bot_talk("Wow you are too good !")
                    return True
            bot_talk("C'est bieng !")
            return True
    return False


def log_states():
    print("\n>>> peur/méfiance: {} - mefiance: {} - amour: {}\n".format(LVL_COLERE_PEUR, LVL_MEFIANCE, LVL_AMOUR))


def rules_states():
    # return false if discuss must be ended
    global LVL_MEFIANCE, LVL_COLERE_PEUR, LVL_AMOUR
    # Rules for max range of different mood
    discuss = None
    if LVL_MEFIANCE > MAX_MEFIANCE:
        LVL_MEFIANCE = MAX_MEFIANCE
        discuss = customize_responses()
    if LVL_COLERE_PEUR > MAX_PEUR_COLERE:
        LVL_COLERE_PEUR = MAX_PEUR_COLERE
        discuss = customize_responses()
    if LVL_AMOUR > MAX_AMOUR:
        LVL_AMOUR = MAX_AMOUR
        discuss = customize_responses()
    if discuss is False:
        return False


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
    print(bot_template.format(msg))


bool = False
while bool is False:
    msg = input(user_template)
    if msg == "exit":
        bot_talk("Goodbye !")
        bool = True
    else:
        if send_message(msg) is False:
            bool = True

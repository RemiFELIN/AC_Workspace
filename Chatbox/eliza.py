import time
import random
import re
# import spacy

# pip install rasa_nlu
# from rasa_nlu.config import RasaNLUConfig
# from rasa_nlu.model import Trainer
# from rasa_nlu.converters import load_data

# Ce bot est inspiré du tutoriel "Eliza" sur Datacamp
# Les principaux concepts ont été implémenté ci-dessous

user_template = "> "
bot_template = "[BOT] {}"

name = "Rémi"
weather = ["cloudy", "rainy", "sunny", "windy", "gusty"]
perception = []
tolerance = 3

# Define a dictionary containing a list of responses for each message
responses = {
    "name": [
        "my name is EchoBot",
        "they call me EchoBot",
        "the name's Bot, Echo Bot"
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
    # Si on se répète sur des concepts
    if perception.count(tolerance) != 0:
        repeated_word = perception[perception.index(tolerance) - 1]
        return responses["repeat"].format(repeated_word)
    if name is not None:
        return "Hello, {0}!".format(name)
    elif "weather" in message:
        return random.choice(responses["weather"])
    elif "name" in message and "?" in message:
        return random.choice(responses["name"])
    elif "yes" == message.lower() or "no" == message.lower():
        return "Why ?"
    else:
        output = replace_pronouns(message)
        if "hello" in output:
            return output
        return output + " ?"


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
    response = respond(message)
    print(bot_template.format(response))
    time.sleep(0.75)


def update_perception(message):
    capitalized_name = re.compile("[A-Z][A-Za-z]*")
    for concept in capitalized_name.findall(message):
        if concept in perception:
            perception.append(concept)
            perception.append(perception.count(concept))
        else:
            perception.append(concept)


'''
send_message("hello")
send_message("what's your name?")
send_message("what's today's weather?")
send_message("my name is Remi !")
send_message("I have the highground")
'''

# SIMULATION
sim = False
while sim is False:
    msg = input(user_template)
    if msg == "exit":
        print(bot_template.format("Goodbye !"))
        sim = True
    else:
        send_message(msg)

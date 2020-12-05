import time
import random
import re
import spacy
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer
from rasa_nlu.converters import load_data

user_template = "[USER] {}"
bot_template = "[BOT] {}"

# Import the random module
import random

name = "Rémi"
weather = "cloudy"

# Define a dictionary containing a list of responses for each message
responses = {
    "what's your name?": [
        "my name is {0}".format(name),
        "they call me {0}".format(name),
        "I go by {0}".format(name)
    ],
    "what's today's weather?": [
        "the weather is {0}".format(weather),
        "it's {0} today".format(weather)
    ],
    "default": ["default message"]
}


# Use random.choice() to choose a matching response
def respond(message):
    if message in responses:
        bot_message = random.choice(responses[message])
    else:
        bot_message = random.choice(responses["default"])
    return bot_message


responses2 = {
    "what's today's weather?": "it's {} today"
}

multi_responses = {
    "what's your name? (rand)": [
        "my name is EchoBot",
        "they call me EchoBot",
        "the name's Bot, Echo Bot"
    ]
}


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
    time.sleep(1)
    # If user give name
    name = find_name(message)
    if name is not None:
        return "Hello, {0}!".format(name)
    if message in responses:
        return responses[message]
    elif message in responses2:
        return responses2[message].format(weather_today)
    elif message in multi_responses:
        return random.choice(multi_responses[message])
    # Check for a question mark
    elif message.endswith('?'):
        # Return a random question
        return random.choice(responses["question"])
    # Return a random statement
    return replace_pronouns(message)


# Define replace_pronouns()
def replace_pronouns(message):
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
    return message


# Define match_rule()
def match_rule(rules, message):
    response, phrase = "default", None
    # Iterate over the rules dictionary
    for pattern, responses in rules.items():
        # Create a match object
        match = re.search(pattern, message)
        if match is not None:
            # Choose a random response
            response = random.choice(responses)
            if '{0}' in response:
                phrase = match.group(1)
    # Return the response and phrase
    return response.format(phrase)


# Test match_rule
'''
print(match_rule(rules, "do you remember your last birthday"))
print(replace_pronouns("my last birthday"))
print(replace_pronouns("when you went to Florida"))
print(replace_pronouns("I had my own castle"))
'''


def send_message(message):
    print(user_template.format(message))
    response = respond(message)
    print(bot_template.format(response))
    time.sleep(1)


send_message("hello")
send_message("what's your name?")
send_message("what's today's weather?")
send_message("what's your name? (rand)")
send_message("My name is Remi !")
print(interpreter.parse("are there any good pizza places in the center?"))

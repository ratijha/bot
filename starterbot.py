__author__ = 'ratijha'
import os
import time
import random
from slackclient import SlackClient
from plugins import weather
import envset

# For NLP
from textblob import TextBlob
user_mention = 'Rati'
GREETING_KEYWORDS = ("hello", "hi", "greetings", "hey",  "sup", "what's up",)
GREETING_RESPONSES = ["hey {mention}", "Hello {mention}", "Hey There {mention}!!! \n How can I help you today? ",
                      "Hi {mention}"]
NORMAL_RESPONSES = ["Thanks", "Thank You", "nice to meet you"]


def is_hi(message):
    tokens = [word.lower() for word in message.strip().split()]
    return any(g in tokens
               for g in GREETING_KEYWORDS)


def is_bye(message):
    tokens = [word.lower() for word in message.strip().split()]
    return any(g in tokens
               for g in ['bye', 'goodbye', 'revoir', 'adios', 'later', 'cya'])


def say_hi(user_mention):
    """Say Hi to a user by formatting their mention"""
    response_template = random.choice(GREETING_RESPONSES)
    return response_template.format(mention=user_mention)


def say_bye(user_mention):
    """Say Goodbye to a user"""
    response_template = random.choice(['see you later, alligator...',
                                       'adios amigo',
                                       'Bye {mention}!',
                                       'Au revoir!'])
    return response_template.format(mention=user_mention)


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarificati  on.
    """
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command with numbers, delimited by spaces."

    # print(command)
    if is_hi(command):
        # response = "Hey There!!! \n How can I help you today? "
        response = say_hi(user_mention)
    elif is_bye(command):
        response = say_bye(user_mention)
    elif command.startswith("weather "):
        res1 = "Today's Weather"
        res2 = weather.on_message(command)
        response = res1 + "\n" + res2
    elif command in NORMAL_RESPONSES:
        blob = TextBlob(command)
        sentiment = blob.sentiment
        if sentiment.polarity > 0:
            response = "That's great to hear.  Is there anything else I can help you with today?"
        elif sentiment.polarity < 0:
            response = "Oh no - we're sorry to hear that! How can we make your experience better?"
    else:
        response = response
    slack_client.api_call("chat.postMessage", token=token,channel=channel,
                         text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    # print(output_list)
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                print(output)
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    envset.env()
    # starterbot's ID as an environment variable
    BOT_ID = os.environ.get("BOT_ID")
    token = os.environ.get("SLACK_BOT_TOKEN")

    # constants
    AT_BOT = "<@" + BOT_ID + ">"
    EXAMPLE_COMMAND = "do"

    # instantiate Slack & Twilio clients
    slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            # print(slack_client.rtm_read())
            command, channel = parse_slack_output(slack_client.rtm_read())
            # print(command, channel)
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
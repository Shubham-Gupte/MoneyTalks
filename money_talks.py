"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import mintapi
import pickle
import datetime
import location


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Money Talks. Let's talk money!"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "What information would you like to know?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    pickler(login=False, read=False)
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def getAccountBalances(intent, session):
    if not (pickler(read=True) and location.verifyLocation()) :
        return build_response({}, build_speechlet_response(
        intent['name'], "Please say, My password is, followed by your password", None, False))
    filehandler = open('accounts.pi', 'r') 
    accts = pickle.load(filehandler)
    speech_output = "You have a balance of "
    for account in accts:
        speech_output += str(int(account['currentBalance'])) + " in your " + account['accountName'] + "account,"
    should_end_session = False
    return build_response({}, build_speechlet_response(
        intent['name'], speech_output, None, should_end_session))

def getNextCreditPayment(intent, session):
    if not (pickler(read=True) and location.verifyLocation()):
        return build_response({}, build_speechlet_response(
        intent['name'], "Please say, My password is, followed by your password", None, False))
    should_end_session = False

    filehandler = open('accounts.pi', 'r') 
    cc = pickle.load(filehandler)[0]
    date = cc['dueDate']
    balance = cc['currentBalance']
    dueAmt = cc['dueAmt']
    today = datetime.datetime.now()
    dueDate = datetime.datetime.strptime(date, "%m/%d/%Y")
    delta = dueDate - today
    daysTillDue = delta.days
    speech_output = "Your next payment is a payment of" + str(int(dueAmt)) + " dollars due on " + str(dueDate.date()) + ". That's in " + str(daysTillDue) + "Days!"
    print(speech_output)
    return build_response({}, build_speechlet_response(
        intent['name'], speech_output, None, should_end_session))


def getBudgets(intent, session):
    if not (pickler(read=True) and location.verifyLocation()):
        return build_response({}, build_speechlet_response(
        intent['name'], "Please say, My password is, followed by your password", None, False))
    filehandler = open('budgets.pi', 'r') 
    budgets = pickle.load(filehandler)
    should_end_session = False
    speech_output = "You should be spending "
    for budget in budgets['spend']:
        speech_output += str(int(budget['bgt'])) + 'dollars on ' + budget['cat'] + ", "
    return build_response({}, build_speechlet_response(
        intent['name'], speech_output, None, should_end_session))


def create_favorite_color_attributes(favorite_color):
    return {"favoriteColor": favorite_color}


def getIndBudget(intent, session):
    if not (pickler(read=True) and location.verifyLocation()):
        return build_response({}, build_speechlet_response(
        intent['name'], "Please say, My password is, followed by your password", None, False))
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """
    categories = ['transportation',
            'entertainment',
            'coffee shops',
            'fast food',
            'groceries',
            'restaurants',
            'clothing']

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    filehandler = open('budgets.pi', 'r') 
    budgets = pickle.load(filehandler)
    should_end_session = False
    speech_output = ""

    if 'BudgetCategory' in intent['slots'] and intent['slots']['BudgetCategory']['value'].lower() in categories:
        requestedCategory = intent['slots']['BudgetCategory']['value'].lower()
        session_attributes = {'BudgetCategory': requestedCategory}
        print(requestedCategory)
        for cat in budgets['spend']:
            print("category: " + cat['cat'])
            if cat['cat'] == requestedCategory:
                speech_output = "You have spent" + str(int(cat['amt'])) + 'dollars out of your ' + str(int(cat['bgt'])) + " dollar allowance for " + cat['cat']
                if cat['cat'] == 'clothing':
                    speech_output += '. Stop buying so many shoes!'
                # print(speech_output)
        reprompt_text = None
    else:
        speech_output = "I'm not sure what category you requested" \
                        "Please try again."
        reprompt_text = "I'm not sure what category you requested. Ask for your spending in a budget category, like Groceries or Clothing."
    print(speech_output)
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def getAuthentication(intent, session, login):
    if location.verifyLocation():
        pickler(login=True, read=False)
        should_end_session = False
        return build_response({}, build_speechlet_response(
            intent['name'], "You are now logged in.", None, should_end_session))
    else:
        should_end_session = False
        return build_response({}, build_speechlet_response(
            intent['name'], "You are not logged in. Try again", None, should_end_session))

def getNetWorth(intent, session, loggedIn):
    # if 'LoggedIn' not in session.keys() or not session['LoggedIn']:
    if not (pickler(read=True) and location.verifyLocation()):
        return build_response({}, build_speechlet_response(
        intent['name'], "Please say, My password is, followed by your password", None, False))

    card_title = "Net Worth"
    filehandler = open('netWorth.pi', 'r')
    net_Worth = pickle.load(filehandler)

    should_end_session = False
    speech_output = "Your net worth is " + str(int(5995)) + " Dollars . Have a great one big boi."
    # speech_output = "Test passed."
    return build_response({}, build_speechlet_response(
        intent['name'], speech_output, None, should_end_session))
    # print('hello')
    # print(speech_output)

def goodbye(intent, session):
    card_title = "GoodBye"
    should_end_session = True
    session['LoggedIn'] = False
    speech_output = "Goodbye!"
    # speech_output = "Test passed."
    return build_response({}, build_speechlet_response(
        intent['name'], speech_output, None, should_end_session))

def get_color_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "favoriteColor" in session.get('attributes', {}):
        favorite_color = session['attributes']['favoriteColor']
        speech_output = "Your favorite color is " + favorite_color
        should_end_session = True
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "You can say, my favorite color is red."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))
def pickler(login=False, read=False):
    if read:
        file = open('/tmp/LogIn', 'r')
        return pickle.load(file)
    file = open('/tmp/LogIn', 'w')
    pickle.dump(login, file)

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """
    pickler()
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    pickler()
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    LoggedIn = False
    # Dispatch to your skill's intent handlers
    if intent_name == "MyColorIsIntent":
        return set_color_in_session(intent, session)
    elif intent_name == "WhatsMyColorIntent":
        return get_color_from_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    elif intent_name == "getNetWorthIntent":
        return getNetWorth(intent, session, LoggedIn)
    elif intent_name == "getAccountBalancesIntent":
        return getAccountBalances(intent, session)
    elif intent_name == "getBudgetsIntent":
        return getBudgets(intent, session)
    elif intent_name == "nextCreditPaymentIntent":
        return getNextCreditPayment(intent, session)
    elif intent_name == 'getIndBudgetIntent':
        return getIndBudget(intent, session)
    elif intent_name == 'getAuthenticationIntent':
        return getAuthentication(intent, session, LoggedIn)
    elif intent_name == 'endSessionIntent':
        return goodbye(intent, session)
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

import logging
import pymysql
import sys
import rds_config

import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

# Init Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Init Database MySQL connection
rds_host  = rds_config.db_endpoint
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name
port = 3306

try:
    conn = pymysql.connect(rds_host, user=name,
                           passwd=password, db=db_name, connect_timeout=5)
except:
    logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()

# ========================================
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        amazon_id = handler_input.request_envelope.session.user.user_id

        with conn.cursor() as cur:
            found = cur.execute(f"SELECT * FROM STUDENTS WHERE amazon_id=\"{amazon_id}\"")

        return ask_utils.is_request_type("LaunchRequest")(handler_input) and found > 0

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "It's not the first time!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class FirstLaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "It's your first time!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class AgendaIntentHandler(AbstractRequestHandler):
    """Handler for Get Assignments Intent"""
    def can_handle(self, handler_input):
        # type (HandlerInput) -> bool
        return ask_utils.is_intent_name("AgendaIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        #get list of assignments within a week from that time given student id
        #query into assignments array
        # speak_output = "Here are the assignments due in the next week."
        # for assignment in assignments:
        #     speak_output = speak_output + "(assignment) due (date)"

        #with conn.cursor() as cur:
            #cur.execute("select * from STUDENTS")

        #speak_output = "My name is " + cur.fetchone()[1] + ". I am the sarge."

        with conn.cursor() as cur:
            cur.execute("select * from ASSIGNMENTS")

        speak_output = "test!!" + cur.fetchone()[1]

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class PrioritizeIntentHandler(AbstractRequestHandler):
    """Handler for Get Assignments Intent"""
    def can_handle(self, handler_input):
        # type (HandlerInput) -> bool
        return ask_utils.is_intent_name("PrioritizeIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        #get all assignments for this week, return one with highest priority
        current_assignment = None
        for assignment in assignments:
            if current_assignment.weight < assignment.weight:
                current_assignment = assignment
        speak_output = "you should work on " + current_assignment



        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class AdditionIntentHandler(AbstractRequestHandler):
    """Handler for Get Assignments Intent"""
    def can_handle(self, handler_input):
        # type (HandlerInput) -> bool
        return ask_utils.is_intent_name("AdditionIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        #create new assignment and put into database
        speak_output = "assignment added to calendar"



        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class CompletionIntentHandler(AbstractRequestHandler):
    """Handler for Get Assignments Intent"""
    def can_handle(self, handler_input):
        # type (HandlerInput) -> bool
        return ask_utils.is_intent_name("CompletionIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        #remove assignment and remove from database
        speak_output = "assignment removed from calendar"



        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can ask me what assignments you have, or what I think you should work on. You can also tell me about new upcoming assignments and tests."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response

class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(FirstLaunchRequestHandler())
sb.add_request_handler(AgendaIntentHandler())
sb.add_request_handler(PrioritizeIntentHandler())
sb.add_request_handler(CompletionIntentHandler())
sb.add_request_handler(AdditionIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()

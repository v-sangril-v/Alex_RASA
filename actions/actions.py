"""Custom actions"""
import os
from typing import Dict, Text, Any, List
import logging
from dateutil import parser
import sqlalchemy as sa

from rasa_sdk.interfaces import Action
from rasa_sdk.events import (
    SlotSet,
    EventType,
    ActionExecuted,
    SessionStarted,
    Restarted,
    FollowupAction,
    UserUtteranceReverted,
)
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
#from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase
#from rasa_sdk.knowledge_base.actions import ActionQueryKnowledgeBase

from actions.parsing import (
    parse_duckling_time_as_interval,
    parse_duckling_time,
    get_entity_details,
    parse_duckling_currency,
)

from actions.profile_db import create_database, ProfileDB

from actions.custom_forms import CustomFormValidationAction


logger = logging.getLogger(__name__)

# The profile database is created/connected to when the action server starts
# It is populated the first time `ActionSessionStart.run()` is called.

PROFILE_DB_NAME = os.environ.get("PROFILE_DB_NAME", "profile")
PROFILE_DB_URL = os.environ.get("PROFILE_DB_URL", f"sqlite:///{PROFILE_DB_NAME}.db")
ENGINE = sa.create_engine(PROFILE_DB_URL)
create_database(ENGINE, PROFILE_DB_NAME)

profile_db = ProfileDB(ENGINE)

NEXT_FORM_NAME = {
    "transfer_money": "transfer_money_form",
    "search_transactions": "transaction_search_form",
    "check_earnings": "transaction_search_form",
}

FORM_DESCRIPTION = {

    "transfer_money_form": "money transfer",
    "transaction_search_form": "transaction search",
}




    
            

        

            

        















    

    











class ActionSessionStart(Action):
    """Executes at start of session"""

    def name(self) -> Text:
        """Unique identifier of the action"""
        return "action_session_start"

    @staticmethod
    def _slot_set_events_from_tracker(
        tracker: "Tracker",
    ) -> List["SlotSet"]:
        """Fetches SlotSet events from tracker and carries over keys and values"""

        # when restarting most slots should be reset
        relevant_slots = ["currency"]

        return [
            SlotSet(
                key=event.get("name"),
                value=event.get("value"),
            )
            for event in tracker.events
            if event.get("event") == "slot" and event.get("name") in relevant_slots
        ]

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:
        """Executes the custom action"""
        # the session should begin with a `session_started` event
        events = [SessionStarted()]

        events.extend(self._slot_set_events_from_tracker(tracker))

        # create a mock profile by populating database with values specific to tracker.sender_id
        profile_db.populate_profile_db(tracker.sender_id)
        currency = profile_db.get_currency(tracker.sender_id)

        # initialize slots from mock profile
        events.append(SlotSet("currency", currency))

        # add `action_listen` at the end
        events.append(ActionExecuted("action_listen"))

        return events


class ActionRestart(Action):
    """Executes after restart of a session"""

    def name(self) -> Text:
        """Unique identifier of the action"""
        return "action_restart"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:
        """Executes the custom action"""
        return [Restarted(), FollowupAction("action_session_start")]




    












#class ActionMyKB(ActionQueryKnowledgeBase):
#    def __init__(self):
#        # load knowledge base with data from the given file
#        knowledge_base = InMemoryKnowledgeBase("knowledgebase.json")

#        super().__init__(knowledge_base)
        
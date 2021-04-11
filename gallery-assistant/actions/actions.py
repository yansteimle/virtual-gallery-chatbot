# actions.py
# This files contains the custom actions which can be used to run
# custom Python code.
#
# Resources consulted:
# https://rasa.com/docs/rasa/custom-actions
# https://rasa.com/docs/action-server/
# https://rasa.com/docs/rasa/forms
#####################################################
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset
from rasa_sdk.types import DomainDict
import datetime
from . import db_handler
import re  # for regex pattern-matching


def is_valid_artwork_id(id_code: str):
    """
    Checks if given string is a valid artwork id code.
    :param id_code: string
    :return: true if the input is in the format ABC123 (3 capital letters followed by 3 digits)
    """
    if id_code is not None and re.match(r"^[A-Z]{3}\d{3}$", id_code):
        return True
    else:
        return False


class ActionAuctionSchedule(Action):
    """Class that corresponds to the action that gets the auction schedule."""

    def name(self) -> Text:
        return "action_auction_schedule"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        today = datetime.date.today()
        delta = datetime.timedelta(days=+3)
        next_auction_date = today + delta
        response = "The next auction is on " + next_auction_date.strftime("%A, %d %b %Y") + \
                   " at 8:00 PM (EST). The bidding closes at 3:00 PM on the same day."
        dispatcher.utter_message(text=response)

        return []


class ActionUserBidList(Action):
    """This action gets the list of bids (and the values) for the logged-in user
    (which is Foo by default). The returned message contains a button for each bid
    where the artwork id and bid value are displayed. By clicking on the button, the
    user gets more info about the artwork (full info card)."""

    def name(self) -> Text:
        return "action_user_bid_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        bid_list = db_handler.get_bids_for_user('Foo')
        if len(bid_list) < 1:
            dispatcher.utter_message(text="You have not submitted any bids yet for the current auction.")
        else:
            if len(bid_list) == 1:
                text = "You have submitted a single bid for the current auction. Click on the artwork ID code " \
                       "below for more information."
            else:
                text = f"You have submitted bids for {len(bid_list)} artworks. Click on one of the artwork ID codes " \
                       f"below for more information."
            buttons = []
            for pair in bid_list:
                buttons.append({'payload': f'/ask_artwork_info_card{{"artwork_id": "{pair[0]}"}}',
                                'title': f'{pair[0]} (${pair[1]})'})
            dispatcher.utter_message(text=text, buttons=buttons)

        return [SlotSet('artwork_id', None)]  # just in case


class ActionNumberBidsOnArtwork(Action):
    """This action checks how many people have bid on a given artwork."""

    def name(self) -> Text:
        return "action_num_bids_on_artwork"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        artwork_id = tracker.get_slot('artwork_id')
        if is_valid_artwork_id(artwork_id):
            artwork = db_handler.get_artwork_info(artwork_id)
            if artwork is None:
                dispatcher.utter_message(
                    text=f"Sorry, there is no artwork with ID code {artwork_id}. Please try again.")
                return [SlotSet('artwork_id', None)]  # empty the artwork_id slot
            else:
                num_bids = len(artwork.bidders)
                if num_bids == 0:
                    text = f"No bids have been submitted for artwork {artwork_id} (\"{artwork.title}\" by " \
                           f"{artwork.artist_name})."
                else:
                    text = f"In total, {num_bids} users have bid on {artwork_id} (\"{artwork.title}\" by " \
                           f"{artwork.artist_name})."
                dispatcher.utter_message(text=text)
                return [SlotSet('artwork_id', None)]
        else:
            dispatcher.utter_message(text=f"Sorry, {artwork_id} is not a valid artwork ID code. Make sure you use "
                                          f"capital letters (e.g. ABC123 or WEB563).")
            return [SlotSet('artwork_id', None)]  # empty the artwork_id slot


class ActionArtworkInfoCard(Action):
    """This action displays the artwork info card (all available information about the artwork)."""

    def name(self) -> Text:
        return "action_artwork_info_card"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        artwork_id = tracker.get_slot('artwork_id')
        if is_valid_artwork_id(artwork_id):
            artwork = db_handler.get_artwork_info(artwork_id)
            if artwork is None:
                dispatcher.utter_message(
                    text=f"Sorry, there is no artwork with ID code {artwork_id}. Please try again.")
                return [SlotSet('artwork_id', None)]  # empty the artwork_id slot
            else:
                text = f"Title: {artwork.title}\nArtist: {artwork.artist_name}\nID code: {artwork_id}\nCategory: " \
                       f"{artwork.category}\nMedium: {artwork.medium}\nMinimum bid: ${artwork.min_bid}\n" \
                       f"Current number of bids: {len(artwork.bidders)}"
                # check if logged-in user (Foo by default) has bid on the artwork
                bid = db_handler.get_bid_info('Foo', artwork_id)
                if bid is None:
                    text += "\nYou have not submitted a bid for this artwork."
                else:
                    text += f"\nYour bid: ${bid.value}"
                dispatcher.utter_message(text=text)
                return []
        else:  # not a valid artwork id code
            dispatcher.utter_message(text=f"Sorry, {artwork_id} is not a valid artwork ID code. Make sure you use "
                                          f"capital letters (e.g. ABC123 or WEB563).")
            return [SlotSet('artwork_id', None)]  # empty the artwork_id slot


class ActionMinimumBid(Action):
    """This action gets the minimum bid value for an artwork. It also tells the title and artist name."""

    def name(self) -> Text:
        return "action_minimum_bid"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        artwork_id = tracker.get_slot('artwork_id')
        if is_valid_artwork_id(artwork_id):
            artwork = db_handler.get_artwork_info(artwork_id)
            if artwork is None:
                dispatcher.utter_message(
                    text=f"Sorry, there is no artwork with ID code {artwork_id}. Please try again.")
                return [SlotSet('artwork_id', None)]  # empty the artwork_id slot
            else:
                text = f"{artwork_id} is the ID code for the artwork \"{artwork.title}\" by {artwork.artist_name}. " \
                       f"The minimum bid is ${artwork.min_bid}."
                dispatcher.utter_message(text=text)
        else:  # not a valid artwork id code
            dispatcher.utter_message(text=f"Sorry, {artwork_id} is not a valid artwork ID code. Make sure you use "
                                          f"capital letters (e.g. ABC123 or WEB563).")
            return [SlotSet('artwork_id', None)]  # empty the artwork_id slot

        return [SlotSet('artwork_id', None)]


class ActionAskModifyBidFormArtworkId(Action):
    """This action asks the user to provide the ID code of the artwork for which they want to modify the
    bid. To help the user, the list of the artwork IDs for which the user has submitted a bid are provided
    as buttons.
    By default, the user is Foo."""

    def name(self) -> Text:
        return "action_ask_modify_bid_form_artwork_id"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        bid_list = db_handler.get_bids_for_user('Foo')
        text = "For which artwork do you want to modify the bid value? Please provide the artwork ID code " \
               "(e.g. ABC123 or GAP009)."
        if len(bid_list) < 1:
            dispatcher.utter_message(text=text)
        else:
            buttons = []
            for pair in bid_list:
                buttons.append({'payload': f'/inform{{"artwork_id": "{pair[0]}"}}',
                                'title': f'{pair[0]}'})
            dispatcher.utter_message(text=text, buttons=buttons)

        return []


class ActionAskModifyBidFormBidValue(Action):
    """This action asks the user to provide the new value for the bid. If we are here, we should have
    already asked the user for the artwork ID, so we can tell them what the minimum bid and the user's current
    bid value is (by default, user is Foo)."""

    def name(self) -> Text:
        return "action_ask_modify_bid_form_bid_value"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        artwork_id = tracker.get_slot('artwork_id')
        if artwork_id is None:
            text = "Error: action_ask_modify_bid_form_bid_value triggered, but value of slot artwork_id is None."
            dispatcher.utter_message(text=text)
        else:
            artwork = db_handler.get_artwork_info(artwork_id)
            if artwork is None:
                text = f"Sorry, no artwork with ID code {artwork_id} exists. Please try again."
                dispatcher.utter_message(text=text)
                return [SlotSet('artwork_id', None)]  # empty the artwork_id slot
            else:
                user_bid = db_handler.get_bid_info('Foo', artwork_id)
                if user_bid is None:  # User has not bid on this artwork yet
                    text = f"How many Canadian dollars do you want to bid on artwork {artwork_id}? The minimum bid " \
                           f"is ${artwork.min_bid}. Please use an integer value (e.g. 1000 or 550)."
                else:
                    text = f"How many Canadian dollars do you want to bid on artwork {artwork_id}? The minimum bid " \
                           f"is ${artwork.min_bid} and your current bid is ${user_bid.value}. Please use an " \
                           f"integer value (e.g. 1000 or 550)."
                dispatcher.utter_message(text=text)

        return []


class ActionAskModifyBidFormConfirmForm(Action):
    """This action asks the user to confirm whether they want to do the bid modification or not."""

    def name(self) -> Text:
        return "action_ask_modify_bid_form_confirm_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        artwork_id = tracker.get_slot('artwork_id')
        bid_value = tracker.get_slot('bid_value')

        text = f"Are you sure you want to submit a new bid for artwork {artwork_id} with value ${bid_value}?"
        buttons = [{'payload': '/agree', 'title': 'Yes'},
                   {'payload': '/disagree', 'title': 'No'}]
        dispatcher.utter_message(text=text, buttons=buttons)

        return []


class ValidateModifyBidForm(FormValidationAction):
    """This action validates all of the slots in modify_bid_form."""

    def name(self) -> Text:
        return "validate_modify_bid_form"

    def validate_artwork_id(self, slot_value: Any,
                            dispatcher: CollectingDispatcher,
                            tracker: Tracker,
                            domain: DomainDict) -> Dict[Text, Any]:
        """Validate artwork_id slot value."""
        id_code = slot_value.upper()  # ensure letters are in upper_case
        if is_valid_artwork_id(id_code):
            # check that an artwork with this ID number actually exists
            if db_handler.get_artwork_info(id_code) is not None:  # the artwork exists
                return {'artwork_id': id_code}
            else:  # the artwork does not exist
                dispatcher.utter_message(text=f"Sorry, no artwork with ID code {id_code} exists.")
                return {'artwork_id': None}
        else:
            dispatcher.utter_message(text=f"Sorry, {slot_value} is not a valid artwork ID code.")
            return {'artwork_id': None}

    def validate_bid_value(self, slot_value: Any,
                           dispatcher: CollectingDispatcher,
                           tracker: Tracker,
                           domain: DomainDict) -> Dict[Text, Any]:
        """Validate the bid_value slot value."""
        try:
            value = int(slot_value)
            min_bid = db_handler.get_min_bid_amount(tracker.get_slot('artwork_id'))
            if min_bid is not None:
                if value >= min_bid:
                    return {'bid_value': value}
                else:
                    dispatcher.utter_message(text=f"Sorry, {value} is less than the minimum bid amount of {min_bid}.")
                    return {'bid_value': None}
            else:
                dispatcher.utter_message(text=f"Error: cannot verify minimum bid amount.")
                return {'bid_value': None}
        except ValueError:
            dispatcher.utter_message(text=f"Sorry, {slot_value} is not a valid bid amount.")
            return {'bid_value': None}

    def validate_confirm_form(self, slot_value: Any,
                              dispatcher: CollectingDispatcher,
                              tracker: Tracker,
                              domain: DomainDict) -> Dict[Text, Any]:
        """Validate that we got yes or no for confirmation."""
        if slot_value in ["yes", "no"]:
            return {'confirm_form': slot_value}
        else:
            dispatcher.utter_message(text="Sorry, I did not understand your response.")
            return {'confirm_form': None}


class ActionSubmitModifyBid(Action):
    """Action to call once have collected all of the information for the modify bid form.
    Either does the modification or says 'ok, cancelled' depending on value of confirm_form slot."""

    def name(self) -> Text:
        return "action_submit_modify_bid"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('confirm_form') == "yes":  # do the modification
            artwork_id = tracker.get_slot('artwork_id')
            bid_value = int(tracker.get_slot('bid_value'))
            text = db_handler.modify_bid_value('Foo', artwork_id, bid_value)
            dispatcher.utter_message(text=text)
        else:  # user said no
            dispatcher.utter_message(response='utter_confirm_request_cancel')
        # reset all slots
        return [SlotSet("artwork_id", None), SlotSet("bid_value", None), SlotSet("confirm_form", None)]

# db_handler.py
# Functions to query the database
# Resources consulted:
# see db_models.py
# https://docs.sqlalchemy.org/en/14/tutorial/index.html
# https://docs.sqlalchemy.org/en/14/orm/index.html
# https://docs.sqlalchemy.org/en/14/orm/loading_objects.html
# https://docs.sqlalchemy.org/en/14/orm/queryguide.html
# https://docs.sqlalchemy.org/en/14/orm/tutorial.html  <-- this one for complete presentation with session and query
# https://docs.sqlalchemy.org/en/14/orm/query.html  <-- Query API
# https://docs.sqlalchemy.org/en/14/orm/session_api.html  <--  Session API
# https://docs.python.org/3/reference/import.html#package-relative-imports
###################################
from .db_models import Session, User, Bid, Artwork

session = Session()


def get_bids_for_user(user_name: str):
    """Function that takes a user_name and returns a list of pairs (artwork_id, value) for
    each bid made by the user that can be found in the database."""
    user = session.query(User).get(user_name)  # returns user with this primary key or None if it does not exist
    if user is None:
        return []
    else:
        return [(b.artwork.artwork_id, b.value) for b in user.bids]


def modify_bid_value(user_name: str, artwork_id: str, new_value: int, create_if_not_exists=True):
    """
    Function that takes a user name, an artwork id, and a new bid value
    modifies the bid value (if the bid exists and the new_value is greater or equal
    to the minimum bid value) and returns a confirmation message. If the operation
    cannot be done, returns an error message.

    :param user_name: user name (string)
    :param artwork_id: artwork id code (string), format: ABC123
    :param new_value: float, must be >= min_bid of artwork
    :param create_if_not_exists: set to true if bid should be created if it does not exist
    :return: Confirmation/Error message (string)
    """
    bid = session.query(Bid).get({"user_name": user_name, "artwork_id": artwork_id})
    if bid is None:
        if create_if_not_exists:
            user = session.query(User).get(user_name)
            artwork = session.query(Artwork).get(artwork_id)
            if user is not None and artwork is not None:
                if new_value >= artwork.min_bid:  # bid is valid
                    new_bid = Bid(user=user, artwork=artwork, value=new_value)
                    session.add(new_bid)
                    session.commit()
                    return f"Ok {user_name}, your bid for artwork {artwork_id} with value {new_value} was " \
                           f"successfully created."
                else:  # bid is not valid
                    return f"Sorry {user_name}, I could not create your bid with value {new_value} since the minimum " \
                           f"bid for artwork {artwork_id} is {artwork.min_bid}."
            else:
                return f"An error occurred: either the user {user_name} or the artwork {artwork_id} does not exist."
        else:
            return f"An error occurred: there is no bid for user {user_name} and artwork {artwork_id} " \
               f"currently in the database."
    else:  # there was such a bid in the database
        if new_value >= bid.artwork.min_bid:  # new bid is valid
            bid.value = new_value  # pending change
            session.commit()  # save change to database
            return f"Ok {user_name}, your bid for artwork {artwork_id} was successfully updated with the new " \
                   f"value {new_value}."
        else:  # new bid is not valid
            return f"Sorry {user_name}, I could not update your bid with the new value {new_value} since the minimum " \
                   f"bid for artwork {artwork_id} is {bid.artwork.min_bid}."


def get_artwork_info(artwork_id: str):
    """
    Function to get information about artwork.

    :param artwork_id: artwork id code (string)
    :return: Artwork object or None if no artwork has this id number
    """
    return session.query(Artwork).get(artwork_id)


def get_min_bid_amount(artwork_id: str):
    """
    Function to get minimum bid amount for an artwork.

    :param artwork_id: artwork id code (string)
    :return: minimum bid amount (int) or None if no such artwork exists
    """
    artwork = get_artwork_info(artwork_id)
    if artwork is None:
        return None
    else:
        return artwork.min_bid


def get_bid_info(user_name: str, artwork_id: str):
    """
    Function to get information about a single bid.

    :param user_name: string
    :param artwork_id: string
    :return: Bid object if it exists, None otherwise
    """
    return session.query(Bid).get({"user_name": user_name, "artwork_id": artwork_id})

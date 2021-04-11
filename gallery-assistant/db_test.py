# db_test.py
# To see if the database works properly
########################################
from actions import db_handler


def test_get_bids(user_name):
    print(f"Bids for user {user_name}:")
    print(db_handler.get_bids_for_user(user_name))


def test_modify_bid(user_name):
    test_get_bids(user_name)
    print(db_handler.modify_bid_value(user_name, 'LEG609', 700))
    test_get_bids(user_name)
    print(db_handler.modify_bid_value(user_name, 'LEG609', 200))
    test_get_bids(user_name)
    print(db_handler.modify_bid_value(user_name, 'MEG404', 1000))
    test_get_bids(user_name)


def artwork_id_test():
    for code in ['abc123', 'ABC123']:
        print(f"Original code: {code}")
        print(f"Upper-case code: {code.upper()}")


def bid_value_test():
    for val in ['10000', 100.56, 1000, '100.67']:
        int_val = int(val)
        print(f"int({val}) = {int_val}")


if __name__ == '__main__':
    print('Database tests')

    # test_get_bids('Foo')
    # test_modify_bid('Foo')

    # artwork_id_test()

    # bid_value_test()

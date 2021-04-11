# db_setup.py
# This file creates the database and inserts some sample data into it.
# Resources consulted: see the resources already cited in db_models.py
# NOTE: only run this once to create database. Therefore, moved this file out of the actions package so
# that it does not get called every time I do 'rasa run actions'
######################################
from actions.db_models import Session, engine, Base, User, Bid, Artwork

Base.metadata.create_all(engine)  # generate database schema
session = Session()  # create a new session

# Create users (i.e. clients)
foo = User(user_name='Foo')  # pretend that this is the logged-in user talking to chatbot
bar = User(user_name='Bar')
baz = User(user_name='Baz')

# Create artwork
artwork_info = [('ABC123', 'Cloud', 'Alice Allen', 'Coloured ink on paper', 'painting', 1000),
                ('DEF871', 'River', 'Alice Allen', 'Coloured ink on paper', 'painting', 500),
                ('LEG609', 'Shells', 'Alice Allen', 'Coloured ink on paper', 'painting', 400),
                ('ARM544', 'Spirals', 'Alice Allen', 'Coloured ink on paper', 'painting', 600),
                ('PAT110', 'Squares', 'Alice Allen', 'Coloured ink on paper', 'painting', 500),
                ('JBD007', 'Stairs', 'Alice Allen', 'Coloured ink on paper', 'painting', 500),
                ('WEB101', 'Eye 1', 'Bob Robson', 'Ballpoint pen on paper', 'drawing', 400),
                ('PAW366', 'Eye 2', 'Bob Robson', 'Ballpoint pen on paper', 'drawing', 400),
                ('HEL666', 'Eye 3', 'Bob Robson', 'Ballpoint pen on paper', 'drawing', 600),
                ('RAT999', 'Eye 4', 'Bob Robson', 'Ballpoint pen on paper', 'drawing', 400),
                ('GDP832', 'Blue', 'Charlie Charlton', 'Coloured pencil on paper', 'drawing', 1000),
                ('MEG404', 'Green', 'Charlie Charlton', 'Coloured pencil on paper', 'drawing', 1000),
                ('LAM734', 'Orange', 'Charlie Charlton', 'Coloured pencil on paper', 'drawing', 1000),
                ('TED837', 'Rainbow', 'Charlie Charlton', 'Coloured pencil on paper', 'drawing', 1000),
                ('PIG190', 'Marmot', 'Eve Evans', 'Photograph', 'photography', 500),
                ('GAP000', 'Flowers', 'Eve Evans', 'Photograph', 'photography', 400),
                ('NOT765', 'Sailboat', 'Eve Evans', 'Photograph', 'photography', 600),
                ('MAN221', 'Walls', 'Eve Evans', 'Sandstone', 'sculpture', 800),
                ('KIM876', 'Seashell', 'Eve Evans', 'Sandstone', 'sculpture', 1000)]
artwork_objects = []
for info in artwork_info:
    artwork_objects.append(Artwork(artwork_id=info[0], title=info[1], artist_name=info[2], medium=info[3],
                                   category=info[4], min_bid=info[5]))

# Create bids
# triple of format: (user, artwork index, value)
triples = [(foo, 0, 1100), (foo, 13, 1500), (foo, 4, 600), (foo, 18, 1200), (foo, 1, 600), (foo, 2, 600), (bar, 5, 600),
           (bar, 13, 1200), (bar, 4, 650), (baz, 0, 1100), (baz, 13, 1500), (baz, 4, 700), (baz, 18, 1100)]
bid_objects = []
for triple in triples:
    bid_objects.append(Bid(user=triple[0], artwork=artwork_objects[triple[1]], value=triple[2]))

# Add everything to the database
session.add_all([foo, bar, baz])
session.add_all(artwork_objects)
session.add_all(bid_objects)

# commit and then close session
session.commit()
session.close()

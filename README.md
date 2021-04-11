# Gabby: a Chatbot for a Virtual Art Gallery

Course project created by Yan Steimle (7685882) for the course CSI 5180 at the University of Ottawa in the Winter 2021 session.

### Contents

- `gallery-assistant`: this folder contains the code and data for the chatbot (including the custom action server). The SQLite database is stored in the file `gallery.db`. The final trained model was too large to be uploaded. It is a .tar.gz file one cannot access without installing rasa and running the whole project anyway. To recover the final trained model, one simply creates a `gallery-assistant/models` subdirectory and calls `rasa train`. Since all of the stories and new training examples created during interactive learning with Rasa X were saved to the data files, it is possible to obtain an analogous bot to the one used for the demonstration by retraining the bot using all provided data.
- `virtual-gallery`: this folder contains the code, html files, and sample images for the rudimentary Virtual Gallery web application (which does absolutely nothing other than display html pages). The web application uses flask and (at least on my computer) is accessible at the following address when run locally: http://127.0.0.1:5000/ 
- `project-presentation-Yan-Steimle.pdf`: this file contains the slides for the presentation (including any links to resources).

## Set-up and installation

### Web Application

The web application is a Python Flask application. I used a virtual environment (`venv`) with Python 3.9.

### Rasa X

To install and run Rasa X, I followed the instructions in the [Rasa documentation](https://rasa.com/docs/). Note that for Rasa X to run, one needs to have specific versions of Python and of certain Python libraries. Consequently, I set up a separate virtual environment for the Rasa X chatbot (not the same as the one for the web application). To satisfy all the package requirements, I ended up specifically installing the following versions:

- Python 3.8 (Rasa needs Python 3.6, 3.7, or 3.8)
- alembic version 1.4.3
- sqlalchemy version 1.3.22
- aiohttp version 3.6.3
- pytz version 2020.5

### Chatbot Action Server

The code for the custom action server (using the Python Rasa SDK) is found in the `gallery-assistant/actions` package, although the database set-up script is found in `gallery-assistant/db_setup.py`. Note that to ensure that the SQLite database file is accessible from different directories, I used an absolute path to specify the database file. To run the action server on another machine, one needs to edit the absolute path found on line 20 of the `gallery-assistant/actions/db_models.py` file (the database file should be located at `gallery-assistant/gallery.db`).


## Training the Chatbot

Note that the custom action server is not used during training.

To train the chatbot, one proceeds as follows:

1. Open the terminal, navigate to the `gallery-assistant` directory, and activate the virtual environment for Python 3.8
2. Run the following command to train the chatbot: ```rasa train```

The trained model will then be saved in the `gallery-assistant/models` directory.

## Running the Chatbot in Rasa X

To interact with the chatbot, I use the "Talk to your bot" feature of Rasa X. To do so, one must run the following steps:

1. Run the Virtual Gallery web application: open a terminal window, navigate to the `virtual-gallery` directory, activate the virtual environment (I used Python 3.9) and run the main program `app.py`. The web application will then be accessible at http://127.0.0.1:5000/ (or at another specified address depending on the machine).
2. Run the Custom Action Server: Open another terminal window, navigate to `gallery-assistant` and activate the virtual environment for Python 3.8. Then, run the action server with the command `rasa run actions`
3. Run Rasa X: Open a third terminal window, navigate to `gallery-assistant` and activate the virtual environment for Python 3.8. Then, run Rasa X with the command `rasa x`.
4. Talk to the bot: Rasa X will automatically open a page in the default web browser. In the menu on the left, select "Talk to your bot" (it might be necessary to wait a few moments while Rasa X locates the trained model). Then, one can start talking to the chatbot.

### Default logged-in user: Foo

Note that by default, the user "Foo" is assumed to be the logged-in user. Hence, when using the chatbot to get the list of submitted bids or to modify the value of the bid, the chatbot uses the data for the user "Foo". 

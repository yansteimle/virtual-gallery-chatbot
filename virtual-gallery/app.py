# app.py
# Yan Steimle (7685882)
# Virtual Gallery Web app
# Note: extremely rudimentary web application which does absolutely nothing.
# Only there to have something to redirect to when the chatbot renders hyperlinks.
# Resources consulted:
# https://realpython.com/introduction-to-flask-part-1-setting-up-a-static-site/
# https://realpython.com/introduction-to-flask-part-2-creating-a-login-page/
# https://realpython.com/flask-by-example-part-1-project-setup/
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
# https://www.tutorialspoint.com/flask/flask_templates.htm
############################################
from flask import Flask, render_template, redirect

# create application object
app = Flask(__name__)


# with the @ decorator, we link a specific url to the function that follows
@app.route('/')
def home():
    return render_template("index.html")  # render html template in templates folder


@app.route('/search')
def artwork_search():
    return render_template("artwork-search.html")


@app.route('/bidding-portal')
def bidding_portal():
    return render_template("bidding-portal.html")


# start local server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=False)

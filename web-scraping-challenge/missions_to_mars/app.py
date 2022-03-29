from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Flask instance
app = Flask(__name__)

# Pymongo setup
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route for html
@app.route("/")
def home():

    mars_db = mongo.db.collection.find_one()
    return render_template("index.html", mars=mars_db)

# Scrape route
@app.route("/scrape")
def scrape():
  
    # mars_dict = mongo.db.collection
    mars_data = scrape_mars.scrape()
    mongo.db.collection.update({}, mars_data, upsert=True)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
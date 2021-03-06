from flask import Flask, render_template, jsonify, redirect
import scrape_mars
from flask_pymongo import PyMongo

app = Flask(__name__)

mongo = PyMongo(app)

@app.route("/scrape")
def scrapy():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update(
        {},
        mars_data,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)


if __name__ == "__main__":
    app.run(debug=True)
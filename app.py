import datetime
import os
from flask import Flask, render_template, request      #from <package> import <class>, <class>,...
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db= client.microblog           

    entries = []

    @app.route("/", methods=["GET", "POST"])            #endpoint registrations      
    def home():
        if request.method == "POST":       
            entry_content = request.form.get("content")
            date = datetime.datetime.today().strftime("%Y-%m-%d")
            entries.append((entry_content,date))
            app.db.entries.insert_one({"content": entry_content, "date": date})

        entries_with_date = [
            (entry[0],
            entry[1],
            datetime.datetime.strptime(entry[1],"%Y-%m-%d").strftime("%b %d")
            )
            for entry in entries
        ]
        return render_template("home.html", entries=entries_with_date)
    
    return app
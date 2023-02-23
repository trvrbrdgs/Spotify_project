from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func ,inspect,Table, Column, ForeignKey
from flask import Flask, jsonify, render_template
username = 'postgres'
password = ''
import pandas as pd
# from flask_cors import CORS
#Read data files
#=======================================================
spotify_df = pd.read_csv('fy_spotify_cleaned.csv')
spotify_df = pd.DataFrame(spotify_df)

#Connect to Database
#psql_conn_str = "postgres:postgres@localhost:5432/spotify_DB"
engine = create_engine(f'postgresql://{username}:{password}@localhost:5432/spotify_DB')
session = Session(engine)

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
table = Base.metadata.tables['spotify_data']

#write df to database
#spotify_df.to_sql(name='spotify_data',con=engine, if_exists='replace',index=False)

app = Flask(__name__)
@app.route("/")
def main():
    print("Server received request for 'Home' page...")
    return("<div ><p><h1> Welcome to Spotify Data Api!</h1></p>"
    "<li><strong> spotyify_table:</strong><font color='orange'> /api/v1.0/</font></li>")

@app.route("/api/v1.0/")
def population():
    spotify1 = session.query(table)
    spotify1 = pd.read_sql('select * from spotify_data', con=engine)
    spotify1 = pd.DataFrame(spotify1, columns=['track_name',"week"])
    spotify1 = spotify1.to_dict()
    return jsonify(spotify1)

# @app.route("/app")
# def home():
#     return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
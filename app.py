import re
import pandas as pd
import sqlite3

from flask import Flask, jsonify, request, render_template, redirect, url_for
from data_cleansing import processing_text

from flasgger import Swagger
from flasgger import swag_from

from data_reading_and_writing import create_table, insert_to_table, read_table

app = Flask(__name__)


swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "docs",
            "route": '/docs.json',
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}


swagger = Swagger(app,  config=swagger_config)


TABLE_NAME = "tweet_cleaning"


@app.route('/', methods=['GET', "POST"])
def hello_world():
    if request.method == 'POST':
        go_to_page = request.form['inputText']
        if go_to_page == "1":
            return redirect(url_for("input_text_processing"))
        elif go_to_page == "2":
            return redirect(url_for("input_file_processing"))
        elif go_to_page == "3":
            return redirect(url_for("read_database"))
    else:
        return render_template("index.html")


@app.route('/text-processing', methods=['GET', 'POST'])
def input_text_processing():
    if request.method == 'POST':
        previous_text = request.form['inputText']
        cleaned_text = processing_text(previous_text)
        json_response = {'previous_text': previous_text,
                         'cleaned_text': cleaned_text
                         }
        json_response = jsonify(json_response)
        return json_response
    else:
        return render_template("input_processing.html")


@app.route('/file-processing', methods=['GET', 'POST'])
def input_file_processing():
    if request.method == 'POST':
        input_file = request.files['inputFile']
        df = pd.read_csv(input_file, encoding='latin1')
        if ("Tweet" in df.columns):
            list_of_tweets = df['Tweet']  # yang dari CSV
            list_of_cleaned_tweet = df['Tweet'].apply(
                lambda x: processing_text(x))  # ini yang hasil cleaning-an

            create_table()
            # disini di-looping barengan
            for previous_text, cleaned_text in zip(list_of_tweets, list_of_cleaned_tweet):
                insert_to_table(value_1=previous_text, value_2=cleaned_text)

            json_response = {'list_of_tweets': list_of_tweets[0],
                             'list_of_cleaned_tweet': list_of_cleaned_tweet[0]
                             }
            json_response = jsonify(json_response)
            return json_response
        else:
            json_response = {
                'ERROR_WARNING': "NO COLUMNS 'Tweet' APPEAR ON THE UPLOADED FILE"}
            json_response = jsonify(json_response)
            return json_response
        return json_response
    else:
        return render_template("file_processing.html")


@app.route('/read-database', methods=['GET', 'POST'])
def read_database():
    if request.method == "POST":
        showed_index = request.form['inputIndex']
        showed_keywords = request.form['inputKeywords']
        if len(showed_index) > 0:
            # print("AAAAAAAAAA")
            result_from_reading_database = read_table(
                target_index=showed_index)
            previous_text = result_from_reading_database[0].decode('latin1')
            cleaned_text = result_from_reading_database[1].decode('latin1')
            json_response = {'Index': showed_index,
                             'Previous_text': previous_text,
                             'Cleaned_text': cleaned_text
                             }
            json_response = jsonify(json_response)
            return json_response
        elif len(showed_keywords) > 0:
            # print("BBBBBBBBB")
            results = read_table(target_keywords=showed_keywords)
            json_response = {'showed_keywords': showed_keywords,
                             'previous_text': results[0][0].decode('latin1'),
                             'cleaned_text': results[0][1].decode('latin1')
                             }
            json_response = jsonify(json_response)
            return json_response
        else:
            # print("CCCCCCCC")
            json_response = {'ERROR_WARNING': "INDEX OR KEYWORDS IS NONE"}
            json_response = jsonify(json_response)
            return json_response
    else:
        return render_template("read_database.html")


# @ swag_from("docs/hello_world.yml", methods=['GET'])
# @ app.route('/', methods=['GET'])
# def hello_world():
#     json_response = {
#         'status_code': 200,
#         'description': "Hello World",
#         'data': 'Hello World'
#     }
#     response_data = jsonify({"response": "SUCCESS"})
#     return response_data
# @swag_from("docs/input_processing.yml", methods=['POST'])
# @app.route('/input-processing', methods=['POST'])
# def input_processing():
#     text = 'pengguna pengguna aku itu akunnku tau matamu tapi dilihat dari mana itu aku'
#     cleaned_tweet = processing_text(text)
#     results = read_table(table_name='cleaning_tweet')
#     last_index = len(results)
#     insert_to_table = (last_index, cleaned_tweet)
#     response_data = jsonify({"response": "SUCCESS"})
#     return response_data
# @swag_from("docs/file_processing.yml", methods=['POST'])
# @app.route('/file-processing', methods=['POST'])
# def text_processing():
#     df = pd.read_csv("/Users/pro2015/Desktop/chapter 3 binar/data/challenge gold/app.py/data.csv",
#                      encoding="latin-1")
#     df['cleaning_new_tweet'] = df['Tweet'].apply(lambda x: processing_text(x))
#     create_table()
#     text = request.form.get('upload_file')
#     for idx, (tweet_1, tweet_2) in enumerate(zip(df['Tweet'], df['cleaning_new_tweet'])):
#         cleaned_tweet = processing_text(text)
#         insert_to_table(value_1=idx,
#                         value_2=cleaned_tweet)
#         response_data = jsonify({"response": "SUCCESS"})
#         return response_data
# @ swag_from("docs/read_index_data.yml", methods=['POST'])
# @ app.route('/read-index-data', methods=['POST'])
# def read_index_data():
#     index = request.form.get('text')
#     results = read_table(target_index=int(index), table_name='cleaning_tweet')
#     response_data = jsonify({"tweets": "result"})
#     return response_data
if __name__ == '__main__':
    app.run(debug=True)

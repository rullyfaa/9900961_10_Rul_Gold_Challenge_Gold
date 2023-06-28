from flask import Flask, jsonify, request
# from data_reading_and_writing import create_json_response
import re

from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

from data_reading_and_writing import create_table, insert_to_table, read_table
# create flask object

app = Flask(__name__)
app.json_provider_class = LazyJSONEncoder
# app.json_encoder = LazyJSONEncoder

# create swagger_template
swagger_template = {'info': {'title': LazyString(lambda: 'API Documentation for Data Processing dan Modelling'),
                             'version': LazyString(lambda: '1.0.0'),
                             'description': LazyString(lambda: 'Dokumnetasi API untuk Data Processing dan Modelling')
                             },
                    'host': LazyString(lambda: request.host)
                    }

swagger_config = {
    "headers": [],
    "specs": [{"endpoint": "docs", "route": '/docs.json'}],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}

swagger = Swagger(app,
                  # template = swagger_template,
                  config=swagger_config
                  )


@swag_from("docs/hello_world.yml", methods=['GET'])
@app.route('/', methods=['GET'])
def hello():
    # json_response = create_json_response(description="Original Teks",data="Halo, apa kabar semua?")
    response_data = jsonify({"response": "SUCCESS"})
    return response_data


@swag_from("docs/", methods=['POST'])
@app.route('/input-processing', methods=['POST'])
def input_processing():

    cleaned_tweet = processing_text(text)
    results = read_table(table_name('cleaning_tweet'))
    last_index = len(results)
    insert_to_table = (last_index, cleaned_tweet)

    response_data = jsonify({"response": "SUCCESS"})
    return response_data


@swag_from("docs/file_processing.yml", methods=['POST'])
@app.route('/file-processing', methods=['POST'])
def text_processing():
    df = pd.read_csv("Desktop/chapter 3 binar/drive/data.csv",
                     encoding="latin-1")
    create_table()
    text = request.form.get('upload_file')
    for idx, tweet in enumerate(df['Tweet']):
        cleaned_tweet = processing_text(Tweet)
        insert_to_table(value_1=Index,
                        value_2=cleaned_tweet,
                        table_name=TABLE_NAME)

        response_data = jsonify({"response": "SUCCESS"})
        return response_data


@swag_from("docs/read_index_data.yml", methods=['POST'])
@app.route('/read-index-data', methods=['POST'])
def read_index_data():
    index = request.form.get('text')
    results = read_table(target_index=int(index), table_name='cleaning_tweet')

    response_data = jsonify({"tweets": "result"})
    return response_data


if __name__ == '__main__':
    app.run(debug=True)

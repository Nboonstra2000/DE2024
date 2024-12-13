# importing Flask and other modules
import json
import logging
import os
from io import StringIO

import pandas as pd
from flask import Flask, request, render_template, jsonify

from diabetes_predictor import DiabetesPredictor

# Flask constructor
app = Flask(__name__)

dp = DiabetesPredictor(os.environ.get('MODEL_NAME', 'MODEL_NAME environment variable is not set.'))


# A decorator used to tell the application
# which URL is associated function
@app.route('/checkdiabetes', methods=["GET", "POST"])
def check_diabetes():
    if request.method == "GET":
        return render_template("input_form_page.html")

    elif request.method == "POST":
        prediction_input = [
            {
                "fixed_acidity": float(request.form.get("fixed_acidity")),  # getting input with name = fixed_acidity in HTML form
                "volatile_acidity": float(request.form.get("volatile_acidity")),  # getting input with name = volatile_acidity in HTML form
                "citric_acid": float(request.form.get("citric_acid")),
                "residual_sugar": float(request.form.get("residual_sugar")),
                "chlorides": float(request.form.get("chlorides")),
                "free_sulfur_dioxide": float(request.form.get("free_sulfur_dioxide")),
                "total_sulfur_dioxide": float(request.form.get("total_sulfur_dioxide")),
                "density": float(request.form.get("density")),
                "pH": float(request.form.get("pH")),
                "sulphates": float(request.form.get("sulphates")),
                "alcohol": float(request.form.get("alcohol"))
            }
        ] 
        print(prediction_input)
        logging.debug("Prediction Input : %s", prediction_input)
        df = pd.read_json(StringIO(json.dumps(prediction_input)), orient='records')
        
        status,number = dp.predict_single_record(df)
        print(status)
        print(number)
        return render_template("response_page.html",
                               prediction_variable=number[0])

    else:
        return jsonify(message="Method Not Allowed"), 405  # The 405 Method Not Allowed should be used to indicate
    # that our app that does not allow the users to perform any other HTTP method (e.g., PUT and  DELETE) for
    # '/checkdiabetes' path


# The code within this conditional block will only run the python file is executed as a
# script. See https://realpython.com/if-name-main-python/
if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0', debug=True)

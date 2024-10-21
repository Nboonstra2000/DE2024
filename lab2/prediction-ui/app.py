# importing Flask and other modules
import json
import os
import logging
import requests
from flask import Flask, request, render_template, jsonify

# Flask constructor
app = Flask(__name__)


# A decorator used to tell the application
# which URL is associated function
@app.route('/checkdiabetes', methods=["GET", "POST"])
def check_diabetes():
    if request.method == "GET":
        return render_template("input_form_page.html")

    elif request.method == "POST":
        # Collect the input data from the form (features for the wine prediction)
        """ prediction_input = [
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
        ] """
        prediction_input = [
            {
                "fixed_acidity": float(request.form.get("fixed_acidity")),  # getting input with name = fixed_acidity in HTML form
                "volatile_acidity": float(request.form.get("volatile_acidity")),  # getting input with name = volatile_acidity in HTML form
                "citric_acid": 1,
                "residual_sugar": 1,
                "chlorides": 1,
                "free_sulfur_dioxide": 1,
                "total_sulfur_dioxide": 1,
                "density": 1,
                "pH": 1,
                "sulphates": 1,
                "alcohol": 1
            }
        ] 
        print(prediction_input)
        logging.debug("Prediction input : %s", prediction_input)

        # use requests library to execute the prediction service API by sending an HTTP POST request
        # use an environment variable to find the value of the diabetes prediction API
        # json.dumps() function will convert a subset of Python objects into a json string.
        # json.loads() method can be used to parse a valid JSON string and convert it into a Python Dictionary.
        predictor_api_url = 'http://127.0.0.1:5001/diabetes_predictor/'
        res = requests.post(predictor_api_url, json=json.loads(json.dumps(prediction_input)))
        print(res)
        prediction_value = res.json()['result']
        logging.info("Prediction Output : %s", prediction_value)
        return render_template("response_page.html",
                               prediction_variable=prediction_value)

    else:
        return jsonify(message="Method Not Allowed"), 405  # The 405 Method Not Allowed should be used to indicate
    # that our app that does not allow the users to perform any other HTTP method (e.g., PUT and  DELETE) for
    # '/checkdiabetes' path


# The code within this conditional block will only run the python file is executed as a
# script. See https://realpython.com/if-name-main-python/
if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5001)), host='0.0.0.0', debug=True)

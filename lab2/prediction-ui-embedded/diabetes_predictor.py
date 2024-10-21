import logging

from keras.models import load_model


class DiabetesPredictor:
    def __init__(self, model_file):
        self.model = load_model(model_file)

    def predict_single_record(self, df):
        print(df)
        y_pred = self.model.predict(df)
        logging.info("Prediction Output : %s", y_pred[0])
        status = (y_pred[0] > 15)
        return status

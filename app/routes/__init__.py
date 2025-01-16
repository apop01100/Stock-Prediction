from flask import Blueprint
from app.controllers.lstm_controller import LSTMController

lstm_models = Blueprint("lstm_models", __name__)
lstm_models.add_url_rule("/training", view_func=LSTMController.create_new_lstm_model, methods=["POST"])
lstm_models.add_url_rule("/predict", view_func=LSTMController.predict_lstm_model, methods=["POST"])

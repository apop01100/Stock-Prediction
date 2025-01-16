from flask import request, jsonify
from app.utils.functions.training_new_model import training_new_model
from app.utils.validations.lstm_validator import LstmTrainValidator, LstmPredictValidator
from pydantic import ValidationError
from app.utils.functions.check_models import check_models
from app.utils.functions.predict_stock_price import predict_stock_price
import yfinance as yf

class LSTMController:
    
    @staticmethod
    def create_new_lstm_model():
        data = request.get_json()
        
        try:
            validator = LstmTrainValidator.model_validate(data)
        except ValidationError as e:
            return jsonify({"message": e.errors()})
        
        response = training_new_model(validator.model_dump())
        
        if response is None:
            return jsonify({"message": "Model training failed"}), 500
        
        if "error" in response:
            return jsonify(response), 400
        
        return jsonify(response), 200
    
    @staticmethod
    def predict_lstm_model():
        data = request.get_json()
        
        try:
            validator = LstmPredictValidator.model_validate(data)
        except ValidationError as e:
            return jsonify({"message": e.errors()}), 400
        
        response = predict_stock_price(validator.model_dump())
        
        if "error" in response:
            return jsonify(response), 400
        
        return jsonify(response), 200
        
        
        
        
        
        
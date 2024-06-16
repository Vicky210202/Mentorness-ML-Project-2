from flask import Flask, request, render_template
import pandas as pd
import numpy as np
from src.pipeline.prediction_pipeline import PredictionPipeline, PredictData

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = PredictData(
        Vehicle_Type = request.form.get("Vehicle_Type"),
        Vehicle_Dimensions = request.form.get("Vehicle_Dimensions"),
        Geographical_Location = request.form.get("Geographical_Location"),
        Transaction_Amount = float(request.form.get("Transaction_Amount")),
        Amount_paid = float(request.form.get("Amount_paid"))        
    )

    predict_df = data.get_predict_data_as_data_frame()
    print(predict_df)

    predict_pipeline = PredictionPipeline()
    prediction = predict_pipeline.predict(predict_df)

    return render_template('index.html', results = prediction[0])

if __name__ == '__main__':
    app.run(debug=True)


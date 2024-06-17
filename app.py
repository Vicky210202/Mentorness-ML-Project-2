import os
from dotenv import load_dotenv
  
from flask import Flask, request, render_template
from src.pipeline.prediction_pipeline import PredictionPipeline, PredictData
from src.pipeline.database_pipeline import DatabaseHandler


load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def predict():
    form_data = {
        "Vehicle_Type": request.form.get("Vehicle_Type"),
        "Vehicle_Plate_Number": request.form.get("Vehicle_Plate_Number"),
        "Vehicle_Dimensions": request.form.get("Vehicle_Dimensions"),
        "Geographical_Location": request.form.get("Geographical_Location"),
        "Transaction_Amount": float(request.form.get("Transaction_Amount")),
        "Amount_paid": float(request.form.get("Amount_paid"))
    }

    data = PredictData(
        Vehicle_Type=form_data["Vehicle_Type"],
        Vehicle_Plate_Number=form_data["Vehicle_Plate_Number"],
        Vehicle_Dimensions=form_data["Vehicle_Dimensions"],
        Geographical_Location=form_data["Geographical_Location"],
        Transaction_Amount=form_data["Transaction_Amount"],
        Amount_paid=form_data["Amount_paid"]
    )

    predict_df = data.get_predict_data_as_data_frame()
    predict_df_ = predict_df.drop(columns=["Vehicle_Plate_Number", "Transaction_Amount", "Amount_paid"], axis=1)

    predict_pipeline = PredictionPipeline()
    prediction = predict_pipeline.predict(predict_df_)

    predict_df["Fraud_indicator"] = int(prediction[0])
    database_handler = DatabaseHandler(
        dbname = os.getenv('DB_NAME'),
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD'),
        host = os.getenv('DB_HOST'),
        port = os.getenv('DB_PORT')
    )

    database_handler.insert_records(predict_df)

    print(predict_df)
    
    return render_template('index.html', results = prediction[0])

if __name__ == '__main__':
    app.run(debug=True)
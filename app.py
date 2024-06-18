import os
import sys
from dotenv import load_dotenv
from src.exception import CustomException
import logging

from flask import Flask, request, render_template, flash
from src.pipeline.prediction_pipeline import PredictionPipeline, PredictData
from src.pipeline.database_pipeline import DatabaseHandler

# Load environment variables
load_dotenv()

# Configure logging to output to the console
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')  # Ensure you set a secret key for flash messages

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def predict():
    try:
        logging.error("Prediction started")
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
        logging.error("Prediction data gathered")
        predict_df = data.get_predict_data_as_data_frame()
        predict_df_ = predict_df.drop(columns=["Vehicle_Plate_Number", "Transaction_Amount", "Amount_paid"], axis=1)

        predict_pipeline = PredictionPipeline()
        prediction = predict_pipeline.predict(predict_df_)

        logging.error("Data predicted")
        predict_df["Fraud_indicator"] = int(prediction[0])

        logging.error("Database is about to connect")
        database_handler = DatabaseHandler(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        logging.error("Database connected")
        database_handler.insert_records(predict_df)

        logging.error("Records entered in the database")
        print(predict_df)

        return render_template('index.html', results=prediction[0])

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        flash(f"An error occurred: {str(e)}", 'error')
        return render_template('index.html')

# Uncomment the following line to run the app locally
# if __name__ == '__main__':
#     app.run(debug=True)

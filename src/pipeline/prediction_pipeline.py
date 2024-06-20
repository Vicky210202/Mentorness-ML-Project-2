import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from exception import CustomException
from logger import logging
from utils import load_object

import pandas as pd

# Creating pipelines for predicting the unseen given by the user in ML flask app
class PredictionPipeline:
    def __init__(self):
        pass

    def predict(self, predict_df):
        try:
            model = load_object('model artifacts\\best_model.pkl')
            preprocessor = load_object('model artifacts\preprocessor.pkl')
            preprocessed_data = preprocessor.transform(predict_df)
            preprocessed_data = pd.DataFrame(preprocessed_data, columns = predict_df.columns)
            prediction = model.predict(preprocessed_data)
            logging.info("Successfully predicted")

            return prediction
         
        except Exception as e:
            raise CustomException(e, sys)

        

class PredictData:
    def __init__(
            self,
            Vehicle_Type: str,
            Vehicle_Plate_Number: str, 
            Vehicle_Dimensions: str, 
            Geographical_Location: str, 
            Transaction_Amount: int,
            Amount_paid: int
        ):
        self.Vehicle_Type = Vehicle_Type
        self.Vehicle_Plate_Number = Vehicle_Plate_Number
        self.Vehicle_Dimensions = Vehicle_Dimensions
        self.Geographical_Location = Geographical_Location
        self.Transaction_Amount = Transaction_Amount
        self.Amount_paid = Amount_paid
        self.Amount_Frauded = Transaction_Amount - Amount_paid
       
    def get_predict_data_as_data_frame(self):
        try:
            predict_data = [
                {
                    'Vehicle_Type' : self.Vehicle_Type,
                    'Vehicle_Plate_Number' : self.Vehicle_Plate_Number,
                    'Vehicle_Dimensions' : self.Vehicle_Dimensions,
                    'Geographical_Location' : self.Geographical_Location,
                    'Transaction_Amount' :     self.Transaction_Amount,
                    'Amount_paid' : self.Amount_paid ,
                    'Amount_Frauded' : self.Amount_Frauded
                }
            ]
            predict_df = pd.DataFrame(predict_data)
            logging.info("prediction input data gathered.")
            return predict_df
        
        except Exception as e:
            raise CustomException(e, sys)    
        
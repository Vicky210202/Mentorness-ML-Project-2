import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from exception import CustomException

from dataclasses import dataclass

import pandas as pd
import psycopg2



class DatabaseHandler:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def insert_records(self, predict_df):
        try:
            conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            

            cursor = conn.cursor()

            for index, row in predict_df.iterrows():
                try:
                    vehicle_type = row['Vehicle_Type']
                    vehicle_plate_number = row['Vehicle_Plate_Number']
                    amount_frauded = row['Amount_Frauded']

                    fraud_labels = ["Fraud", "Legit"]
                    fraud_indicator = fraud_labels[row['Fraud_indicator']] 
                    
                    cursor.execute("""
                        INSERT INTO fastag (vehicle_type, vehicle_plate_number, amount_frauded, 
                                   fraud_indicator)
                        VALUES (%s, %s, %s, %s) """, 
                        (vehicle_type, vehicle_plate_number, amount_frauded, fraud_indicator))
                    conn.commit()

                except Exception as e:
                    conn.rollback()
                    raise CustomException(e, sys)

            cursor.close()
            conn.close()

            
        except Exception as e:
            raise CustomException(e, sys)
    

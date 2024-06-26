import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from exception import CustomException
from logger import logging

import pandas as pd
from sklearn.model_selection import train_test_split 
from dataclasses import dataclass

# Configuration file paths for train, test and raw data.
@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('model artifacts', 'train.csv')
    test_data_path: str = os.path.join('model artifacts', 'test.csv')
    raw_data_path: str = os.path.join('model artifacts', 'data.csv')


# Data ingestion algorithm
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Started the data ingestion process.")
        try:
            data = pd.read_csv(r'notebook\data\FastagFraudDetection.csv')
            logging.info("Imported data as dataframe.")

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok = True)
            data.to_csv(self.ingestion_config.raw_data_path, index = None)
            logging.info("Exported source data in model artifacts.")

            logging.info("Train test split initiated")
            train_data, test_data = train_test_split(data, test_size = 0.2, random_state = 42)
            train_data.to_csv(self.ingestion_config.train_data_path, index = None) 
            test_data.to_csv(self.ingestion_config.test_data_path, index = None)
            logging.info("Train test split executed succesfully and exported to model artifacts.")

            logging.info("Data ingestion executed successfully")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            raise  CustomException(e, sys)




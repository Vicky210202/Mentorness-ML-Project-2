import os
import sys
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging 

import numpy as np
import pandas as pd
from category_encoders import TargetEncoder
from sklearn.preprocessing import StandardScaler, LabelEncoder
from src.utils import save_object
from src.utils import VehicleDimensionsEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

@dataclass
class DataTransformationConfig:
    preprocessor_file_path: str = os.path.join('model artifacts', 'preprocessor.pkl')
    train_data_path: str = os.path.join('model artifacts', 'feature_engineering_train.csv')
    test_data_path: str = os.path.join('model artifacts', 'feature_engineering_test.csv')
    preprocessed_train_data_path: str = os.path.join('model artifacts', 'preprocessed_train_data.csv')
    preprocessed_test_data_path: str = os.path.join('model artifacts', 'preprocessed_test_data.csv')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def feature_engineer(self, train_data_path, test_data_path):
        logging.info("Starting data transformation.")
        logging.info("Initializing feature engineering.")
        try:
            new_feature =  'Amount_Frauded'
            target_variable = 'Fraud_indicator'
            selected_features = ['Vehicle_Type', 'Vehicle_Dimensions', 
                                 'Geographical_Location', new_feature, target_variable]

            logging.info("Reading train data and test data")
            train_data, test_data = pd.read_csv(train_data_path), pd.read_csv(test_data_path)
            logging.info("Train data and test data imported as train and test dataframes.")

            train_data[new_feature] = train_data["Transaction_Amount"] - train_data["Amount_paid"]
            test_data[new_feature] = test_data["Transaction_Amount"] - test_data["Amount_paid"]
            logging.info(f"New feature: {new_feature} created successfully.")

            target_variable_encoder = LabelEncoder()
            train_data[target_variable] = target_variable_encoder.fit_transform(train_data[target_variable])
            test_data[target_variable] = target_variable_encoder.fit_transform(test_data[target_variable])
            logging.info("Target variable encoded.")

            train_data = train_data[selected_features]
            test_data = test_data[selected_features]
            logging.info(f"feature engineering successfully finished, features: {selected_features}.")
            train_data.to_csv(self.data_transformation_config.train_data_path, index = None) 
            test_data.to_csv(self.data_transformation_config.test_data_path, index = None)
            logging.info("Feature engineered train and test data exported to model artifacts.")

            return(
                train_data,
                test_data
            )

        except Exception as e:
            raise CustomException(e, sys)

    def get_data_preprocessor(self):
        logging.info("Preprocessing initiated")
        try:
            numerical_features = ['Amount_Frauded']
            target_encoding_features = ['Vehicle_Type', 'Geographical_Location']
            ordinal_encoding_features = ['Vehicle_Dimensions']
            Vehicle_Dimensions = {'Large': 3, 'Medium': 2, 'Small': 1}
            
            numerical_pipeline = Pipeline(
                steps = [
                    ('scaler', StandardScaler())
                ]
            )

            target_encoding_pipeline = Pipeline(
                steps = [
                    ('target_encoder', TargetEncoder()),
                    ('scaler', StandardScaler())
                ]
            )

            ordinal_encoding_pipeline = Pipeline(
                steps = [
                    ('ordinal_encoder', VehicleDimensionsEncoder()),
                    ('scaler', StandardScaler())
                
                ]
            )

            logging.info("Pipelines created!")
            logging.info(f"Numerical features: {numerical_features}")
            logging.info(f"Target encoding features: {target_encoding_features}")
            logging.info(f"Ordinal encoding features: {ordinal_encoding_features}")
            logging.info("All features are to be scaled and encoded.")

            preprocessor = ColumnTransformer(
                [
                    ('numerical_pipeline', numerical_pipeline, numerical_features),
                    ('target_encoding_pipeline', target_encoding_pipeline, target_encoding_features),
                    ('ordinal_encoding_pipeline', ordinal_encoding_pipeline, ordinal_encoding_features)

                ]
            )
            
            logging.info("Preprocessor is successfully created!")

            return preprocessor 
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_preprocessor(self, train_data, test_data):
        try:
            logging.info("Obtaining the preprocessor")
            preprocessor = self.get_data_preprocessor()
            target_variable = 'Fraud_indicator'

            X_train = train_data.drop(columns = [target_variable], axis = 1)
            y_train = train_data[target_variable]

            X_test = test_data.drop(columns = [target_variable], axis = 1)
            y_test = test_data[target_variable]

            logging.info("Preprocessing initiated!")

            X_train_arr = preprocessor.fit_transform(X_train, y_train)
            X_test_arr = preprocessor.transform(X_test)

            train_arr = np.c_[X_train_arr, np.array(y_train)]
            test_arr = np.c_[X_test_arr, np.array(y_test)]

            logging.info("Saving the preprocessing object.")

            save_object(
                file_path = self.data_transformation_config.preprocessor_file_path,
                obj = preprocessor
            )

            logging.info("Creating preprocessed train data and test data as dataframes")
            preprocessed_train_data = pd.DataFrame(train_arr, columns = train_data.columns)
            preprocessed_test_data = pd.DataFrame(test_arr, columns = test_data.columns)
            logging.info("Created dataframes successfully")

            preprocessed_train_data.to_csv(self.data_transformation_config.preprocessed_train_data_path, index = None)
            preprocessed_test_data.to_csv(self.data_transformation_config.preprocessed_test_data_path, index = None)
            logging.info("Preprocessed train and test data exported to model artifacts.")


            
            return(
                preprocessed_train_data,
                preprocessed_test_data
            )

        except Exception as e:
            raise CustomException(e, sys)
            

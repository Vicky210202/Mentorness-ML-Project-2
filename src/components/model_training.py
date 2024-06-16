import os
import sys
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

from dataclasses import dataclass

import pandas as pd 
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report

@dataclass
class ModelTrainingConfig:
    best_model_file_path: str = os.path.join('model artifacts', 'best_model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_training_config = ModelTrainingConfig()

    def initiate_model_trainer(self, preprocessed_train_data, preprocessed_test_data):
        try:
            logging.info("Model training initiated.")
            
            logging.info("Spliting Target and Input features")
            target_variable = 'Fraud_indicator'
            X_train = preprocessed_train_data.drop(columns = [target_variable], axis = 1)
            y_train = preprocessed_train_data[target_variable]
            X_test = preprocessed_test_data.drop(columns = [target_variable], axis = 1)
            y_test = preprocessed_test_data[target_variable]

            classification_models = {
                'LogisticRegression' : LogisticRegression(),
                'RandomForestClassifier' : RandomForestClassifier(),
                'KNeighborsClassifier:' : KNeighborsClassifier(),
                'SVC' : SVC()
            }

            for name, model in classification_models.items():
                scores = cross_val_score(model, pd.concat([X_train, X_test], axis = 0), pd.concat([y_train, y_test], axis = 0), cv=25)
                print(f'{name} Cross-Validation Accuracy: {np.round(np.mean(scores), 2)}')

            classification_reports = {}

            for model_name, model in classification_models.items():
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                report = classification_report(y_test, y_pred, output_dict=True)
                classification_reports[model_name] = report
                print(f"{model_name} Classification Report:\n", classification_report(y_test, y_pred))
                print("".center(100, "="))
            logging.info("Model training is executed successfully.")

            best_model_name = max(classification_reports, key=lambda x: classification_reports[x]['accuracy'])
            best_model = classification_models[best_model_name]
            best_model_accuracy = classification_reports[best_model_name]['accuracy']

            logging.info("Evaluating the best performing model.")    
            if best_model_accuracy < 0.9:
                raise CustomException("Best model not found")
            else:
                print(f"\nBest Model: {best_model_name} with Accuracy: {best_model_accuracy:.2f}")
                logging.info("Best model found on the both training and testing data.")
                logging.info(f"The best model: {best_model_name}!") 
                logging.info("Saving the best model.")
                save_object(
                    file_path = self.model_training_config.best_model_file_path,
                    obj = best_model
                )              

                
        except Exception as e:
            raise CustomException(e, sys)

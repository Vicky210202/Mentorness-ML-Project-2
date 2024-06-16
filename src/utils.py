import os
import sys
from src.exception import CustomException
from src.logger import logging 

import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from dill import dump, load

class VehicleDimensionsEncoder(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.mapping = {'Large': 3, 'Medium': 2, 'Small': 1}
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X_encoded = X.copy()
        X_encoded['Vehicle_Dimensions'] = X_encoded['Vehicle_Dimensions'].map(self.mapping)
        return X_encoded
    
    def fit_transform(self, X, y=None):
        self.fit(X, y)
        return self.transform(X)


def save_object(file_path, obj):
    logging.info("Utilizing save_object() from utils.py")
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok = True)

        with open(file_path, 'wb') as file_object:
            dump(obj, file_object)
        logging.info("Saved the object successfully!")
    except Exception as e:
        raise CustomException(e, sys)

def load_object(file_path):
    try:
        with open(file_path, "rb") as file_object:
            return load(file_object)
        
    except Exception as e:
        raise CustomException(e, sys) 
            


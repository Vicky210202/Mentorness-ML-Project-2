from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation


if __name__ == "__main__" :
    
    # data ingestion
    data_obj = DataIngestion()
    train_data_path, test_data_path = data_obj.initiate_data_ingestion()


    # data transformation
    data_transformation_obj = DataTransformation()
    train_data, test_data = data_transformation_obj.feature_engineer(train_data_path, test_data_path)
    train_arr, test_arr = data_transformation_obj.initiate_preprocessor(train_data, test_data)


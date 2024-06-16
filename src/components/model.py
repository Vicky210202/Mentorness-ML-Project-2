from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_training import ModelTrainer


if __name__ == "__main__" :
    
    # data ingestion
    data_obj = DataIngestion()
    train_data_path, test_data_path = data_obj.initiate_data_ingestion()

    # data transformation
    data_transformation_obj = DataTransformation()
    train_data, test_data = data_transformation_obj.feature_engineer(train_data_path, test_data_path)
    preprocessed_train_data, preprocessed_test_data = data_transformation_obj.initiate_preprocessor(train_data, test_data)

    # model training
    model_training_obj = ModelTrainer()
    model_training_obj.initiate_model_trainer(preprocessed_train_data, preprocessed_test_data)


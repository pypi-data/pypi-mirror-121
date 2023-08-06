import logging
import os
import joblib
def save_model(model,file_name): 
    """This saves the trained model to
    Args:
        model (python object): trained model to
        filename (str): path to save the trained model
    """
    logging.info("Saving the trained model")
    model_dir = "models"
    os.makedirs(model_dir, exist_ok=True)  
    filepath = os.path.join(model_dir, file_name)
    joblib.dump(model, filepath)
    logging.info(f"Saved the trained model in {filepath}")
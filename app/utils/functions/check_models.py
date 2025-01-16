import os

def check_models(name):
    folder_path = "../RestAPI/app/assets/ML/"
    file_name = f"{name}_lstm_model.keras"
    file_path = os.path.join(folder_path, file_name)

    if os.path.exists(file_path):
        return {"message": "Model already exists",
                "status": "error"}
    
    return None